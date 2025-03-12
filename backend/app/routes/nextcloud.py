import logging

from fastapi import APIRouter, Request

from app.clients.nextcloud import NextCloudClient
from app.config import settings
from app.models import Activity, User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/nextcloud", tags=["nextcloud"])


@router.get("/activities", response_model=list[Activity])
async def nextcloud_activities(request: Request) -> list[Activity]:
    user: User = request.state.user
    access_token = user.access_token

    new_token = await exchange_token(access_token, audience="files")

    if not new_token:
        return []

    client = NextCloudClient(base_url=settings.NEXTCLOUD_URL, token=new_token)

    activities: list[Activity] = client.get_activities()

    return activities
