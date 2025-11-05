"""Tests for the OCS endpoints."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from app.models.activity import Activity
from app.models.search import SearchResults
from fastapi.testclient import TestClient


class TestOCSEndpoints:
    """Test cases for OCS endpoints."""

    def test_ocs_activities_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that activities endpoint requires authentication."""
        response = fresh_client.get("/api/v1/ocs/activities")
        assert response.status_code == 401

    def test_ocs_search_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that search endpoint requires authentication."""
        response = fresh_client.get("/api/v1/ocs/search?term=test")
        assert response.status_code == 401

    @patch("app.routes.ocs.settings.OCS_URL", None)
    def test_ocs_activities_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test activities endpoint when service is disabled."""
        response = authenticated_client.get("/api/v1/ocs/activities")
        assert response.status_code == 503

    @patch("app.routes.ocs.settings.OCS_URL", None)
    def test_ocs_search_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test search endpoint when service is disabled."""
        response = authenticated_client.get("/api/v1/ocs/search?term=test")
        assert response.status_code == 503

    @patch("app.routes.ocs.settings.OCS_URL", "https://ocs.example.com")
    @patch("app.routes.ocs.settings.OCS_AUDIENCE", "ocs")
    @patch("app.routes.ocs.get_token")
    @patch("app.routes.ocs.OCSClient")
    def test_ocs_activities_success(
        self,
        mock_ocs_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful activities retrieval."""
        # Mock token exchange
        mock_get_token.return_value = "test-ocs-token"

        # Mock OCSClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_activities.return_value = [
            Activity(
                activity_id=123,
                app="files",
                type="file_created",
                user="testuser",
                subject="File created",
                message="Created file document.pdf",
                link="/f/456",
                object_type="files",
                object_id=456,
                object_name="documents/document.pdf",
                datetime=datetime(2024, 11, 1, 10, 30, 0),
            ),
            Activity(
                activity_id=124,
                app="files",
                type="file_changed",
                user="testuser",
                subject="File changed",
                message="Modified file report.docx",
                link="/f/789",
                object_type="files",
                object_id=789,
                object_name="reports/report.docx",
                datetime=datetime(2024, 11, 1, 14, 15, 0),
            ),
        ]
        mock_ocs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/ocs/activities")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["activity_id"] == 123
        assert data[0]["app"] == "files"
        assert data[0]["type"] == "file_created"
        assert data[0]["user"] == "testuser"
        assert data[0]["subject"] == "File created"
        assert data[0]["object_name"] == "documents/document.pdf"
        assert data[0]["url"] == "https://ocs.example.com/f/456"
        assert data[0]["date"] == "01 Nov 2024"
        assert data[0]["time"] == "10:30:00"
        assert data[0]["object_filename"] == "document.pdf"
        assert data[1]["activity_id"] == 124
        assert data[1]["object_filename"] == "report.docx"

        # Verify OCSClient was called correctly
        mock_client_instance.get_activities.assert_called_once()

    @patch("app.routes.ocs.settings.OCS_URL", "https://ocs.example.com")
    @patch("app.routes.ocs.settings.OCS_AUDIENCE", "ocs")
    @patch("app.routes.ocs.get_token")
    @patch("app.routes.ocs.OCSClient")
    def test_ocs_activities_empty_result(
        self,
        mock_ocs_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test activities endpoint with no activities."""
        # Mock token exchange
        mock_get_token.return_value = "test-ocs-token"

        # Mock OCSClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_activities.return_value = []
        mock_ocs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/ocs/activities")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    @patch("app.routes.ocs.settings.OCS_URL", "https://ocs.example.com")
    @patch("app.routes.ocs.settings.OCS_AUDIENCE", "ocs")
    @patch("app.routes.ocs.get_token")
    @patch("app.routes.ocs.OCSClient")
    def test_ocs_search_success(
        self,
        mock_ocs_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful search."""
        # Mock token exchange
        mock_get_token.return_value = "test-ocs-token"

        # Mock OCSClient
        mock_client_instance = AsyncMock()
        mock_client_instance.search_files.return_value = [
            SearchResults(
                name="Meeting notes.txt",
                url="/f/123",
            ),
            SearchResults(
                name="Project report.pdf",
                url="/f/456",
            ),
        ]
        mock_ocs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/ocs/search?term=meeting")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Meeting notes.txt"
        assert data[0]["url"] == "/f/123"
        assert data[1]["name"] == "Project report.pdf"
        assert data[1]["url"] == "/f/456"

        # Verify OCSClient was called correctly
        mock_client_instance.search_files.assert_called_once_with(term="meeting")

    @patch("app.routes.ocs.settings.OCS_URL", "https://ocs.example.com")
    @patch("app.routes.ocs.settings.OCS_AUDIENCE", "ocs")
    @patch("app.routes.ocs.get_token")
    @patch("app.routes.ocs.OCSClient")
    def test_ocs_search_empty_result(
        self,
        mock_ocs_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test search endpoint with no results."""
        # Mock token exchange
        mock_get_token.return_value = "test-ocs-token"

        # Mock OCSClient
        mock_client_instance = AsyncMock()
        mock_client_instance.search_files.return_value = []
        mock_ocs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/ocs/search?term=nonexistent")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_ocs_search_short_term(self, authenticated_client: TestClient) -> None:
        """Test search endpoint with term shorter than 4 characters."""
        response = authenticated_client.get("/api/v1/ocs/search?term=abc")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_ocs_search_missing_term(self, authenticated_client: TestClient) -> None:
        """Test search endpoint without term parameter."""
        response = authenticated_client.get("/api/v1/ocs/search")
        assert response.status_code == 422  # Validation error

    @patch("app.routes.ocs.settings.OCS_URL", "https://ocs.example.com")
    @patch("app.routes.ocs.settings.OCS_AUDIENCE", "ocs")
    @patch("app.routes.ocs.get_token")
    def test_ocs_activities_token_exchange_error(
        self,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test activities endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.get("/api/v1/ocs/activities")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.ocs.settings.OCS_URL", "https://ocs.example.com")
    @patch("app.routes.ocs.settings.OCS_AUDIENCE", "ocs")
    @patch("app.routes.ocs.get_token")
    def test_ocs_search_token_exchange_error(
        self,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test search endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.get("/api/v1/ocs/search?term=test")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.ocs.settings.OCS_URL", "https://ocs.example.com")
    @patch("app.routes.ocs.settings.OCS_AUDIENCE", "ocs")
    @patch("app.routes.ocs.get_token")
    @patch("app.routes.ocs.OCSClient")
    def test_ocs_activities_api_error(
        self,
        mock_ocs_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test activities endpoint when OCS API returns error."""
        from app.exceptions import ExternalServiceError

        # Mock token exchange
        mock_get_token.return_value = "test-ocs-token"

        # Mock OCSClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.get_activities.side_effect = ExternalServiceError("OCS", "API error")
        mock_ocs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/ocs/activities")

        assert response.status_code == 502  # ExternalServiceError returns 502

    @patch("app.routes.ocs.settings.OCS_URL", "https://ocs.example.com")
    @patch("app.routes.ocs.settings.OCS_AUDIENCE", "ocs")
    @patch("app.routes.ocs.get_token")
    @patch("app.routes.ocs.OCSClient")
    def test_ocs_search_api_error(
        self,
        mock_ocs_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test search endpoint when OCS API returns error."""
        from app.exceptions import ExternalServiceError

        # Mock token exchange
        mock_get_token.return_value = "test-ocs-token"

        # Mock OCSClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.search_files.side_effect = ExternalServiceError("OCS", "Search failed")
        mock_ocs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/ocs/search?term=test")

        assert response.status_code == 502  # ExternalServiceError returns 502
