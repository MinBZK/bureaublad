import json
import logging
import typing
from time import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.utils.mask import Mask

RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all HTTP requests and responses.

    Responsibilities:
    - Logs request method, path, and query parameters
    - Logs response status code and request duration
    - Masks sensitive data in headers (passwords, secrets, cookies, authorization)

    Note: Request ID must be set by RequestIDMiddleware before this middleware runs.
    """

    def __init__(self, app: ASGIApp, mask_keywords: list[str] | None = None) -> None:
        super().__init__(app)
        default_keywords = ["cookie", "authorization", "token"]
        self.masker = Mask(mask_keywords=default_keywords + (mask_keywords or []))

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_time = time()

        response = await call_next(request)
        response_time = time()

        logging_body = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round((response_time - request_time) * 1000, 2),
        }

        if request.query_params:
            logging_body["query_params"] = str(request.query_params)

        logger.info(json.dumps(logging_body))
        return response
