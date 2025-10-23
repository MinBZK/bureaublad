import logging

import httpx
from app.exceptions import ExternalServiceError
from app.models.grist import GristOrganization
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class GristClient:
    def __init__(self, http_client: httpx.AsyncClient, base_url: str, token: str) -> None:
        self.client = http_client
        self.base_url = base_url.rstrip("/")
        self.token = token

    async def get_organizations(self) -> list[GristOrganization]:
        url = f"{self.base_url}/api/orgs"

        try:
            response = await self.client.get(
                url,
                headers={"Authorization": f"Bearer {self.token}"},
            )

            if response.status_code != 200:
                logger.error(f"Grist API returned status {response.status_code}: {response.text}")
                raise ExternalServiceError("Grist", f"Failed to fetch organizations (status {response.status_code})")

            data = response.json()
            organizations: list[GristOrganization] = TypeAdapter(list[GristOrganization]).validate_python(data)

        except httpx.HTTPError as e:
            logger.exception("HTTP error calling Grist API")
            raise ExternalServiceError("Grist", f"HTTP error: {e}") from e

        else:
            return organizations
