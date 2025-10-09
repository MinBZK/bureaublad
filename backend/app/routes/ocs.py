import asyncio
import logging

from fastapi import APIRouter, Request

from app.clients.ocs import OCSClient
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ServiceUnavailableError
from app.models.activity import Activity
from app.models.search import SearchResults
from app.models.user import User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ocs", tags=["ocs"])


@router.get("/activities", response_model=list[Activity])
async def ocs_activities(
    request: Request,
    http_client: HTTPClient,
) -> list[Activity]:
    """Get activities from OCS service."""
    if not settings.ocs_enabled or not settings.OCS_URL:
        raise ServiceUnavailableError("OCS")

    user: User = request.state.user
    token = await exchange_token(user.access_token, audience=settings.OCS_AUDIENCE) or ""

    client = OCSClient(http_client, settings.OCS_URL, token)
    return await client.get_activities()


@router.get("/search", response_model=list[SearchResults])
async def ocs_search(
    request: Request,
    http_client: HTTPClient,
    term: str,
) -> list[SearchResults]:
    """Search across files, calendar, and tasks in parallel."""
    if not settings.ocs_enabled or not settings.OCS_URL:
        raise ServiceUnavailableError("OCS")

    user: User = request.state.user
    token = await exchange_token(user.access_token, audience=settings.OCS_AUDIENCE) or ""

    client = OCSClient(http_client, settings.OCS_URL, token)

    # Run searches in parallel for 3x speedup
    search_results_files, search_results_calendar, search_results_tasks = await asyncio.gather(
        client.search_files(term=term),
        client.search_calendar(term=term),
        client.search_tasks(term=term),
    )

    combined_results: list[SearchResults] = search_results_files + search_results_calendar + search_results_tasks

    return combined_results
