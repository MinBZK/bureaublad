"""Meet service client for meeting management."""

import logging
from typing import Any

import httpx
from app.models.conversation import Conversation
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class ConversationClient:
    """Client for Conversation service API.

    Handles business logic for fetching and managing conversations.
    """

    def __init__(self, http_client: httpx.AsyncClient, base_url: str, token: str) -> None:
        """Initialize ConversationClient.

        Args:
            http_client: Shared httpx.AsyncClient instance
            base_url: Base URL for the conversations service
            token: Authentication token for this request
        """
        self.client = http_client
        self.base_url = base_url.rstrip("/")
        self.token = token

    async def get_chats(
        self,
        path: str = "api/v1.0/chats/",
        page: int | None = 1,
    ) -> list[Conversation]:
        """Fetch chats from conversation service.

        Args:
            path: API endpoint path
            page: Page number for pagination
            title: Optional title filter
            favorite: Whether to filter for favorites only

        Returns:
            List of chats objects
        """
        params: dict[str, Any] = {"page": page}

        url = f"{self.base_url}/{path.lstrip('/')}"
        response = await self.client.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        print(response)

        if response.status_code != 200:
            return TypeAdapter(list[Conversation]).validate_python([])

        results = response.json().get("results", [])
        chats: list[Conversation] = TypeAdapter(list[Conversation]).validate_python(results)

        return chats
