from fastapi import APIRouter, Query, Response

from app.core.http_clients import HTTPClient

router = APIRouter(prefix="/rss", tags=["rss"])


@router.get("/")
async def rss_feed(
    http_client: HTTPClient,
    url: str = Query(..., description="URL of the RSS feed"),
) -> Response:
    """Fetch and return an RSS feed."""
    resp = await http_client.get(url)
    resp.raise_for_status()

    # Forward the raw RSS feed content and content-type header
    return Response(content=resp.content, media_type=resp.headers.get("content-type", "application/xml"))
