import time
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

PROCESS_TIME_HEADER = "X-Process-Time-Ms"


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Add server-side processing time (ms) as a response header.

    Visible in Swagger UI's response headers when using "Try it out", so the
    server-measured duration can be checked alongside the client-side timing.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        response.headers[PROCESS_TIME_HEADER] = f"{elapsed_ms:.1f}"
        return response
