from api.utils.config import ConfigService
from api.utils.mailer import MailerService


class UserService:
    @staticmethod
    def send_verification_email(email: str, token: str):
        frontend_url = ConfigService.get_env('FRONTEND_URL')

        MailerService.send_email(
            email,
            'Verify your email',
            f"<p>Verification link: <a href=\"{frontend_url}/verifying?token={token}\">Click here</a></p>"
        )
