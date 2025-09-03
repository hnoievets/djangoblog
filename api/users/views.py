from http import HTTPMethod

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User
from .serializers import CreateUserSerializer, UserModelSerializer, UpdateUserSerializer
from .user_service import UserService
from ..auth.auth_service import AuthService
from ..files import File
from ..files.files_service import FileService
from ..libs.enums.token_type import TokenType
from ..libs.resources.files.file_type import FileType
from ..utils.config import ConfigService


class UserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def me(self, request):
        user = request.user

        if user.avatar_id:
            user = User.objects.select_related('avatar').get(id=request.user.id)

        return Response(UserModelSerializer(user).data)

    @action(
        permission_classes=[AllowAny],
        methods=[HTTPMethod.POST],
        detail=False,
    )
    def signup(self, request):
        serializer = CreateUserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token = AuthService.generate_token(
            user,
            TokenType.EMAIL_VERIFICATION,
            int(ConfigService.get_env('EMAIL_VERIFICATION_LIFETIME_MINUTES'))
        )

        UserService.send_verification_email(user.email, token)

        return Response(UserModelSerializer(user).data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request: Request, pk: int):
        body = request.data
        user = request.user

        if pk != str(user.id):
            raise PermissionDenied()

        serializer = UpdateUserSerializer(instance=user, data=body, context={'user': user})
        serializer.is_valid(raise_exception=True)

        avatar_id = body['avatar_id']

        if avatar_id and user.avatar_id != avatar_id:
            file = get_object_or_404(
                File,
                pk=avatar_id,
                user_id=pk,
                type=FileType.AVATAR,
                is_used=False
            )

            file.is_used = True
            file.save()

            FileService.delete(avatar_id)

        updated_user = serializer.save()

        return Response(UserModelSerializer(updated_user).data)