import logging

from fastapi import APIRouter, HTTPException, Request

from app.clients.ocs import OCSClient
from app.config import settings
from app.models import Activity, SearchResults, User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ocs", tags=["ocs"])


@router.get("/activities", response_model=list[Activity])
async def ocs_activities(request: Request) -> list[Activity]:
    # Redundant checks needed to satisfy the type system.
    if not settings.ocs_enabled or not settings.OCS_URL:
        raise HTTPException(status_code=503, detail="OCS service is not configured")

    user: User = request.state.user
    access_token = user.access_token

    new_token = await exchange_token(access_token, audience=settings.OCS_AUDIENCE)

    if not new_token:
        return []

    client = OCSClient(base_url=settings.OCS_URL, token=new_token)

    activities: list[Activity] = client.get_activities()

    return activities


@router.get("/search", response_model=list[SearchResults])
async def ocs_search(request: Request, term: str) -> list[SearchResults]:
    # Redundant checks needed to satisfy the type system.
    if not settings.ocs_enabled or not settings.OCS_URL:
        raise HTTPException(status_code=503, detail="OCS service is not configured")

    user: User = request.state.user
    access_token = user.access_token

    new_token = await exchange_token(access_token, audience=settings.OCS_AUDIENCE)

    if not new_token:
        return []

    client = OCSClient(base_url=settings.OCS_URL, token=new_token)

    # todo: make parallel requests
    search_results_files: list[SearchResults] = client.search_files(term=term)
    search_results_calendar: list[SearchResults] = client.search_calendar(term=term)
    search_results_tasks: list[SearchResults] = client.search_tasks(term=term)

    combined_results: list[SearchResults] = search_results_files + search_results_calendar + search_results_tasks

    return combined_results
