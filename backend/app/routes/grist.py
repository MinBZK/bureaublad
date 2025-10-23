"""Grist API routes."""

import logging

from fastapi import APIRouter, Request

from app.clients.grist import GristClient
from app.core import session
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import CredentialError, ServiceUnavailableError
from app.models.grist import GristDocument, GristOrganization
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/grist", tags=["grist"])


@router.get("/orgs", response_model=list[GristOrganization])
async def get_organizations(
    request: Request,
    http_client: HTTPClient,
) -> list[GristOrganization]:
    """Get organizations (teams) from Grist that the user has access to.

    Note: Auth is already validated by get_current_user() at router level.
    """

    if not settings.grist_enabled or not settings.GRIST_URL:
        raise ServiceUnavailableError("Grist")

    # Get auth from session (already refreshed by get_current_user dependency)
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    token = await exchange_token(auth.access_token, audience=settings.GRIST_AUDIENCE) or ""

    # Create client and fetch organizations
    client = GristClient(http_client, settings.GRIST_URL, token)
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

    if not settings.grist_enabled or not settings.GRIST_URL:
        raise ServiceUnavailableError("Grist")

    # Get auth from session (already refreshed by get_current_user dependency)
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    token = await exchange_token(auth.access_token, audience=settings.GRIST_AUDIENCE) or ""

    client = GristClient(http_client, settings.GRIST_URL, token)

    return await client.get_all_documents(page, page_size)
