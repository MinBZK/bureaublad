import httpx
import time
from jose import jwt
from jose.constants import ALGORITHMS
from app.models import Zaak
from app.config import settings
from pydantic import TypeAdapter


class ZakenClient:
    def __init__(self, base_url: str, user_id: str, user_representation: str) -> None:
        self.base_url = base_url
        self.user_id = user_id
        self.user_representation = user_representation

    def get_zaken(
            self, path: str = "zaken/api/v1/zaken", page: int = 1
    ) -> list[Zaak]:
        payload = {
            "iss": settings.OPENZAAK_CLIENT_ID,
            "iat": int(time.time()),  # current time in seconds
            "client_id": settings.OPENZAAK_CLIENT_ID,
            "user_id": self.user_id,
            "user_representation": self.user_representation,
        }
        jwt_token = jwt.encode(payload, settings.OPENZAAK_SECRET, algorithm=ALGORITHMS.HS256)

        client = httpx.Client(
            headers={"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json", "Accept-Crs": "EPSG:4326"}
        )

        url = httpx.URL(f"{self.base_url}/{path}", params={"page": page, "ordering": "startdatum"})


        response = client.request("GET", url)
        if response.status_code != 200:
            return TypeAdapter(list[Zaak]).validate_python([])

        results = response.json().get("results", [])

        zaken: list[Zaak] = TypeAdapter(list[Zaak]).validate_python(results)
        zaken.reverse()

        return zaken
