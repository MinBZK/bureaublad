"""Tests for the OCS endpoints."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from app.models.activity import FileActivity, FileActivityResponse, FileInfo
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
        """Test successful file activities retrieval."""
        # Mock token exchange
        mock_get_token.return_value = "test-ocs-token"

        # Mock OCSClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_file_activities.return_value = FileActivityResponse(
            results=[
                FileActivity(
                    activity_id=123,
                    datetime=datetime(2024, 11, 1, 14, 15, 0),
                    action="file_changed",
                    files=[
                        FileInfo(
                            id=456,
                            name="document.pdf",
                            path="documents/document.pdf",
                            link="https://ocs.example.com/f/456",
                        ),
                    ],
                ),
                FileActivity(
                    activity_id=124,
                    datetime=datetime(2024, 11, 1, 10, 30, 0),
                    action="file_created",
                    files=[
                        FileInfo(
                            id=789,
                            name="report.docx",
                            path="reports/report.docx",
                            link="https://ocs.example.com/f/789",
                        ),
                    ],
                ),
            ],
            last_given=124,
        )
        mock_ocs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/ocs/activities")

        assert response.status_code == 200
        data = response.json()
        assert data["last_given"] == 124
        assert len(data["results"]) == 2
        assert data["results"][0]["activity_id"] == 123
        assert data["results"][0]["action"] == "file_changed"
        assert len(data["results"][0]["files"]) == 1
        assert data["results"][0]["files"][0]["id"] == 456
        assert data["results"][0]["files"][0]["name"] == "document.pdf"
        assert data["results"][0]["files"][0]["link"] == "https://ocs.example.com/f/456"
        assert data["results"][1]["activity_id"] == 124
        assert data["results"][1]["files"][0]["name"] == "report.docx"

        # Verify OCSClient was called correctly
        mock_client_instance.get_file_activities.assert_called_once()

    @patch("app.routes.ocs.settings.OCS_URL", "https://ocs.example.com")
    @patch("app.routes.ocs.settings.OCS_AUDIENCE", "ocs")
    @patch("app.routes.ocs.get_token")
    @patch("app.routes.ocs.OCSClient")
    def test_ocs_activities_multi_file(
        self,
        mock_ocs_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test file activities with multiple files per activity."""
        # Mock token exchange
        mock_get_token.return_value = "test-ocs-token"

        # Mock OCSClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_file_activities.return_value = FileActivityResponse(
            results=[
                FileActivity(
                    activity_id=2217,
                    datetime=datetime(2026, 1, 13, 16, 7, 43),
                    action="file_created",
                    files=[
                        FileInfo(
                            id=33485,
                            name="Drive.png",
                            path="Drive.png",
                            link="https://ocs.example.com/f/33485",
                        ),
                        FileInfo(
                            id=33482,
                            name="Docs.png",
                            path="Docs.png",
                            link="https://ocs.example.com/f/33482",
                        ),
                        FileInfo(
                            id=33483,
                            name="element.png",
                            path="element.png",
                            link="https://ocs.example.com/f/33483",
                        ),
                    ],
                ),
            ],
            last_given=2199,
        )
        mock_ocs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/ocs/activities")

        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 1
        activity = data["results"][0]
        assert activity["activity_id"] == 2217
        assert activity["action"] == "file_created"
        assert len(activity["files"]) == 3
        assert activity["files"][0]["name"] == "Drive.png"
        assert activity["files"][1]["name"] == "Docs.png"
        assert activity["files"][2]["name"] == "element.png"

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
        """Test activities endpoint with no file activities."""
        # Mock token exchange
        mock_get_token.return_value = "test-ocs-token"

        # Mock OCSClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_file_activities.return_value = FileActivityResponse(results=[], last_given=None)
        mock_ocs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/ocs/activities")

        assert response.status_code == 200
        data = response.json()
        assert data["results"] == []
        assert data["last_given"] is None

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
        mock_client_instance.get_file_activities.side_effect = ExternalServiceError("OCS", "API error")
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
