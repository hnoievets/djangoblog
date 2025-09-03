from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Comment
from api.comments.serializers import CommentCreateSerializer, CommentModelSerializer, CommentBaseSerializer
from ..posts import PostConsumer


class CommentViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    paginator = LimitOffsetPagination()

    channel_layer = get_channel_layer()

    def create(self, request):
        payload = request.data
        payload['user_id'] = request.user.id

        serializer = CommentCreateSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        comment = serializer.save()
        response = CommentModelSerializer(comment).data

        async_to_sync(self.channel_layer.group_send)(
            PostConsumer.get_room_name(comment.post_id),
            {
                'type': 'comment_created',
                'data': response
            }
        )

        return Response(response, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user_id=request.user.id)

        payload = { 'text': request.data['text'] }

        serializer = CommentBaseSerializer(instance=comment, data=payload)
        serializer.is_valid(raise_exception=True)

        updated_comment = serializer.save()
        response = CommentModelSerializer(updated_comment).data

        async_to_sync(self.channel_layer.group_send)(
            PostConsumer.get_room_name(comment.post_id),
            {
                'type': 'comment_updated',
                'data': response
            }
        )

        return Response(response, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = (
            Comment.objects
            .all()
            .select_related('user')
            .order_by('-id')
        )

        comments = self.paginator.paginate_queryset(queryset, request)
        response = []

        if len(comments):
            response = CommentModelSerializer(comments, many=True).data

        return self.paginator.get_paginated_response(response)

    def destroy(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user_id=request.user.id)
        comment.delete()

        async_to_sync(self.channel_layer.group_send)(
            PostConsumer.get_room_name(comment.post_id),
            {
                'type': 'comment_deleted',
                'data': {'id': pk}
            }
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
