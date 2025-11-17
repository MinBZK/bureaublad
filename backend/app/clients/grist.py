import logging

from app.clients.base import BaseAPIClient
from app.models.grist import GristDocument, GristOrganization, GristWorkspace
from app.models.pagination import PaginatedResponse

logger = logging.getLogger(__name__)


class GristClient(BaseAPIClient):
    service_name = "Grist"

    async def get_organizations(self, path: str = "api/orgs") -> list[GristOrganization]:
        return await self._get_resource(path=path, model_type=list[GristOrganization])

    async def get_workspaces(self, organization_id: int) -> list[GristWorkspace]:
        path = f"api/orgs/{organization_id}/workspaces"
        return await self._get_resource(path=path, model_type=list[GristWorkspace])

    async def get_documents(
        self,
        organization_id: int,
        page: int = 1,
        page_size: int = 5,
    ) -> PaginatedResponse[GristDocument]:
        """
        Fetch all documents for organization with organization_id, sorted by updated date (most recent first).
        """
        page = max(1, page)
        page_size = max(1, page_size)

        workspace_tasks = await self.get_workspaces(organization_id)

        docs = sorted(
            [doc for workspace in workspace_tasks for doc in workspace.docs],
            key=lambda d: d.updated_at,
            reverse=True,
        )

        offset = (page - 1) * page_size
        return PaginatedResponse[GristDocument](count=len(docs), results=docs[offset : offset + page_size])
