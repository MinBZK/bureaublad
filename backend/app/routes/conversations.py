import logging

from fastapi import APIRouter, Request

from app.clients.conversation import ConversationClient
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ServiceUnavailableError
from app.models.conversation import Conversation
from app.token_exchange import get_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversations", tags=["conversations"])


async def get_conversations_client(request: Request, http_client: HTTPClient) -> ConversationClient:
    if not settings.conversation_enabled or not settings.CONVERSATION_URL:
        raise ServiceUnavailableError("Conversation")

    # Get auth from session (already refreshed by get_current_user dependency)
    token = await get_token(request, settings.CONVERSATION_AUDIENCE)

    return ConversationClient(http_client, settings.CONVERSATION_URL, token)


@router.get("/chats", response_model=list[Conversation])
async def conversations_get_chat(request: Request, http_client: HTTPClient, page: int = 1) -> list[Conversation]:
    """Get meetings from Meet service.

    Note: Auth is validated by get_current_user() at router level.
    """
    client = await get_conversations_client(request, http_client)
    return await client.get_chats(page=page)
