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

    def get_documents(self, path: str = "api/v1.0/documents/", page: int = 1, title: str | None = None) -> list[Note]:
        url = f"{self.base_url}/{path}?page={page}"

        if title:
            url = f"{url}&title={title}"
        response = self.client.request("GET", url)
        if response.status_code != 200:
            return TypeAdapter(list[Note]).validate_python([])

        results = response.json().get("results", [])

        notes: list[Note] = TypeAdapter(list[Note]).validate_python(results)

        return notes
