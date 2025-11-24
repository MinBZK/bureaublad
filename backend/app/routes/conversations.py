import logging

from fastapi import APIRouter, Request

from app.clients.conversation import ConversationClient
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ServiceUnavailableError
from app.models.conversation import Conversation
from app.models.pagination import PaginatedResponse
from app.token_exchange import get_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversations", tags=["conversations"])


async def get_conversations_client(request: Request, http_client: HTTPClient) -> ConversationClient:
    if not settings.conversation_enabled or not settings.CONVERSATION_URL:
        raise ServiceUnavailableError("Conversation")

    # Get auth from session (already refreshed by get_current_user dependency)
    token = await get_token(request, settings.CONVERSATION_AUDIENCE)

    return ConversationClient(http_client, settings.CONVERSATION_URL, token)


@router.get("/chats", response_model=PaginatedResponse[Conversation])
async def conversations_get_chat(
    request: Request,
    http_client: HTTPClient,
    page: int = 1,
    page_size: int = 5,
    title: str | None = None,
) -> PaginatedResponse[Conversation]:
    """Get meetings from Meet service."""
    client = await get_conversations_client(request, http_client)
    return await client.get_chats(page=page, page_size=page_size, title=title)
