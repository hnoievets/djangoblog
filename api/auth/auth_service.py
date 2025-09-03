from datetime import timedelta

from django.core.exceptions import BadRequest
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from api.libs.enums.token_type import TokenType
from ..users.models import User


class AuthService:
    algorithm = "HS256"

    @staticmethod
    def generate_token(user: User, token_type: TokenType, lifetime_in_minutes = 15) -> str:
        token = AccessToken.for_user(user)

        token['type'] = token_type.value
        token.set_exp(
            lifetime=timedelta(
                minutes=lifetime_in_minutes
            )
        )

        return str(token)

    @staticmethod
    def verify_token(token_str: str, token_type: TokenType):
        try:
            token = AccessToken(token_str)

            if token.get('type') != token_type:
                raise TokenError()

            return token.payload
        except TokenError:
            raise BadRequest('Invalid token')