import asyncio
import logging

import httpx
from app.exceptions import ExternalServiceError
from app.models.grist import GristDocument, GristOrganization, GristWorkspace
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class GristClient:
    def __init__(self, http_client: httpx.AsyncClient, base_url: str, token: str) -> None:
        self.client = http_client
        self.base_url = base_url.rstrip("/")
        self.token = token

    async def _fetch_list[T](self, url: str, model_type: type[T], resource_name: str) -> list[T]:
        """Generic method to fetch a list of resources from the Grist API."""
        try:
            response = await self.client.get(
                url,
                headers={"Authorization": f"Bearer {self.token}"},
            )

            if response.status_code != 200:
                logger.error(f"Grist API returned status {response.status_code}: {response.text}")
                raise ExternalServiceError("Grist", f"Failed to fetch {resource_name} (status {response.status_code})")

            data = response.json()
            return TypeAdapter(list[model_type]).validate_python(data)

        except httpx.HTTPError as e:
            logger.exception("HTTP error calling Grist API")
            raise ExternalServiceError("Grist", f"HTTP error: {e}") from e

    async def get_organizations(self, path: str = "api/orgs") -> list[GristOrganization]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        return await self._fetch_list(url, GristOrganization, "organizations")

    async def get_workspaces(self, organization_id: int) -> list[GristWorkspace]:
        url = f"{self.base_url}/api/orgs/{organization_id}/workspaces"
        return await self._fetch_list(url, GristWorkspace, "workspaces")

    async def get_all_documents(self, page: int = 1, page_size: int = 5) -> list[GristDocument]:
        """
        Fetch all documents across all organizations, sorted by updated date (most recent first).
        """

        if page < 1:
            page = 1

        if page_size < 1:
            page_size = 1

        # NOTE: The Girst API does not support pagination, so we have to fetch all documents
        # for all workspaces for all organizations.
        orgs = await self.get_organizations()

        workspace_tasks = [self.get_workspaces(org.id) for org in orgs]
        all_workspaces_nested = await asyncio.gather(*workspace_tasks)

        docs = sorted(
            [doc for workspaces in all_workspaces_nested for workspace in workspaces for doc in workspace.docs],
            key=lambda d: d.updated_at,
            reverse=True,
        )

        offset = (page - 1) * page_size
        return docs[offset : offset + page_size]
