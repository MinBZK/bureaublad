import logging

from fastapi import APIRouter, Request

from app.clients.drive import DriveClient
from app.config import settings
from app.models import Document, User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/drive", tags=["drive"])


@router.get("/documents", response_model=list[Document])
async def drive_documents(request: Request, title: str | None = None, favorite: bool = False) -> list[Document]:
    user: User = request.state.user
    access_token = user.access_token
    new_token = await exchange_token(access_token, audience=settings.DRIVE_AUDIENCE)

    if not new_token:
        return []

    client = DriveClient(base_url=settings.DRIVE_URL, token=new_token)

    documents: list[Document] = client.get_documents(title=title, favorite=favorite)

    return documents