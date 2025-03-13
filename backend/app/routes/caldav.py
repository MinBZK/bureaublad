import logging

from fastapi import APIRouter, Request

from app.clients.caldav import CaldavClient
from app.config import settings
from app.models import User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/caldav", tags=["caldav"])


@router.get("/calendars", response_model=list[str])
async def nextcloud_activities(request: Request) -> list[str]:
    user: User = request.state.user
    access_token = user.access_token

    new_token = await exchange_token(access_token, audience=settings.CALENDAR_AUDIENCE)

    if not new_token:
        return []

    client = CaldavClient(base_url=settings.CALENDAR_URL, token=new_token)

    activities: list[str] = client.get_calendars()

    return activities
