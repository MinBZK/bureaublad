import logging

from fastapi import APIRouter, Request

from app.clients.drive import DriveClient
from app.core import session
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import CredentialError, ServiceUnavailableError
from app.models.document import Document
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/drive", tags=["drive"])


@router.get("/documents", response_model=list[Document])
async def drive_documents(
    request: Request,
    http_client: HTTPClient,
    title: str | None = None,
    is_favorite: bool = False,
) -> list[Document]:
    """Get documents from Drive service.

    Note: Auth is validated by get_current_user() at router level.
    """
    if not settings.drive_enabled or not settings.DRIVE_URL:
        raise ServiceUnavailableError("Drive")

    # Get auth from session (already refreshed by get_current_user dependency)
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    token = await exchange_token(http_client, auth.access_token, audience=settings.DRIVE_AUDIENCE) or ""

    client = DriveClient(http_client, settings.DRIVE_URL, token)
    return await client.get_documents(title=title, is_favorite=is_favorite)
