from http import HTTPMethod

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .auth_service import AuthService
from .serializers import CustomTokenObtainPairSerializer
from ..libs.enums.token_type import TokenType
from ..users.models import User


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VerificationViewSet(ViewSet):
    @action(detail=False, methods=[HTTPMethod.PUT])
    def email(self, request: Request):
        token = request.query_params.get('token')
        payload = AuthService.verify_token(token, TokenType.EMAIL_VERIFICATION)

        user = get_object_or_404(User, id=payload['user_id'])

        user.is_verified = True
        user.save()

        return Response()
