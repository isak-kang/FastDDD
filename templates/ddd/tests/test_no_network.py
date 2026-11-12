import asyncio
import socket

import httpx
import pytest

from tests.network_guard import NetworkAccessError


@pytest.mark.unit
def test_asyncio_internal_socketpair_is_allowed() -> None:
    async def run() -> int:
        await asyncio.sleep(0)
        return 42

    assert asyncio.run(run()) == 42


@pytest.mark.unit
def test_connect_ex_is_still_refused() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        with pytest.raises(NetworkAccessError):
            sock.connect_ex(("127.0.0.1", 5432))


@pytest.mark.unit
@pytest.mark.parametrize("address", [("127.0.0.1", 5432), ("localhost", 6379), ("10.0.0.1", 9001)])
def test_tests_cannot_open_tcp_connections(address) -> None:
    """Local infra and external services alike are unreachable from tests."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        with pytest.raises(NetworkAccessError):
            sock.connect(address)


@pytest.mark.unit
def test_a_real_http_client_is_refused_too() -> None:
    with pytest.raises((NetworkAccessError, httpx.ConnectError)) as info:
        httpx.get("http://127.0.0.1:9/", timeout=1)
    # httpx may wrap the socket error; the guard must be what stopped it.
    assert "tests must not open network connections" in str(info.value)
