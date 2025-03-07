import httpx


class MatrixClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token
        self.client = httpx.Client(headers={"Authorization": f"Bearer {self.token}"})

    def get_files(self, path: str = "api/v1.0/documents/?page=1") -> str:
        url = f"{self.base_url}/{path}".rstrip("/")
        response = self.client.request("GET", url)
        response.raise_for_status()
        return response.text
