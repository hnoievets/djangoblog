from rest_framework import serializers

from api.files.serializers.model import FileModelSerializer


class AwsPresignedPostSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    fields = serializers.DictField(child=serializers.CharField(), required=True)


class PresignedPostSerializer:
    presignedPost = AwsPresignedPostSerializer(required=True)
    file = FileModelSerializer(required=True)

    def __init__(self, presigned_post, file):
        self.data = {
            'presignedPost': AwsPresignedPostSerializer({
                'url': presigned_post['url'],
                'fields': presigned_post['fields']
            }).data,
            'file': FileModelSerializer(file).data
        }
