from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from app.shared.exceptions.error_code import ErrorCode

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    status: int
    code: str
    message: str
    data: T | None = None

    @classmethod
    def success(
        cls,
        data: T,
        status: int = 200,
        code: str = ErrorCode.COMMON_SUCCESS.value,
        message: str = "",
    ) -> "ApiResponse[T]":
        return cls(status=status, code=code, message=message, data=data)

    @classmethod
    def ok(cls, data: T | None = None) -> "ApiResponse[T]":
        return cls(status=200, code=ErrorCode.COMMON_SUCCESS.value, message="", data=data)

    @classmethod
    def no_content(
        cls,
        status: int = 204,
        code: str = ErrorCode.COMMON_NO_CONTENT.value,
        message: str = "",
    ) -> "ApiResponse[None]":
        return cls(status=status, code=code, message=message)

    @classmethod
    def request_error(
        cls,
        status: int = 400,
        code: str = ErrorCode.COMMON_REQUEST_ERROR.value,
        message: str = "",
    ) -> "ApiResponse[None]":
        return cls(status=status, code=code, message=message)

    @classmethod
    def server_error(
        cls,
        status: int = 500,
        code: str = ErrorCode.COMMON_INTERNAL_SERVER_ERROR.value,
        message: str = "",
    ) -> "ApiResponse[None]":
        return cls(status=status, code=code, message=message)

    @classmethod
    def fail(
        cls,
        status: int,
        code: str,
        message: str,
    ) -> "ApiResponse[None]":
        return cls(status=status, code=code, message=message)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)
