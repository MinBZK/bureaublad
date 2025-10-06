import logging

from fastapi import APIRouter, HTTPException, Request

from app.clients.docs import DocsClient
from app.config import settings
from app.models import Note, User
from app.token_exchange import exchange_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/docs", tags=["docs"])


@router.get("/documents", response_model=list[Note])
async def docs_documents(request: Request, title: str | None = None, favorite: bool = False) -> list[Note]:
    # Redundant checks needed to satisfy the type system.
    if not settings.docs_enabled or not settings.DOCS_URL:
        raise HTTPException(status_code=503, detail="Docs service is not configured")

    user: User = request.state.user
    access_token = user.access_token
    new_token = await exchange_token(access_token, audience=settings.DOCS_AUDIENCE)

    if not new_token:
        return []

    client = DocsClient(base_url=settings.DOCS_URL, token=new_token)

    documents: list[Note] = client.get_documents(title=title, favorite=favorite)

    return documents
