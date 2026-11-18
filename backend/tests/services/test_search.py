from collections.abc import Callable
from unittest.mock import patch

import httpx
import pytest
from app.services.search import (
    FIND_SEARCH_PATH,
    MENSHEN_EXCHANGE_PATH,
    SearchUnavailableError,
    exchange_token_for_find,
    search_documents,
)


def make_client(handler: Callable[[httpx.Request], httpx.Response]) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


EXCHANGE_SETTINGS = {
    "MENSHEN_URL": "https://menshen.example.com",
    "MENSHEN_CLIENT_ID": "bureaublad",
    "MENSHEN_CLIENT_SECRET": "secret",
    "FIND_AUDIENCE": "find",
    "FIND_SEARCH_SCOPE": "action:search-find-bureaublad",
}


@pytest.mark.asyncio
async def test_exchange_token_for_find_success() -> None:
    """Test that a token exchange posts an RFC 8693 request and returns the new token."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == MENSHEN_EXCHANGE_PATH
        assert request.headers["Authorization"].startswith("Basic ")
        body = request.read().decode()
        assert "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange" in body
        assert "subject_token=user-token" in body
        assert "audience=find" in body
        return httpx.Response(200, json={"access_token": "find-token"})

    patchers = [patch(f"app.core.config.settings.{key}", value) for key, value in EXCHANGE_SETTINGS.items()]
    for patcher in patchers:
        patcher.start()
    try:
        token = await exchange_token_for_find(make_client(handler), "user-token")
    finally:
        for patcher in patchers:
            patcher.stop()

    assert token == "find-token"


@pytest.mark.asyncio
async def test_exchange_token_for_find_failure() -> None:
    """Test that a failed exchange raises SearchUnavailableError."""
    with (
        patch("app.core.config.settings.MENSHEN_URL", "https://menshen.example.com"),
        pytest.raises(SearchUnavailableError),
    ):
        await exchange_token_for_find(make_client(lambda request: httpx.Response(403)), "user-token")


@pytest.mark.asyncio
async def test_search_documents_maps_results_and_links() -> None:
    """Test that Find hits are mapped to SearchResult objects with deep links."""
    find_response = {
        "results": [
            {
                "id": "a8098c1a-f86e-11da-bd1a-00112444be1e",
                "service": "docs",
                "title": "Meeting notes",
                "score": 1.5,
                "path": "/notes",
                "depth": 1,
                "numchild": 0,
                "size": 100,
                "created_at": "2026-10-01T10:00:00Z",
                "updated_at": "2026-11-01T10:00:00Z",
                "reach": "restricted",
                "tags": [],
            },
            {
                "id": "b8098c1a-f86e-11da-bd1a-00112444be1e",
                "service": "unknown-service",
                "title": "Unlinkable",
                "score": 1.0,
                "path": "/",
                "depth": 0,
                "numchild": 0,
                "size": 10,
                "created_at": "2026-10-01T10:00:00Z",
                "updated_at": "2026-11-01T10:00:00Z",
                "reach": None,
                "tags": [],
            },
        ]
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == FIND_SEARCH_PATH
        assert request.headers["Authorization"] == "Bearer find-token"
        assert request.read()  # body sent
        return httpx.Response(200, json=find_response)

    with (
        patch("app.core.config.settings.FIND_URL", "https://find.example.com"),
        patch("app.core.config.settings.DOCS_URL", "https://docs.example.com"),
    ):
        results = await search_documents(make_client(handler), "find-token", "notes")

    assert len(results) == 2
    assert results[0].title == "Meeting notes"
    # Default Docs URL convention
    assert results[0].url == "https://docs.example.com/docs/a8098c1a-f86e-11da-bd1a-00112444be1e"
    # No template configured for the service: no link
    assert results[1].url is None


@pytest.mark.asyncio
async def test_search_documents_failure() -> None:
    """Test that a Find error raises SearchUnavailableError."""
    with (
        patch("app.core.config.settings.FIND_URL", "https://find.example.com"),
        pytest.raises(SearchUnavailableError),
    ):
        await search_documents(make_client(lambda request: httpx.Response(500)), "find-token", "notes")


def test_find_document_url_override() -> None:
    """Test that FIND_URL_TEMPLATES overrides the default per-service templates."""
    from app.core.config import settings

    with (
        patch("app.core.config.settings.FIND_URL_TEMPLATES", {"docs": "https://custom.example.com/d/{id}?view=1"}),
        patch("app.core.config.settings.DOCS_URL", "https://docs.example.com"),
    ):
        url = settings.find_document_url("docs", "abc")

    assert url == "https://custom.example.com/d/abc?view=1"
