from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware
from channels.exceptions import DenyConnection
from rest_framework_simplejwt.tokens import AccessToken

from api.users import User


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        if not token:
            raise DenyConnection("Invalid token")

        scope["user"] = await get_user_from_token(token)

        return await super().__call__(scope, receive, send)

@sync_to_async
def get_user_from_token(token):
    payload = AccessToken(token)

    user = User.objects.filter(id=payload["user_id"]).first()

    if not user:
        raise DenyConnection("User not found")

    return user