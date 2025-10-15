import logging
from typing import Any

import httpx
from app.models.document import Document
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class DriveClient:
    def __init__(self, http_client: httpx.AsyncClient, base_url: str, token: str) -> None:
        self.client = http_client
        self.base_url = base_url.rstrip("/")
        self.token = token

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
        params: dict[str, Any] = {"page": page, "page_size": page_size, "ordering": ordering}

        if title:
            params["title"] = title
        if is_creator_me:
            params["is_creator_me"] = str(is_creator_me)
        if is_favorite:
            params["is_favorite"] = str(is_favorite)

        url = f"{self.base_url}/{path.lstrip('/')}"

        response = await self.client.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        if response.status_code != 200:
            return TypeAdapter(list[Document]).validate_python([])

        results = response.json().get("results", [])

        if len(results) < 1:
            return TypeAdapter(list[Document]).validate_python([])

        workspace_id = results[0]["id"]

        item_path = f"api/v1.0/items/{workspace_id}/children/"
        item_url = f"{self.base_url}/{item_path.lstrip('/')}"
        response = await self.client.get(
            item_url,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if response.status_code != 200:
            return TypeAdapter(list[Document]).validate_python([])

        results = response.json().get("results", [])
        documents: list[Document] = TypeAdapter(list[Document]).validate_python(results)

        return documents
