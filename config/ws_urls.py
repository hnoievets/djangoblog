from django.urls import path

from api.posts import PostConsumer

websocket_urlpatterns = [
    path('ws/posts/<int:post_id>/', PostConsumer.as_asgi()),
]
