"""Grist API routes."""

import logging

from fastapi import APIRouter, Request

from app.clients.grist import GristClient
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ServiceUnavailableError
from app.models.grist import GristDocument, GristOrganization
from app.token_exchange import get_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/grist", tags=["grist"])


async def get_grist_client(request: Request, http_client: HTTPClient) -> GristClient:
    if not settings.grist_enabled or not settings.GRIST_URL:
        raise ServiceUnavailableError("Grist")

    # Get auth from session (already refreshed by get_current_user dependency)
    token = await get_token(request, settings.GRIST_AUDIENCE)

    # Create client and fetch organizations
    return GristClient(http_client, settings.GRIST_URL, token)


@router.get("/orgs", response_model=list[GristOrganization])
async def get_organizations(
    request: Request,
    http_client: HTTPClient,
) -> list[GristOrganization]:
    """Get organizations (teams) from Grist that the user has access to.

    Note: Auth is already validated by get_current_user() at router level.
    """

    client = await get_grist_client(request, http_client)
    return await client.get_organizations()


@router.get("/docs", response_model=list[GristDocument])
async def get_documents(
    request: Request,
    http_client: HTTPClient,
    page: int = 1,
    page_size: int = 5,
) -> list[GristDocument]:
    """Get all documents across all organizations with pagination.
    Documents are sorted by updated date (most recent first).

    Note: Auth is already validated by get_current_user() at router level.
    """

    client = await get_grist_client(request, http_client)
    return await client.get_all_documents(page, page_size)
