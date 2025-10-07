import logging

from fastapi import APIRouter, Request

from app.clients.drive import DriveClient
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ServiceUnavailableError
from app.models.document import Document
from app.models.user import User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/drive", tags=["drive"])


@router.get("/documents", response_model=list[Document])
async def drive_documents(
    request: Request,
    http_client: HTTPClient,
    title: str | None = None,
    favorite: bool = False,
) -> list[Document]:
    """Get documents from Drive service."""
    if not settings.drive_enabled or not settings.DRIVE_URL:
        raise ServiceUnavailableError("Drive")

    user: User = request.state.user
    token = await exchange_token(user.access_token, audience=settings.DRIVE_AUDIENCE) or ""

    client = DriveClient(http_client, settings.DRIVE_URL, token)
    return await client.get_documents(title=title, favorite=favorite)
