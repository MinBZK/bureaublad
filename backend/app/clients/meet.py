"""Meet service client for meeting management."""

import logging
from typing import Any

import httpx
from app.models.meeting import Meeting
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class MeetClient:
    """Client for Meet service API.

    Handles business logic for fetching and managing meetings.
    """

    def __init__(self, http_client: httpx.AsyncClient, base_url: str, token: str) -> None:
        """Initialize MeetClient.

        Args:
            http_client: Shared httpx.AsyncClient instance
            base_url: Base URL for the Meet service
            token: Authentication token for this request
        """
        self.client = http_client
        self.base_url = base_url.rstrip("/")
        self.token = token

    async def get_meetings(
        self,
        path: str = "api/v1.0/documents/",
        page: int = 1,
        title: str | None = None,
        favorite: bool = False,
    ) -> list[Meeting]:
        """Fetch meetings from Meet service.

        Args:
            path: API endpoint path
            page: Page number for pagination
            title: Optional title filter
            favorite: Whether to filter for favorites only

        Returns:
            List of Meeting objects
        """
        params: dict[str, Any] = {"page": page}
        if title:
            params["title"] = title
        if favorite:
            params["favorite"] = str(favorite)

        url = f"{self.base_url}/{path.lstrip('/')}"
        response = await self.client.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if response.status_code != 200:
            return TypeAdapter(list[Meeting]).validate_python([])

        results = response.json().get("results", [])
        meetings: list[Meeting] = TypeAdapter(list[Meeting]).validate_python(results)

        return meetings
