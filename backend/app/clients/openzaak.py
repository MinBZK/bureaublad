import httpx
from app.models import Zaak
from pydantic import TypeAdapter


class OpenzaakClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        )


    def get_zaken(
        self, path: str = "zaken/api/v1/zaken") -> list[Zaak]:
        url = httpx.URL(f"{self.base_url}/{path}")

        print(self.token)
        response = self.client.request("GET", url)
        print(response)
        if response.status_code != 200:
            return TypeAdapter(list[Zaak]).validate_python([])

        results = response.json().get("results", [])

        zaken: list[Zaak] = TypeAdapter(list[Zaak]).validate_python(results)

        return zaken
