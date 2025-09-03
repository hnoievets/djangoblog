from rest_framework import serializers

from ..models import File
from api.libs.base.base_serializer import BaseSerializer
from api.libs.helpers import get_choices_from_enum
from api.libs.resources.files.file_type import FileType


class FileCreateSerializer(BaseSerializer):
    class Meta:
        model = File

    content_type = serializers.CharField(
        required=True,
        trim_whitespace=True,
        allow_null=False,
        allow_blank=False,
    )
    type = serializers.ChoiceField(
        required=True,
        allow_null=False,
        choices=get_choices_from_enum(FileType)
    )
    original_name = serializers.CharField(
        required=False,
        trim_whitespace=True,
        allow_blank=False
    )
