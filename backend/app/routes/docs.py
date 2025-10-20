import logging

from fastapi import APIRouter, Request

from app.clients.docs import DocsClient
from app.core import session
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import CredentialError, ServiceUnavailableError
from app.models.note import Note
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/docs", tags=["docs"])


@router.get("/documents", response_model=list[Note])
async def docs_get_documents(
    request: Request,
    http_client: HTTPClient,
    title: str | None = None,
    is_favorite: bool = False,
) -> list[Note]:
    """Get documents from Docs service.

    Note: Auth is already validated by get_current_user() at router level.
    The auth state (including refreshed tokens) is available in request.session.
    """
    if not settings.docs_enabled or not settings.DOCS_URL:
        raise ServiceUnavailableError("Docs")

    # Get auth from session (already refreshed by get_current_user dependency)
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    token = await exchange_token(auth.access_token, audience=settings.DOCS_AUDIENCE) or ""

    client = DocsClient(http_client, settings.DOCS_URL, token)
    return await client.get_documents(title=title, is_favorite=is_favorite)


@router.post("/documents", response_model=Note)
async def docs_post_documents(request: Request, http_client: HTTPClient) -> Note:
    if not settings.docs_enabled or not settings.DOCS_URL:
        raise ServiceUnavailableError("Docs")

    # Get auth from session (already refreshed by get_current_user dependency)
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    token = await exchange_token(auth.access_token, audience=settings.DOCS_AUDIENCE) or ""

    client = DocsClient(http_client, settings.DOCS_URL, token)
    return await client.post_document()
