from rest_framework import serializers

from .. import Post
from ...libs.base.base_serializer import BaseSerializer


class PostSerializer(BaseSerializer):
    class Meta:
        model = Post

    user_id = serializers.IntegerField(
        required=True,
        allow_null=False,
        min_value=1,
    )
    title = serializers.CharField(
        required=True,
        allow_null=False,
        trim_whitespace=True,
        allow_blank=False,
        max_length=254,
    )
    text = serializers.CharField(
        required=False,
        allow_null=True,
        trim_whitespace=True,
        allow_blank=False,
        max_length=1000,
    )
