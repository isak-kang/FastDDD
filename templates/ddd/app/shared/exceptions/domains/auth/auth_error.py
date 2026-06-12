from app.shared.exceptions.base import BaseAppException
from app.shared.exceptions.domains.auth.error_code import AuthErrorCode


class AuthError(BaseAppException):
    def __init__(
        self,
        error_code: AuthErrorCode,
        message: str | None = None,
        detail: object | None = None,
    ) -> None:
        status_code, code, default_message = error_code.value
        super().__init__(
            code=code,
            message=message or default_message,
            status_code=status_code,
            detail=detail,
        )
