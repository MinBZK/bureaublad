"""Meet service client for meeting management."""

import logging
from typing import Any

import httpx
from app.exceptions import ExternalServiceError
from app.models.room import Room
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

    async def get_rooms(self, path: str = "api/v1.0/rooms/", page: int | None = 1) -> list[Room]:
        """Fetch meetings from Meet service.

        Args:
            path: API endpoint path
            page: Page number for pagination

        Returns:
            List of Meeting objects
        """
        if page is None or page < 1:
            page = 1

        params: dict[str, Any] = {"page": page}

        url = f"{self.base_url}/{path.lstrip('/')}"
        response = await self.client.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if response.status_code != 200:
            return TypeAdapter(list[Room]).validate_python([])

        results = response.json().get("results", [])
        rooms: list[Room] = TypeAdapter(list[Room]).validate_python(results)

        return rooms

    async def post_room(self, name: str, path: str = "api/v1.0/rooms/") -> Room:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = await self.client.post(
            url,
            json={"name": name},
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if response.status_code != 201:
            raise ExternalServiceError("Meet", f"Failed to create room (status {response.status_code})")

        result = response.json()
        room: Room = TypeAdapter(Room).validate_python(result)
        return room
