import logging
import random
from string import ascii_lowercase

from fastapi import APIRouter, Request

from app.clients.meet import MeetClient
from app.core import session
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import CredentialError, ServiceUnavailableError
from app.models.room import Room
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/meet", tags=["meet"])


def generate_random_room_name() -> str:
    letters = ascii_lowercase

    def rand_str(length: int) -> str:
        return "".join(random.choice(letters) for _ in range(length))  # noqa: S311

    return f"{rand_str(3)}-{rand_str(4)}-{rand_str(3)}"


@router.get("/rooms", response_model=list[Room])
async def meet_get_rooms(
    request: Request,
    http_client: HTTPClient,
    page: int | None = None,
) -> list[Room]:
    """Get meetings from Meet service.

    Note: Auth is validated by get_current_user() at router level.
    """
    if not settings.meet_enabled or not settings.MEET_URL:
        raise ServiceUnavailableError("Meet")

    # Get auth from session (already refreshed by get_current_user dependency)
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    token = await exchange_token(http_client, auth.access_token, audience=settings.MEET_AUDIENCE) or ""

    client = MeetClient(http_client, settings.MEET_URL, token)
    return await client.get_rooms(page=page)


@router.post("/rooms", response_model=Room)
async def meet_post_room(request: Request, http_client: HTTPClient) -> Room:
    if not settings.meet_enabled or not settings.MEET_URL:
        raise ServiceUnavailableError("Meet")

    # Get auth from session (already refreshed by get_current_user dependency)
    auth = session.get_auth(request)
    if not auth:
        raise CredentialError("Not authenticated")

    token = await exchange_token(auth.access_token, audience=settings.MEET_AUDIENCE) or ""

    client = MeetClient(http_client, settings.MEET_URL, token)

    name: str = generate_random_room_name()

    return await client.post_room(name=name)
