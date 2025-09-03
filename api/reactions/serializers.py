from rest_framework import serializers

from api.libs.base.base_serializer import BaseSerializer
from api.libs.enums.reaction_type import ReactionType
from .models import Reaction


class ReactionSerializer(BaseSerializer):
    class Meta:
        model = Reaction

    user_id = serializers.IntegerField(
        required=True,
        allow_null=False,
    )
    post_id = serializers.IntegerField(
        required=True,
        allow_null=False,
    )
    type = serializers.ChoiceField(
        required=True,
        allow_null=False,
        choices=ReactionType
    )
