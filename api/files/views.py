from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from . import File
from .files_service import FileService
from api.files.serializers import FileCreateSerializer
from .serializers.presigned_post import PresignedPostSerializer


class FileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request):
        body = request.data
        user_id = request.user.id

        serializer = FileCreateSerializer(data=body)
        serializer.is_valid(raise_exception=True)

        file_key = FileService.generate_file_key(user_id)

        presigned_post = FileService.generate_presigned_post(file_key, body['content_type'])

        file = File.objects.create(
            user_id=user_id,
            type=body['type'],
            original_name=body['original_name'],
            file_key=file_key
        )

        return Response(
            PresignedPostSerializer(presigned_post, file).data,
            status=status.HTTP_201_CREATED
        )
