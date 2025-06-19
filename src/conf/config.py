from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 35
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    MAIL_SMTP_USERNAME: str
    MAIL_SMTP_PASSWORD: str
    MAIL_SMTP_FROM: str
    MAIL_SMTP_SERVER: str
    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


config = Settings()
