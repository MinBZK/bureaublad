import logging

from fastapi import APIRouter, Request

from app.clients.ocs import OCSClient
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ServiceUnavailableError
from app.models.activity import Activity
from app.models.search import SearchResults
from app.token_exchange import get_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ocs", tags=["ocs"])


async def get_ocs_client(request: Request, http_client: HTTPClient) -> OCSClient:
    if not settings.ocs_enabled or not settings.OCS_URL:
        raise ServiceUnavailableError("OCS")

    token = await get_token(request, settings.OCS_AUDIENCE)

    client = OCSClient(http_client, settings.OCS_URL, token)
    return client


@router.get("/activities", response_model=list[Activity])
async def ocs_activities(
    request: Request,
    http_client: HTTPClient,
) -> list[Activity]:
    """Get activities from OCS service.

    Note: Auth is validated by get_current_user() at router level.
    """
    client = await get_ocs_client(request, http_client)

    return await client.get_activities()


@router.get("/search", response_model=list[SearchResults])
async def ocs_search(request: Request, http_client: HTTPClient, term: str) -> list[SearchResults]:
    """Get file search results from OCS service.

    Note: Auth is validated by get_current_user() at router level.
    """
    if len(term) < 4:
        return []

    client = await get_ocs_client(request, http_client)

    search_results_files: list[SearchResults] = await client.search_files(term=term)
    return search_results_files
