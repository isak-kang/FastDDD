from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.shared.exceptions.base import BaseAppException
from app.shared.exceptions.error_code import ErrorCode
from app.shared.logging.logger import get_logger
from app.shared.response.api_response import ApiResponse

logger = get_logger(__name__)


async def app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
    if exc.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error("Application error on %s %s: %s", request.method, request.url.path, exc.message)
    else:
        logger.warning("Application error on %s %s: %s", request.method, request.url.path, exc.message)

    response = ApiResponse.fail(status=exc.status_code, code=exc.code, message=exc.message)
    return JSONResponse(status_code=exc.status_code, content=response.to_dict())


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("Validation error on %s %s: %s", request.method, request.url.path, exc.errors())

    response = ApiResponse.fail(
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code=ErrorCode.VALIDATION_ERROR.value,
        message="Request validation failed.",
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.to_dict(),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)

    response = ApiResponse.fail(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code=ErrorCode.INTERNAL_SERVER_ERROR.value,
        message="Internal server error.",
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.to_dict(),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BaseAppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
