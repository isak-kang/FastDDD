"""Shared exception handling utilities."""

from app.shared.exceptions.base import AppException, BaseAppException
from app.shared.exceptions.error_code import ErrorCode

__all__ = [
    "AppException",
    "BaseAppException",
    "ErrorCode",
]
