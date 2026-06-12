from functools import lru_cache

from app.config.components.app import AppConfig
from app.config.components.base import BaseConfig
from app.config.components.logging import LoggingConfig


class Settings(BaseConfig):
    app: AppConfig
    logging: LoggingConfig


@lru_cache
def get_settings() -> Settings:
    return Settings(app=AppConfig(), logging=LoggingConfig())
