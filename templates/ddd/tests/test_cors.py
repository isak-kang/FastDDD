from collections.abc import Callable, Iterator

import pytest
from fastapi.testclient import TestClient

from app.config.components.cors import CorsConfig
from app.config.settings import get_settings
from main import create_app

ORIGIN = "http://localhost:3000"


@pytest.fixture
def cors_origins(monkeypatch: pytest.MonkeyPatch) -> Iterator[Callable[[str], None]]:
    """Set CORS_ALLOW_ORIGINS for one test; get_settings() is cached, so reset it around."""

    def set_origins(value: str) -> None:
        monkeypatch.setenv("CORS_ALLOW_ORIGINS", value)
        get_settings.cache_clear()

    yield set_origins
    get_settings.cache_clear()


@pytest.mark.unit
def test_allow_origins_splits_on_commas_and_drops_blanks() -> None:
    config = CorsConfig(cors_allow_origins=" http://a.test , ,http://b.test ")

    assert config.allow_origins == ["http://a.test", "http://b.test"]
    assert config.is_active


@pytest.mark.api
def test_configured_origin_is_allowed(cors_origins: Callable[[str], None]) -> None:
    cors_origins(ORIGIN)
    client = TestClient(create_app())

    response = client.options(
        "/api/health",
        headers={"Origin": ORIGIN, "Access-Control-Request-Method": "GET"},
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ORIGIN


@pytest.mark.api
def test_cors_is_off_when_no_origin_is_configured(cors_origins: Callable[[str], None]) -> None:
    cors_origins("")
    client = TestClient(create_app())

    response = client.get("/api/health", headers={"Origin": ORIGIN})

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers
