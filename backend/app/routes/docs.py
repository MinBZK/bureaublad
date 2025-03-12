import logging

from fastapi import APIRouter, Request

from app.clients.docs import DocsClient
from app.config import settings
from app.models import Note, User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/docs", tags=["docs"])


@router.get("/documents", response_model=list[Note])
async def docs_documents(request: Request, q: str | None = None) -> list[Note]:
    user: User = request.state.user
    access_token = user.access_token
    new_token = await exchange_token(access_token, audience="docs")

    if not new_token:
        return []

    client = DocsClient(base_url=settings.DOCS_URL, token=new_token)

    documents: list[Note] = client.get_documents(title=q)

    return documents
