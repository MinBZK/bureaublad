import typing

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from ulid import ULID

from app.context import set_request_id
from app.utils.request_id import validate_request_id

RequestResponseEndpoint = typing.Callable[[Request], typing.Awaitable[Response]]


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to manage request IDs for distributed tracing.

    Responsibilities:
    - Extracts and validates X-Request-ID from incoming requests
    - Generates ULID if X-Request-ID is missing or invalid
    - Sets request ID in context for access by other components
    - Adds X-Request-ID header to all responses

    This middleware should run before other middlewares that need the request ID.
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        incoming_request_id = request.headers.get("X-Request-ID")
        validated_request_id = validate_request_id(incoming_request_id)

        request_id: str = validated_request_id or str(ULID())
        request.state.request_id = request_id

        set_request_id(request_id)

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        return response
