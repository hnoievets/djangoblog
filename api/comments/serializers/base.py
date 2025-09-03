from rest_framework import serializers

from ..models import Comment
from api.libs.base.base_serializer import BaseSerializer
from api.libs.resources.comments.validation_rule import CommentsValidationRule


class CommentBaseSerializer(BaseSerializer):
    class Meta:
        model = Comment

    text = serializers.CharField(
        required=True,
        allow_null=False,
        trim_whitespace=True,
        allow_blank=False,
        max_length=CommentsValidationRule.TEXT_MAX_LENGTH,
        min_length=CommentsValidationRule.TEXT_MIN_LENGTH,
    )