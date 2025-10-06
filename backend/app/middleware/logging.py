import logging
import typing

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        logger.debug(f"Request: {request.method} {request.url} - Response: {response.status_code}")
        return response
