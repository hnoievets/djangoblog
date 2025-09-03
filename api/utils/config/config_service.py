import os


class ConfigService:
    @staticmethod
    def get_env(key: str) -> str:
        return os.getenv(key)
