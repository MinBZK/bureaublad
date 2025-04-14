import logging

from fastapi import APIRouter, Request

from app.clients.zaken import ZakenClient
from app.config import settings
from app.models import User, Zaak
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/zaken", tags=["zaken"])


@router.get("/zaken", response_model=list[Zaak])
async def zaken_zaken(request: Request) -> list[Zaak]:
    user: User = request.state.user
    access_token = user.access_token
    new_token = await exchange_token(access_token, audience=settings.ZAKEN_AUDIENCE)

    if not new_token:
        return []

    client = ZakenClient(base_url=settings.ZAKEN_URL, user_id=user.email, user_representation=user.name)

    zaken: list[Zaak] = client.get_zaken()

    return zaken
