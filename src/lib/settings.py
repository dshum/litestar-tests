from pathlib import Path

from pydantic_settings import BaseSettings

__all__ = [
    "BASE_DIR",
    "app",
    "jwt",
    "db",
    "sentry",
    "mail",
]

BASE_DIR = Path(__file__).resolve().parent.parent


class AppSettings(BaseSettings):
    class Config:
        case_sensitive = True

    APP_NAME: str = "Tests"
    SECRET_KEY: str = "fake_secret_key"
    BUILD_NUMBER: str = "0"
    DEBUG: bool = False
    ENVIRONMENT: str = "local"
    LOG_LEVEL: str = "INFO"


class JWTSettings(BaseSettings):
    class Config:
        env_prefix = "JWT_"
        case_sensitive = True

    TTL: int = 1440
    SECRET: str


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "DATABASE_"
        case_sensitive = True

    URL: str
    ECHO: bool = False


class SentrySettings(BaseSettings):
    class Config:
        env_prefix = "SENTRY_"
        case_sensitive = True

    DSN: str = ""
    ENABLE: bool = False
    TRACES_SAMPLE_RATE: float = 0.0


class MailSettings(BaseSettings):
    class Config:
        env_prefix = "MAIL_"
        case_sensitive = True

    HOST: str
    PORT: int = 465
    USERNAME: str
    PASSWORD: str
    ENCRYPTION: str = "SSL"


app = AppSettings.model_validate({})
jwt = JWTSettings.model_validate({})
db = DatabaseSettings.model_validate({})
sentry = SentrySettings.model_validate({})
mail = MailSettings.model_validate({})
