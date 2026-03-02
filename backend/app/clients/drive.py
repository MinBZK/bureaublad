import logging
from typing import Any

from app.clients.base import BaseAPIClient
from app.models.document import Document
from app.models.pagination import PaginatedResponse

logger = logging.getLogger(__name__)


class DriveClient(BaseAPIClient):
    service_name = "Drive"

    async def get_documents(
        self,
        page: int = 1,
        page_size: int = 5,
        title: str | None = None,
    ) -> PaginatedResponse[Document]:
        page = max(1, page)
        page_size = max(1, page_size)

        params: dict[str, Any] = {"page": page, "page_size": page_size}

        if title:
            params["title"] = title

        try:
            return await self._get_resource(
                path="api/v1.0/items/recents/",
                model_type=PaginatedResponse[Document],
                params=params,
                response_parser=lambda data: {"count": data.get("count", 0), "results": data.get("results", [])},
            )
        except Exception:
            logger.exception(f"Error fetching documents from {self.service_name}")
            return PaginatedResponse[Document](count=0, results=[])
