import logging

from fastapi import APIRouter, Request

from app.clients.meet import MeetClient
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ServiceUnavailableError
from app.models.meeting import Meeting
from app.models.user import User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/meet", tags=["meet"])


@router.get("/meeting", response_model=list[Meeting])
async def meet_dmeetings(
    request: Request,
    http_client: HTTPClient,
    title: str | None = None,
    favorite: bool = False,
) -> list[Meeting]:
    """Get meetings from Meet service."""
    if not settings.meet_enabled or not settings.MEET_URL:
        raise ServiceUnavailableError("Meet")

    user: User = request.state.user
    token = await exchange_token(user.access_token, audience=settings.MEET_AUDIENCE) or ""

    client = MeetClient(http_client, settings.MEET_URL, token)
    return await client.get_meetings(title=title, favorite=favorite)
