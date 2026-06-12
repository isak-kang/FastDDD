from app.shared.exceptions.base import BaseAppException
from app.shared.exceptions.domains.chat.error_code import ChatErrorCode


class ChatError(BaseAppException):
    def __init__(
        self,
        error_code: ChatErrorCode,
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
