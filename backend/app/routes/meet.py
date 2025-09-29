import logging

from fastapi import APIRouter, Request

from app.clients.meet import MeetClient
from app.config import settings
from app.models import Meeting, User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/meet", tags=["meet"])


@router.get("/meeting", response_model=list[Meeting])
async def meet_dmeetings(request: Request, title: str | None = None, favorite: bool = False) -> list[Meeting]:
    user: User = request.state.user
    access_token = user.access_token
    new_token = await exchange_token(access_token, audience=settings.MEET_AUDIENCE)

    if not new_token:
        return []

    client = MeetClient(base_url=settings.MEET_URL, token=new_token)

    documents: list[Meeting] = client.get_documents(title=title, favorite=favorite)

    return documents