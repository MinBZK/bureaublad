import logging
from collections.abc import Callable
from typing import Any

import httpx
from app.core.translate import _
from app.exceptions import ExternalServiceError
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """Base client for all external API services."""

    service_name: str

    def __init__(self, http_client: httpx.AsyncClient, base_url: str, token: str) -> None:
        self.client = http_client
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _build_url(self, path: str) -> str:
        """Build full URL from base and path."""
        return f"{self.base_url}/{path.lstrip('/')}"

    def _auth_headers(self) -> dict[str, str]:
        """Generate authentication headers."""
        return {"Authorization": f"Bearer {self.token}"}

    async def _get_resource_with_headers[T](
        self,
        path: str,
        model_type: type[T],
        params: dict[str, Any] | None = None,
        response_parser: Callable[[dict[str, Any]], Any] | None = None,
    ) -> tuple[T, dict[str, str]]:
        """Get resource and return both data and response headers."""
        try:
            url = self._build_url(path)
            response = await self.client.get(
                url,
                params=params or {},
                headers=self._auth_headers(),
            )

            if response.status_code != 200:
                raise ExternalServiceError(
                    self.service_name, _(f"Failed to fetch {path} (status {response.status_code})")
                )

            json_data = response.json()
            data = response_parser(json_data) if response_parser else json_data
            validated = TypeAdapter(model_type).validate_python(data)
            return validated, dict(response.headers)

        except httpx.HTTPError as e:
            logger.exception(f"HTTP error calling {self.service_name} API")
            raise ExternalServiceError(self.service_name, f"HTTP error: {e}") from e

    async def _get_resource[T](
        self,
        path: str,
        model_type: type[T],
        params: dict[str, Any] | None = None,
        response_parser: Callable[[dict[str, Any]], Any] | None = None,
    ) -> T:
        data, _ = await self._get_resource_with_headers(path, model_type, params, response_parser)
        return data
