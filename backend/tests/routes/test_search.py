from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

from app.models.search import SearchResult
from fastapi.testclient import TestClient

SEARCH_SETTINGS = {
    "FIND_URL": "https://find.example.com",
    "MENSHEN_URL": "https://menshen.example.com",
    "MENSHEN_CLIENT_ID": "bureaublad",
    "MENSHEN_CLIENT_SECRET": "secret",
    "FIND_SEARCH_SCOPE": "action:search-find-bureaublad",
}


def enable_search() -> list:
    """Patch the settings that make up the search feature toggle."""
    return [patch(f"app.core.config.settings.{key}", value) for key, value in SEARCH_SETTINGS.items()]


class TestSearchEndpoint:
    """Tests for /search endpoint."""

    def test_search_unauthenticated(self, client: TestClient) -> None:
        """Test that search returns 401 when not authenticated."""
        response = client.get("/api/v1/search", params={"q": "test"})
        assert response.status_code == 401

    def test_search_disabled(self, authenticated_client: TestClient) -> None:
        """Test that search returns 404 when Find is not configured."""
        response = authenticated_client.get("/api/v1/search", params={"q": "test"})
        assert response.status_code == 404

    def test_search_requires_query(self, authenticated_client: TestClient) -> None:
        """Test that search validates the q parameter."""
        response = authenticated_client.get("/api/v1/search")
        assert response.status_code == 422

    @patch("app.routes.search.search_documents", new_callable=AsyncMock)
    @patch("app.routes.search.exchange_token_for_find", new_callable=AsyncMock)
    def test_search_success(
        self, mock_exchange: AsyncMock, mock_search: AsyncMock, authenticated_client: TestClient
    ) -> None:
        """Test a successful search proxies the query and returns mapped results."""
        mock_exchange.return_value = "find-token"
        mock_search.return_value = [
            SearchResult(
                id="a8098c1a-f86e-11da-bd1a-00112444be1e",
                service="docs",
                title="Meeting notes",
                path="/notes",
                updated_at=datetime(2026, 11, 1, tzinfo=UTC),
                url="https://docs.example.com/docs/a8098c1a-f86e-11da-bd1a-00112444be1e",
            )
        ]

        patchers = enable_search()
        for patcher in patchers:
            patcher.start()
        try:
            response = authenticated_client.get("/api/v1/search", params={"q": "notes"})
        finally:
            for patcher in patchers:
                patcher.stop()

        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 1
        assert data["results"][0]["title"] == "Meeting notes"
        mock_exchange.assert_called_once()
        # The user's access token from the authenticated session is exchanged
        assert mock_exchange.call_args.args[1] == "test-token"
        mock_search.assert_called_once()
        assert mock_search.call_args.args[2] == "notes"

    @patch("app.routes.search.exchange_token_for_find", new_callable=AsyncMock)
    def test_search_exchange_failure(self, mock_exchange: AsyncMock, authenticated_client: TestClient) -> None:
        """Test that a token exchange failure returns 503."""
        from app.services.search import SearchUnavailableError

        mock_exchange.side_effect = SearchUnavailableError("exchange failed")

        patchers = enable_search()
        for patcher in patchers:
            patcher.start()
        try:
            response = authenticated_client.get("/api/v1/search", params={"q": "notes"})
        finally:
            for patcher in patchers:
                patcher.stop()

        assert response.status_code == 503
