from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    DATABASE_URL: PostgresDsn 

    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env', env_file_encoding='utf-8')

config = Config()

