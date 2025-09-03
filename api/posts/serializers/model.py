from rest_framework import serializers

from ..models import Post
from ...users.serializers import UserModelSerializer


class PostModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_user(self, post):
        if 'user' in post._state.fields_cache:
            return UserModelSerializer(post.user).data

        return None
