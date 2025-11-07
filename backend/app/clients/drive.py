import logging
from typing import Any

from app.clients.base import BaseAPIClient
from app.models.document import Document
from pydantic import TypeAdapter

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
    ) -> list[Document]:
        page = max(1, page)
        page_size = max(1, page_size)

        params: dict[str, Any] = {"page": page, "page_size": page_size, "ordering": ordering}

        if title:
            params["title"] = title
        if is_creator_me:
            params["is_creator_me"] = str(is_creator_me)
        if is_favorite:
            params["is_favorite"] = str(is_favorite)

        url = self._build_url(path)

        response = await self.client.get(
            url,
            params=params,
            headers=self._auth_headers(),
        )
        if response.status_code != 200:
            return TypeAdapter(list[Document]).validate_python([])

        results = response.json().get("results", [])

        if len(results) < 1:
            return TypeAdapter(list[Document]).validate_python([])

        workspace_id = results[0]["id"]

        item_path = f"api/v1.0/items/{workspace_id}/children/"
        item_url = self._build_url(item_path)
        response = await self.client.get(
            item_url,
            headers=self._auth_headers(),
        )

        if response.status_code != 200:
            return TypeAdapter(list[Document]).validate_python([])

        results = response.json().get("results", [])
        documents: list[Document] = TypeAdapter(list[Document]).validate_python(results)

        return documents
