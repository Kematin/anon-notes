from pathlib import Path
from typing import List, Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_model_config(env_dir: str = f"{BASE_DIR}/.env"):
    config = SettingsConfigDict(
        env_file=env_dir, env_file_encoding="utf-8", extra="ignore"
    )
    return config


class MiscSettings(BaseSettings):
    delete_time: int = Field(alias="DELETE_TIME")

    model_config = get_model_config()


class DBSettings(BaseSettings):
    host: str = Field(alias="DB_HOST")
    port: str = Field(alias="DB_PORT")
    name: str = Field(alias="DB_NAME", default="notes")
    test_db_name: str = Field(alias="DB_TEST_NAME", default="test_db")

    model_config = get_model_config()


class Settings(BaseSettings):
    debug: bool = Field(alias="DEBUG", default=True)
    host: str = Field(alias="API_HOST", default="localhost")
    port: int = Field(alias="API_PORT", default=8000)
    secret: SecretStr = Field(alias="SECRET_KEY")

    origins: List[str] = Field(alias="API_ORIGINS")

    _db: Optional[DBSettings] = None
    _misc: Optional[MiscSettings] = None

    model_config = get_model_config()

    @property
    def db(self) -> DBSettings:
        if self._db is None:
            self._db = DBSettings()
        return self._db

    @property
    def misc(self) -> MiscSettings:
        if self._misc is None:
            self._misc = MiscSettings()
        return self._misc

    model_config = get_model_config()


CONFIG = Settings()
