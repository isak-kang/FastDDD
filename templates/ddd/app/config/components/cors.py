from app.config.components.base import BaseConfig


class CorsConfig(BaseConfig):
    """Browser origins allowed to call this API.

    Comma-separated so the whole list lives in one environment variable, e.g.
    ``CORS_ALLOW_ORIGINS=http://localhost:3000,https://app.example.com``.
    Empty (the default) disables CORS entirely — nothing cross-origin is
    allowed unless an origin is named.
    """

    cors_allow_origins: str = ""

    @property
    def allow_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]

    @property
    def is_active(self) -> bool:
        return bool(self.allow_origins)
