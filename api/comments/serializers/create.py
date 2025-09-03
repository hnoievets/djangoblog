from rest_framework import serializers

from api.comments.serializers.base import CommentBaseSerializer


class CommentCreateSerializer(CommentBaseSerializer):
    user_id = serializers.IntegerField(
        required=True,
        allow_null=False,
    )
    post_id = serializers.IntegerField(
        required=True,
        allow_null=False,
    )
