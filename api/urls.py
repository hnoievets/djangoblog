from django.urls import path, include
from rest_framework import routers

from .comments import CommentViewSet
from .posts import PostViewSet
from .users import UserViewSet
from .auth import urlpatterns as auth_urls
from .files import FileViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'user')
router.register(r'posts', PostViewSet, 'post')
router.register(r'comments', CommentViewSet, 'comment')
router.register(r'files', FileViewSet, 'file')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_urls))
]