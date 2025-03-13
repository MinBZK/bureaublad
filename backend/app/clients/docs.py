import httpx
from app.models import Note
from pydantic import TypeAdapter


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
            return TypeAdapter(list[Note]).validate_python([])

        results = response.json().get("results", [])

        notes: list[Note] = TypeAdapter(list[Note]).validate_python(results)

        return notes
