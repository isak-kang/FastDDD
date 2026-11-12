"""Shared test setup.

Tests never touch real infrastructure or external services — no database,
cache, object storage or external API. ``_no_network`` (autouse) makes every
TCP connect fail loudly, so a test that would reach any of those errors
instead of quietly calling it.

API tests use ``TestClient(create_app())`` without ``with``: TestClient only
runs the lifespan when used as a context manager, so no external client is
connected. Replace the dependencies a route needs with
``app.dependency_overrides`` and in-memory fakes (shared fakes go in
``tests/fakes.py``).
"""

import pytest

from tests.network_guard import refuse_network


@pytest.fixture(autouse=True)
def _no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    refuse_network(monkeypatch)
