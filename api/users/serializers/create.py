from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .base import BaseUserSerializer
from ..models import User


class CreateUserSerializer(BaseUserSerializer):
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        allow_blank=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='User with that email already exists.'
            )
        ]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        allow_null=False,
        trim_whitespace=True
    )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)