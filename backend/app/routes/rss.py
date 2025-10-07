import httpx
from fastapi import APIRouter, Query, Response

router = APIRouter(prefix="/rss", tags=["rss"])


@router.get("/")
async def rss_feed(url: str = Query(..., description="URL of the RSS feed")) -> Response:
    client = httpx.AsyncClient(timeout=5.0)
    resp = await client.get(url)
    resp.raise_for_status()
    # Forward the raw RSS feed content and content-type header
    return Response(content=resp.content, media_type=resp.headers.get("content-type", "application/xml"))
