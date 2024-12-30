from typing import List

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_model_config(env_dir: str = "../.env"):
    config = SettingsConfigDict(
        env_file=env_dir, env_file_encoding="utf-8", extra="ignore"
    )
    return config


class DBSettings(BaseSettings):
    host: str = Field(alias="DB_HOST")
    port: str = Field(alias="DB_PORT")
    name: str = Field(alias="DB_NAME")

    model_config = get_model_config()


class Settings(BaseSettings):
    debug: bool = Field(alias="DEBUG", default=True)
    host: str = Field(alias="API_HOST", default="localhost")
    port: int = Field(alias="API_PORT", default=8000)
    secret: SecretStr = Field(alias="SECRET_KEY")

    origins: List[str] = Field(alias="API_ORIGINS")

    db: DBSettings = DBSettings()

    model_config = get_model_config()


config = Settings()
