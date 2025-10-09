import logging

from fastapi import APIRouter, Request

from app.clients.docs import DocsClient
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ServiceUnavailableError
from app.models.note import Note
from app.models.user import User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/docs", tags=["docs"])


@router.get("/documents", response_model=list[Note])
async def docs_documents(
    request: Request,
    http_client: HTTPClient,
    title: str | None = None,
    favorite: bool = False,
) -> list[Note]:
    """Get documents from Docs service."""
    if not settings.docs_enabled or not settings.DOCS_URL:
        raise ServiceUnavailableError("Docs")

    user: User = request.state.user
    token = await exchange_token(user.access_token, audience=settings.DOCS_AUDIENCE) or ""

    client = DocsClient(http_client, settings.DOCS_URL, token)
    return await client.get_documents(title=title, favorite=favorite)
