import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.clients.ai import AIClient
from app.core.config import settings
from app.exceptions import ServiceUnavailableError
from app.models.ai import ChatCompletionRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat/completions")
async def ai_post_chat_completions(chat_request: ChatCompletionRequest) -> StreamingResponse:
    # Redundant checks needed to satisfy the type system.
    if not settings.ai_enabled or not settings.AI_MODEL:
        raise ServiceUnavailableError("AI")

    client = AIClient(model=settings.AI_MODEL, base_url=settings.AI_BASE_URL, api_key=settings.AI_API_KEY)

    return StreamingResponse(client.stream_response(chat_request=chat_request), media_type="text/event-stream")
