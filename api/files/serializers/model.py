from rest_framework import serializers

from ..models import File


class FileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ['user']