import logging

import httpx
from bureaublad_api.exceptions import ExternalServiceError
from bureaublad_api.models.note import Note
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class DocsClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        )

    def get_documents(
        self, path: str = "api/v1.0/documents/", page: int = 1, title: str | None = None, favorite: bool = False
    ) -> list[Note]:
        url = httpx.URL(f"{self.base_url}/{path}", params={"page": page})

        if title:
            url = url.copy_add_param("title", str(title))

        if favorite:
            url = url.copy_add_param("favorite", str(favorite))

        response = self.client.request("GET", url)
        if response.status_code != 200:
            logger.error(f"Docs get_documents failed: status={response.status_code}, url={url}")
            raise ExternalServiceError("Docs", f"Failed to fetch documents (status {response.status_code})")

        results = response.json().get("results", [])

        notes: list[Note] = TypeAdapter(list[Note]).validate_python(results)

        return notes
