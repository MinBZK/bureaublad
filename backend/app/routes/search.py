import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request

from app.core import session
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.core.translate import _
from app.exceptions import CredentialError
from app.models.search import SearchResponse
from app.services.search import SearchUnavailableError, exchange_token_for_find, search_documents

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
async def search(
    request: Request,
    client: HTTPClient,
    q: Annotated[str, Query(min_length=1, max_length=300)],
) -> SearchResponse:
    """Search documents across all La Suite services via Find.

    Exchanges the user's access token with Menshen for a Find-scoped token and
    proxies the query to the Find search endpoint.
    """
    if not settings.search_enabled:
        raise HTTPException(status_code=404, detail=_("Search is not enabled"))

    auth = await session.get_auth(request)
    if not auth:
        raise CredentialError(_("Not authenticated"))

    try:
        find_token = await exchange_token_for_find(client, auth.access_token)
        results = await search_documents(client, find_token, q)
    except SearchUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return SearchResponse(results=results)
