"""Docs service client for document management."""

import logging
from typing import Any

import httpx
from app.exceptions import ExternalServiceError
from app.models.note import Note
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class DocsClient:
    def __init__(self, http_client: httpx.AsyncClient, base_url: str, token: str) -> None:
        self.client = http_client
        self.base_url = base_url.rstrip("/")
        self.token = token

    async def get_documents(
        self,
        path: str = "api/v1.0/documents/",
        page: int = 1,
        page_size: int = 5,
        title: str | None = None,
        is_favorite: bool = False,
        is_creator_me: bool = False,
        ordering: str = "-updated_at",
    ) -> list[Note]:
        params: dict[str, Any] = {"page": page, "page_size": page_size, "ordering": ordering}

        if title:
            params["title"] = title

        if is_favorite:
            params["is_favorite"] = str(is_favorite)

        if is_creator_me:
            params["is_creator_me"] = str(is_creator_me)

        url = f"{self.base_url}/{path.lstrip('/')}"
        response = await self.client.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if response.status_code != 200:
            return TypeAdapter(list[Note]).validate_python([])

        results = response.json().get("results", [])
        notes: list[Note] = TypeAdapter(list[Note]).validate_python(results)

        return notes

    async def post_document(self, path: str = "api/v1.0/documents/") -> Note:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = await self.client.post(
            url,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if response.status_code != 201:
            raise ExternalServiceError("Docs", f"Failed to create document (status {response.status_code})")

        result = response.json()
        note: Note = TypeAdapter(Note).validate_python(result)
        return note
