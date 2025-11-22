from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    TEST_DATABASE_URL: PostgresDsn
    AUTH_JWT_SECRET_KEY: str
    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file='.env',
        env_file_encoding='utf-8',

    )

config = Config()

