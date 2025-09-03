from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models import User


class BaseUserSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        trim_whitespace=True,
        allow_blank=False,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='User with that username already exists.'
            )
        ]
    )
    first_name = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True
    )
    last_name = serializers.CharField(
        required=False,
        trim_whitespace=True,
        allow_blank=False,
        allow_null=False,
    )
    bio = serializers.CharField(
        required=False,
        trim_whitespace=True,
        allow_null=True,
        allow_blank=False,
    )
    avatar_id = serializers.IntegerField(
        required=False,
        allow_null=True
    )
