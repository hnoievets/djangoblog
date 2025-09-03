import boto3
from botocore.exceptions import ClientError
import logging

from api.utils.config import ConfigService


class MailerService:
    _ses = None
    from_email = ConfigService.get_env('AWS_SES_FROM_EMAIL')
    logger = logging.getLogger(__name__)

    @classmethod
    def _get_client(cls):
        if cls._ses is None:
            cls._ses = boto3.client(
                'ses',
                aws_access_key_id=ConfigService.get_env('AWS_SES_ACCESS_KEY'),
                aws_secret_access_key=ConfigService.get_env('AWS_SES_KEY_SECRET'),
                region_name=ConfigService.get_env('AWS_SES_REGION')
            )

        return cls._ses

    @classmethod
    def send_email(
        cls,
        to_email: str,
        subject: str,
        body_html: str,
    ):
        try:
            cls._get_client().send_email(
                Source=cls.from_email,
                Destination={
                    'ToAddresses': [to_email],
                },
                Message={
                    'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                    'Body': {
                        'Html': {'Data': body_html, 'Charset': 'UTF-8'},
                    }
                }
            )

        except ClientError as e:
            cls.logger.error(f"SES failed: {e.response['Error']['Message']}")