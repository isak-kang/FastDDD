from app.config.components.base import BaseConfig
from app.config.shared.environment import Environment


class AppConfig(BaseConfig):
    app_name: str = "FastAPI DDD Template"
    app_env: Environment = Environment.LOCAL
    debug: bool = False
