import logging

from fastapi import APIRouter, Request

from app.clients.openzaak import OpenzaakClient
from app.config import settings
from app.models import User, Zaak
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/openzaak", tags=["openzaak"])


@router.get("/zaken")
async def openzaak_get_zaken(request: Request) -> list[Zaak | None]:
    user: User = request.state.user
    access_token = user.access_token

    new_token = await exchange_token(access_token, audience=settings.OPENZAAK_AUDIENCE)

    if not new_token:
        return []

    client = OpenzaakClient(base_url=settings.OPENZAAK_URL, token=new_token)

    zaken: list[Zaak | None] = client.get_zaken()

    return zaken
