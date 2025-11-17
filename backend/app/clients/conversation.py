"""Meet service client for meeting management."""

import logging

from app.clients.base import BaseAPIClient
from app.models.conversation import Conversation
from app.models.pagination import PaginatedResponse

logger = logging.getLogger(__name__)


class ConversationClient(BaseAPIClient):
    """Client for Conversation service API."""

    service_name = "Conversations"

    async def get_chats(
        self,
        path: str = "api/v1.0/chats/",
        page: int = 1,
        page_size: int = 5,
        ordering: str = "-updated_at",
    ) -> PaginatedResponse[Conversation]:
        """Fetch chats from conversation service.

        Args:
            path: API endpoint path
            page: Page number for pagination
            title: Optional title filter
            favorite: Whether to filter for favorites only

        Returns:
            List of chats objects
        """
        page = max(1, page)
        page_size = max(1, page_size)
        params: dict[str, int | str] = {"page": page, "page_size": page_size, "ordering": ordering}

        chats = await self._get_resource(
            path=path,
            model_type=PaginatedResponse[Conversation],
            params=params,
            response_parser=lambda data: {"count": data.get("count", 0), "results": data.get("results", [])},
        )
        return chats
