import logging

from fastapi import APIRouter, Request

from app.clients.conversation import ConversationClient
from app.core import session
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import CredentialError, ServiceUnavailableError
from app.models.conversation import Conversation
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("/chats", response_model=list[Conversation])
async def conversations_get_chat(request: Request, http_client: HTTPClient, page: int = 1) -> list[Conversation]:
    """Get meetings from Meet service.

    Note: Auth is validated by get_current_user() at router level.
    """
    if not settings.conversation_enabled or not settings.CONVERSATION_URL:
        raise ServiceUnavailableError("Conversation")

    # Get auth from session (already refreshed by get_current_user dependency)
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    token = await exchange_token(auth.access_token, audience=settings.CONVERSATION_AUDIENCE) or ""

    client = ConversationClient(http_client, settings.CONVERSATION_URL, token)
    return await client.get_chats(page=page)
