from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis import Redis

BASE_DIR = Path(__file__).resolve().parent.parent


def get_model_config(env_dir: str = f"{BASE_DIR}/.env"):
    config = SettingsConfigDict(
        env_file=env_dir, env_file_encoding="utf-8", extra="ignore"
    )
    return config


class MiscSettings(BaseSettings):
    # In minutes
    delete_time: int = Field(alias="DELETE_TIME")

    model_config = get_model_config()


class CelerySettings(BaseSettings):
    host: str = Field(alias="CELERY_HOST", default="localhost")
    port: str = Field(alias="CELERY_PORT", default=6379)

    _redis: Redis = None

    @property
    def redis(self) -> Redis:
        if self._redis is None:
            self._redis = Redis(host=self.host, port=self.port, decode_responses=True)
        return self._redis

    @property
    def url(self) -> str:
        url = f"redis://{self.host}:{self.port}"
        return url

    model_config = get_model_config()


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

    _db: DBSettings = None
    _celery: CelerySettings = None
    _misc: MiscSettings = None

    model_config = get_model_config()

    @property
    def db(self) -> DBSettings:
        if self._db is None:
            self._db = DBSettings()
        return self._db

    @property
    def celery(self) -> CelerySettings:
        if self._celery is None:
            self._celery = CelerySettings()
        return self._celery

    @property
    def misc(self) -> MiscSettings:
        if self._misc is None:
            self._misc = MiscSettings()
        return self._misc

    model_config = get_model_config()


@lru_cache()
def get_config():
    return Settings()
