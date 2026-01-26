"""Docs service client for document management."""

import logging
from typing import Any

from app.clients.base import BaseAPIClient
from app.core.translate import _
from app.exceptions import ExternalServiceError
from app.models.note import Note
from app.models.pagination import PaginatedResponse
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class DocsClient(BaseAPIClient):
    service_name = "Docs"

    async def get_documents(
        self,
        path: str = "api/v1.0/documents/all/",
        page: int = 1,
        page_size: int = 5,
        title: str | None = None,
        is_favorite: bool = False,
        is_creator_me: bool = False,
        ordering: str = "-updated_at",
    ) -> PaginatedResponse[Note]:
        page = max(1, page)
        page_size = max(1, page_size)

        params: dict[str, Any] = {"page": page, "page_size": page_size, "ordering": ordering}

        if title:
            params["title"] = title

        if is_favorite:
            params["is_favorite"] = str(is_favorite)

        if is_creator_me:
            params["is_creator_me"] = str(is_creator_me)

        notes = await self._get_resource(
            path=path,
            model_type=PaginatedResponse[Note],
            params=params,
            response_parser=lambda data: {"count": data.get("count", 0), "results": data.get("results", [])},
        )

        return notes

    async def post_document(self, path: str = "api/v1.0/documents/") -> Note:
        url = self._build_url(path)
        response = await self.client.post(
            url,
            headers=self._auth_headers(),
        )

        if response.status_code != 201:
            raise ExternalServiceError("Docs", _(f"Failed to create document (status {response.status_code})"))

        result = response.json()
        note: Note = TypeAdapter(Note).validate_python(result)
        return note
