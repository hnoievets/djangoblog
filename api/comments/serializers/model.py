from rest_framework import serializers

from ..models import Comment
from api.users.serializers import UserModelSerializer


class CommentModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_user(self, comment):
        if 'user' in comment._state.fields_cache:
            return UserModelSerializer(comment.user).data

        return None