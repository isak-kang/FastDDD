"""Refusing network access from tests (see tests/conftest.py)."""

import socket
import sys

import pytest

_INET_FAMILIES = (socket.AF_INET, socket.AF_INET6)

_SOCKETPAIR_CODE = getattr(getattr(socket, "_fallback_socketpair", None), "__code__", None)


class NetworkAccessError(RuntimeError):
    """A test tried to open a network connection."""


def refuse_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make every TCP connect fail, localhost included: locally that is exactly
    where databases, caches and object storage listen."""
    real_connect, real_connect_ex = socket.socket.connect, socket.socket.connect_ex

    def refuse(address: object) -> None:
        raise NetworkAccessError(
            f"tests must not open network connections (tried {address!r}); use fakes and dependency_overrides"
        )

    def connect(self: socket.socket, address: object) -> None:
        # Windows asyncio needs the stdlib's private loopback socket pair.
        # Ordinary localhost connections must still be refused.
        internal_socketpair = _SOCKETPAIR_CODE is not None and sys._getframe(1).f_code is _SOCKETPAIR_CODE
        if self.family in _INET_FAMILIES and not internal_socketpair:
            refuse(address)
        return real_connect(self, address)

    def connect_ex(self: socket.socket, address: object) -> int:
        if self.family in _INET_FAMILIES:
            refuse(address)
        return real_connect_ex(self, address)

    monkeypatch.setattr(socket.socket, "connect", connect)
    monkeypatch.setattr(socket.socket, "connect_ex", connect_ex)
