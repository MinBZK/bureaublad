<<<<<<< HEAD:backend/app/middleware/logging.py
import logging
import typing
=======
import json
import logging
import typing
from time import time
>>>>>>> d47f213 (🎨(structure) restructure backend code):backend/bureaublad_api/middleware/logging.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
<<<<<<< HEAD:backend/app/middleware/logging.py
=======
from starlette.types import ASGIApp
from ulid import ULID

from bureaublad_api.context import set_request_id
from bureaublad_api.utils.mask import Mask

RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]
>>>>>>> d47f213 (🎨(structure) restructure backend code):backend/bureaublad_api/middleware/logging.py

logger = logging.getLogger(__name__)


<<<<<<< HEAD:backend/app/middleware/logging.py
RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        logger.debug(f"Request: {request.method} {request.url} - Response: {response.status_code}")
=======
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all HTTP requests and responses with request IDs.

    Features:
    - Generates ULID for each request (sortable, timestamp-based)
    - Masks sensitive data in headers (passwords, secrets, cookies, authorization)
    - Logs request/response details with timing
    - Adds X-API-Request-ID header to responses
    """

    def __init__(self, app: ASGIApp, mask_keywords: list[str] | None = None) -> None:
        super().__init__(app)
        default_keywords = ["cookie", "authorization", "token"]
        self.masker = Mask(mask_keywords=default_keywords + (mask_keywords or []))

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_time = time()

        # Always generate ULID for this service (sortable, timestamp-based)
        request_id: str = str(ULID())
        request.state.request_id = request_id

        # Set request_id in context so all loggers can access it
        set_request_id(request_id)

        response = await call_next(request)
        response_time = time()

        response.headers["X-API-Request-ID"] = request_id

        logging_body = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round((response_time - request_time) * 1000, 2),
        }

        if request.query_params:
            logging_body["query_params"] = str(request.query_params)

        # Check for incoming correlation ID from upstream (load balancer, API gateway, etc.)
        incoming_request_id = request.headers.get("X-Request-ID")
        if incoming_request_id:
            logging_body["X-Request-ID"] = incoming_request_id

        logger.info(json.dumps(logging_body))
>>>>>>> d47f213 (🎨(structure) restructure backend code):backend/bureaublad_api/middleware/logging.py
        return response
