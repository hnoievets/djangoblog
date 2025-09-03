from collections import defaultdict
from http import HTTPMethod
from django.core.exceptions import BadRequest
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.pagination import LimitOffsetPagination

from api.libs.base.query_sort_serializer import QuerySortSerializer
from api.libs.enums.reaction_type import ReactionType
from api.libs.helpers import get_choices_from_enum, add_order_prefix
from api.libs.resources.posts.sort_field import PostsSortFiled
from api.posts import Post
from api.posts.serializers import PostSerializer, PostModelSerializer
from api.reactions import Reaction, ReactionSerializer


class PostViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    search_fields = ['title', 'text']
    paginator = LimitOffsetPagination()

    def create(self, request):
        payload = request.data
        payload['user_id'] = request.user.id

        serializer = PostSerializer(data=payload)

        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        return Response(PostModelSerializer(post).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user_id=request.user.id)

        payload = request.data
        payload['user_id'] = request.user.id

        serializer = PostSerializer(instance=post, data=payload)
        serializer.is_valid(raise_exception=True)

        updated_post = serializer.save()

        return Response(PostModelSerializer(updated_post).data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user_id=request.user.id)

        serializer = PostSerializer(instance=post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_post = serializer.save()

        return Response(PostModelSerializer(updated_post).data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        return Response(PostModelSerializer(post).data, status=status.HTTP_200_OK)

    def list(self, request):
        query_serializer = QuerySortSerializer(
            data=request.query_params,
            sort_choices=get_choices_from_enum(PostsSortFiled),
        )
        query_serializer.is_valid(raise_exception=True)

        query = query_serializer.data
        sort_filed = query['sort']

        queryset = (
            Post.objects
            .all()
            .select_related('user')
        )

        queryset = SearchFilter().filter_queryset(request, queryset, self)
        response = []

        if queryset.count:
            if sort_filed == PostsSortFiled.LIKES:
                annotation = {
                    PostsSortFiled.LIKES.value: Count('reactions', filter=Q(reactions__type=ReactionType.LIKE))
                }

                queryset = (
                    queryset
                    .annotate(**annotation)
                )

            queryset = queryset.order_by(add_order_prefix(sort_filed, query['order']))

            posts = self.paginator.paginate_queryset(queryset, request)
            post_ids = [post.id for post in posts]

            reaction_groups = (
                Reaction.objects
                .filter(post_id__in=post_ids)
                .values('post_id', 'type')
                .annotate(count=Count('id'))
            )

            reactions_by_post = defaultdict(list)

            for row in reaction_groups: (
                reactions_by_post[row['post_id']]
                    .append({
                        'type': row['type'],
                        'count': row['count']
                    })
            )

            for post in posts:
                item = PostModelSerializer(post).data
                item['reactions'] = reactions_by_post[post.id]

                response.append(item)

        return self.paginator.get_paginated_response(response)

    @action(detail=True, methods=[HTTPMethod.PUT], url_path='reactions')
    @transaction.atomic
    def react(self, request, pk):
        payload = {
            'user_id': request.user.id,
            'post_id': pk,
            'type': request.data['type']
        }

        serializer = ReactionSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        post = get_object_or_404(Post, pk=pk)

        if post.user_id == payload['user_id']:
            raise BadRequest('User can\'t react to the own post')

        reaction = Reaction.objects.filter(post_id=pk, user_id=payload['user_id']).first()

        if reaction:
            reaction.delete()

        if not reaction or (reaction and reaction.type != payload['type']):
            serializer.save()

        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user_id=request.user.id)
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
