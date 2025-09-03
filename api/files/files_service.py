from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
import logging

from api.files import File
from api.utils.config import ConfigService


class FileService:
    _s3 = None
    bucket_name = ConfigService.get_env('AWS_S3_BUCKET_NAME')

    logger = logging.getLogger(__name__)

    @classmethod
    def _get_client(cls):
        if cls._s3 is None:
            cls._s3 = boto3.client(
                's3',
                region_name=ConfigService.get_env('AWS_S3_REGION'),
                aws_access_key_id=ConfigService.get_env('AWS_S3_ACCESS_KEY'),
                aws_secret_access_key=ConfigService.get_env('AWS_S3_SECRET_KEY'),
            )

        return cls._s3

    @classmethod
    def generate_presigned_post(
        cls,
        key: str,
        content_type: str
    ):
        content_type_condition = {
            'Content-Type': content_type,
        }

        try:
            return cls._get_client().generate_presigned_post(
                Bucket=cls.bucket_name,
                Key=key,
                Conditions=[content_type_condition],
                Fields=content_type_condition,
            )
        except ClientError as e:
            cls.logger.error(f"S3 failed: {e.response['Error']['Message']}")

            return None

    @classmethod
    def generate_file_key(cls, user_id: int) -> str:
        return f"files/user_{user_id}/{uuid4()}"

    @classmethod
    def delete(cls, id: int):
        file = File.objects.get(pk=id)

        cls._get_client().delete_object(
            Bucket=cls.bucket_name,
            Key=file.file_key
        )

        file.delete()

        return
