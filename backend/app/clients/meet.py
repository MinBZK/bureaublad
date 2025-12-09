"""Meet service client for meeting management."""

import logging
from typing import Any

from app.clients.base import BaseAPIClient
from app.core.translate import _
from app.exceptions import ExternalServiceError
from app.models.pagination import PaginatedResponse
from app.models.room import Room
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class MeetClient(BaseAPIClient):
    """Client for Meet service API."""

    service_name = "Meet"

    async def get_rooms(
        self, path: str = "api/v1.0/rooms/", page: int = 1, page_size: int = 5
    ) -> PaginatedResponse[Room]:
        """Fetch meetings from Meet service.

        Args:
            path: API endpoint path
            page: Page number for pagination

        Returns:
            List of Meeting objects
        """
        page = max(1, page)
        page_size = max(1, page_size)

        params: dict[str, Any] = {}

        rooms = await self._get_resource(
            path=path,
            model_type=PaginatedResponse[Room],
            params=params,
            response_parser=lambda data: {"count": data.get("count", 0), "results": data.get("results", [])},
        )

        # honor pagination from Page and page_size params
        start = (page - 1) * page_size
        end = start + page_size
        rooms.results = rooms.results[start:end]

        return rooms

    async def post_room(self, name: str, path: str = "api/v1.0/rooms/") -> Room:
        url = self._build_url(path)
        response = await self.client.post(
            url,
            json={"name": name},
            headers=self._auth_headers(),
        )

        if response.status_code != 201:
            raise ExternalServiceError("Meet", _(f"Failed to create room (status {response.status_code})"))

        result = response.json()
        room: Room = TypeAdapter(Room).validate_python(result)
        return room
