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
        path: str = "api/v1.0/items/",
        page: int = 1,
        page_size: int = 5,
        ordering: str = "-updated_at",
        title: str | None = None,
        is_creator_me: bool = False,
        is_favorite: bool = False,
    ) -> PaginatedResponse[Document]:
        # NOTE: Documents in Drive can be nested. Currently, we do not support retrieving all
        # documents in a sensible manner. The current implementation get's the documents in
        # the (arbitrary) first workspace it encounters. This needs to be refactored so such that
        # this endpoint returns all documents.

        page = max(1, page)
        page_size = max(1, page_size)

        params: dict[str, Any] = {"page": page, "page_size": page_size, "ordering": ordering}

        if title:
            params["title"] = title
        if is_creator_me:
            params["is_creator_me"] = str(is_creator_me)
        if is_favorite:
            params["is_favorite"] = str(is_favorite)

        try:
            result = await self._get_resource(
                path=path,
                model_type=PaginatedResponse[Document],
                params=params,
                response_parser=lambda data: {"count": data.get("count", 0), "results": data.get("results", [])},
            )

            if len(result.results) < 1:
                return PaginatedResponse[Document](count=0, results=[])

            workspace_id = result.results[0].id
            item_path = f"api/v1.0/items/{workspace_id}/children/"
            return await self._get_resource(
                path=item_path,
                model_type=PaginatedResponse[Document],
                params=params,
                response_parser=lambda data: {"count": data.get("count", 0), "results": data.get("results", [])},
            )
        except Exception:
            logger.exception(f"Error fetching documents from {self.service_name}")
            return PaginatedResponse[Document](count=0, results=[])
