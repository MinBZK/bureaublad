import logging
import random
from string import ascii_lowercase

from fastapi import APIRouter, Request

from app.clients.meet import MeetClient
from app.core.config import settings
from app.core.http_clients import HTTPClient
from app.exceptions import ServiceUnavailableError
from app.models.room import Room
from app.token_exchange import get_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/meet", tags=["meet"])


def generate_random_room_name() -> str:
    letters = ascii_lowercase

    def rand_str(length: int) -> str:
        return "".join(random.choice(letters) for _ in range(length))  # noqa: S311

    return f"{rand_str(3)}-{rand_str(4)}-{rand_str(3)}"


async def get_meet_client(request: Request, http_client: HTTPClient) -> MeetClient:
    if not settings.meet_enabled or not settings.MEET_URL:
        raise ServiceUnavailableError("Meet")

    token = await get_token(request, settings.MEET_AUDIENCE)

    return MeetClient(http_client, settings.MEET_URL, token)


@router.get("/rooms", response_model=list[Room])
async def meet_get_rooms(
    request: Request,
    http_client: HTTPClient,
    page: int | None = None,
) -> list[Room]:
    """Get meetings from Meet service.

    Note: Auth is validated by get_current_user() at router level.
    """
    client = await get_meet_client(request, http_client)
    return await client.get_rooms(page=page)


@router.post("/rooms", response_model=Room)
async def meet_post_room(request: Request, http_client: HTTPClient) -> Room:
    if not settings.meet_enabled or not settings.MEET_URL:
        raise ServiceUnavailableError("Meet")

    # Get auth from session (already refreshed by get_current_user dependency)
    client = await get_meet_client(request, http_client)

    name: str = generate_random_room_name()

    return await client.post_room(name=name)
