from enum import Enum


def _resolve_error_code(code: str | Enum) -> str:
    if isinstance(code, str):
        return code

    value = code.value
    if isinstance(value, tuple):
        return str(value[1])

    return str(value)


class BaseAppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
        detail: object | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class AppException(BaseAppException):
    def __init__(
        self,
        code: str | Enum,
        message: str,
        status_code: int = 400,
        detail: object | None = None,
    ) -> None:
        super().__init__(code=_resolve_error_code(code), message=message, status_code=status_code, detail=detail)
