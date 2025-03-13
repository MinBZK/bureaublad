import httpx


class CaldavClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        )

    def get_calendars(self, path: str = "/remote.php/dav") -> list[str]:
        url = httpx.URL(f"{self.base_url}/{path}")

        response = self.client.request("GET", url)
        if response.status_code != 200:
            return []

        _ = response.text

        return []
