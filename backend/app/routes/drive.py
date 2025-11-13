import logging

from fastapi import APIRouter, Request

from app.clients.drive import DriveClient
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ServiceUnavailableError
from app.models.document import Document
from app.models.pagination import PaginatedResponse
from app.token_exchange import get_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/drive", tags=["drive"])


async def get_drive_client(request: Request, http_client: HTTPClient) -> DriveClient:
    if not settings.drive_enabled or not settings.DRIVE_URL:
        raise ServiceUnavailableError("Drive")

    token = await get_token(request, settings.DRIVE_AUDIENCE)

    return DriveClient(http_client, settings.DRIVE_URL, token)


@router.get("/documents", response_model=PaginatedResponse[Document])
async def drive_documents(
    request: Request,
    http_client: HTTPClient,
    page: int = 1,
    page_size: int = 5,
    title: str | None = None,
    is_favorite: bool = False,
) -> PaginatedResponse[Document]:
    """Get documents from Drive service."""
    if not settings.drive_enabled or not settings.DRIVE_URL:
        raise ServiceUnavailableError("Drive")

    client = await get_drive_client(request, http_client)
    return await client.get_documents(page=page, page_size=page_size, title=title, is_favorite=is_favorite)
