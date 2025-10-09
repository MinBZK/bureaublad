import logging
from typing import Annotated

import httpx
from fastapi import Depends

from app.context import get_request_id

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 2.0
DEFAULT_MAX_RETRIES = 2


async def add_request_id_header(request: httpx.Request) -> None:
    """
    Event hook to automatically add X-Request-ID header to outgoing requests.

    This enables distributed tracing by propagating the request ID from the
    incoming request to all downstream services.
    """
    request_id = get_request_id()
    if request_id:
        request.headers["X-Request-ID"] = request_id


class HTTPClientDependency:
    """Reusable httpx.AsyncClient dependency for FastAPI.

    Creates a single httpx.AsyncClient on first use and reuses it for all
    subsequent requests. This enables proper HTTP connection pooling and
    improves performance.

    Automatically propagates X-Request-ID header to all outgoing requests
    for distributed tracing.
    """

    def __init__(
        self,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self.http_client: httpx.AsyncClient | None = None

    async def __call__(self) -> httpx.AsyncClient:
        """Return the cached httpx.AsyncClient, creating it if needed."""
        if not self.http_client:
            transport = httpx.AsyncHTTPTransport(retries=self.max_retries)

            self.http_client = httpx.AsyncClient(
                timeout=self.timeout,
                transport=transport,
                follow_redirects=True,
                event_hooks={"request": [add_request_id_header]},
            )
            logger.info("Created shared HTTP client")

        return self.http_client

    async def aclose(self) -> None:
        """Close the httpx.AsyncClient."""
        if self.http_client:
            await self.http_client.aclose()
            logger.info("Closed HTTP client")
            self.http_client = None


# Single shared HTTP client for the entire application
http_client_dependency = HTTPClientDependency()

# Type alias for dependency injection
HTTPClient = Annotated[httpx.AsyncClient, Depends(http_client_dependency)]
