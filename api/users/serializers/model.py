from rest_framework import serializers

from ..models import User
from ...files.serializers.model import FileModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']


    def get_avatar(self, user):
        if 'avatar' in user._state.fields_cache and user.avatar:
            return FileModelSerializer(user.avatar).data

        return None