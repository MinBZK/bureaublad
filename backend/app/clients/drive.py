import httpx
from app.models import Document
from pydantic import TypeAdapter


class DriveClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        )

    def get_documents(
        self, path: str = "api/v1.0/items/", page: int = 1, title: str | None = None, favorite: bool = False
    ) -> list[Document]:
        url = httpx.URL(f"{self.base_url}/{path}", params={"page": page})

        if title:
            url = url.copy_add_param("title", str(title))

        response = self.client.request("GET", url)
        if response.status_code != 200:
            return TypeAdapter(list[Document]).validate_python([])

        results = response.json().get("results", [])

        if len(results) < 1:
            return TypeAdapter(list[Document]).validate_python([])

        workspace_id = results[0]["id"]

        item_url = f"{self.base_url}/api/v1.0/items/{workspace_id}/children/"

        response = self.client.request("GET", item_url)
        if response.status_code != 200:
            return TypeAdapter(list[Document]).validate_python([])

        results = response.json().get("results", [])

        print(results)

        notes: list[Document] = TypeAdapter(list[Document]).validate_python(results)

        return notes
