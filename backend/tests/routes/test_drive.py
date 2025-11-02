"""Tests for the Drive endpoints."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
from app.models.document import Document
from fastapi.testclient import TestClient


class TestDriveEndpoints:
    """Test cases for Drive endpoints."""

    def test_drive_documents_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that documents endpoint requires authentication."""
        response = fresh_client.get("/api/v1/drive/documents")
        assert response.status_code == 401

    @patch("app.routes.drive.settings.DRIVE_URL", None)
    def test_drive_documents_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test documents endpoint when service is disabled."""
        response = authenticated_client.get("/api/v1/drive/documents")
        assert response.status_code == 503

    @patch("app.routes.drive.settings.DRIVE_URL", "https://drive.example.com")
    @patch("app.routes.drive.settings.DRIVE_AUDIENCE", "drive")
    @patch("app.routes.drive.get_token")
    @patch("app.routes.drive.DriveClient")
    def test_drive_documents_success(
        self,
        mock_drive_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful documents retrieval."""
        # Mock token exchange
        mock_get_token.return_value = "test-drive-token"

        # Mock DriveClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            Document(
                title="Project Report.docx",
                url="https://drive.example.com/files/doc-123",
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                updated_at="2024-11-01T10:00:00Z",
            ),
            Document(
                title="Presentation.pptx",
                url="https://drive.example.com/files/doc-456",
                mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                updated_at="2024-11-01T11:00:00Z",
            ),
        ]
        mock_drive_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/drive/documents")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Project Report.docx"
        assert data[0]["mimetype"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        assert data[1]["title"] == "Presentation.pptx"
        assert data[1]["mimetype"] == "application/vnd.openxmlformats-officedocument.presentationml.presentation"

        # Verify DriveClient was called correctly
        mock_client_instance.get_documents.assert_called_once_with(title=None, is_favorite=False)

    @patch("app.routes.drive.settings.DRIVE_URL", "https://drive.example.com")
    @patch("app.routes.drive.settings.DRIVE_AUDIENCE", "drive")
    @patch("app.routes.drive.get_token")
    @patch("app.routes.drive.DriveClient")
    def test_drive_documents_with_title_filter(
        self,
        mock_drive_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents retrieval with title filter."""
        # Mock token exchange
        mock_get_token.return_value = "test-drive-token"

        # Mock DriveClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            Document(
                title="Filtered Document.pdf",
                url="https://drive.example.com/files/doc-789",
                mimetype="application/pdf",
                updated_at="2024-11-01T12:00:00Z",
            )
        ]
        mock_drive_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/drive/documents?title=Filtered%20Document")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Filtered Document.pdf"
        assert data[0]["mimetype"] == "application/pdf"

        # Verify DriveClient was called with title filter
        mock_client_instance.get_documents.assert_called_once_with(title="Filtered Document", is_favorite=False)

    @patch("app.routes.drive.settings.DRIVE_URL", "https://drive.example.com")
    @patch("app.routes.drive.settings.DRIVE_AUDIENCE", "drive")
    @patch("app.routes.drive.get_token")
    @patch("app.routes.drive.DriveClient")
    def test_drive_documents_with_favorite_filter(
        self,
        mock_drive_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents retrieval with is_favorite filter."""
        # Mock token exchange
        mock_get_token.return_value = "test-drive-token"

        # Mock DriveClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            Document(
                title="Favorite Spreadsheet.xlsx",
                url="https://drive.example.com/files/doc-101",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                updated_at="2024-11-01T13:00:00Z",
            )
        ]
        mock_drive_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/drive/documents?is_favorite=true")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Favorite Spreadsheet.xlsx"
        assert data[0]["mimetype"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        # Verify DriveClient was called with is_favorite=True
        mock_client_instance.get_documents.assert_called_once_with(title=None, is_favorite=True)

    @patch("app.routes.drive.settings.DRIVE_URL", "https://drive.example.com")
    @patch("app.routes.drive.settings.DRIVE_AUDIENCE", "drive")
    @patch("app.routes.drive.get_token")
    @patch("app.routes.drive.DriveClient")
    def test_drive_documents_with_combined_filters(
        self,
        mock_drive_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents retrieval with both title and favorite filters."""
        # Mock token exchange
        mock_get_token.return_value = "test-drive-token"

        # Mock DriveClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            Document(
                title="Important Document.pdf",
                url="https://drive.example.com/files/doc-202",
                mimetype="application/pdf",
                updated_at="2024-11-01T14:00:00Z",
            )
        ]
        mock_drive_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/drive/documents?title=Important&is_favorite=true")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Important Document.pdf"

        # Verify DriveClient was called with both filters
        mock_client_instance.get_documents.assert_called_once_with(title="Important", is_favorite=True)

    @patch("app.routes.drive.settings.DRIVE_URL", "https://drive.example.com")
    @patch("app.routes.drive.settings.DRIVE_AUDIENCE", "drive")
    @patch("app.routes.drive.get_token")
    @patch("app.routes.drive.DriveClient")
    def test_drive_documents_empty_result(
        self,
        mock_drive_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint with empty result."""
        # Mock token exchange
        mock_get_token.return_value = "test-drive-token"

        # Mock DriveClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = []
        mock_drive_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/drive/documents")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    @patch("app.routes.drive.settings.DRIVE_URL", "https://drive.example.com")
    @patch("app.routes.drive.settings.DRIVE_AUDIENCE", "drive")
    @patch("app.routes.drive.get_token")
    def test_drive_documents_token_exchange_error(
        self,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.get("/api/v1/drive/documents")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.drive.settings.DRIVE_URL", "https://drive.example.com")
    @patch("app.routes.drive.settings.DRIVE_AUDIENCE", "drive")
    @patch("app.routes.drive.get_token")
    @patch("app.routes.drive.DriveClient")
    def test_drive_documents_client_error(
        self,
        mock_drive_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint when DriveClient raises an exception."""
        # Mock token exchange
        mock_get_token.return_value = "test-drive-token"

        # Mock DriveClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.side_effect = httpx.HTTPError("Drive service error")
        mock_drive_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/drive/documents")

        assert response.status_code == 502  # HTTPError returns 502 Bad Gateway

    @patch("app.routes.drive.settings.DRIVE_URL", "https://drive.example.com")
    @patch("app.routes.drive.settings.DRIVE_AUDIENCE", "drive")
    @patch("app.routes.drive.get_token")
    @patch("app.routes.drive.DriveClient")
    def test_drive_documents_with_computed_fields(
        self,
        mock_drive_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint returns computed fields correctly."""
        # Mock token exchange
        mock_get_token.return_value = "test-drive-token"

        # Mock DriveClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            Document(
                title="Test Computed Fields.docx",
                url="https://drive.example.com/files/doc-computed",
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                updated_at="2024-11-01T15:30:00Z",
            )
        ]
        mock_drive_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/drive/documents")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Computed Fields.docx"
        assert data[0]["url"] == "https://drive.example.com/files/doc-computed"
        assert data[0]["mimetype"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        assert data[0]["updated_at"] == "2024-11-01T15:30:00Z"

        # Verify computed field is included
        assert "updated_date" in data[0]
        assert data[0]["updated_date"] == "01 Nov 2024 15:30"

    @patch("app.routes.drive.settings.DRIVE_URL", "https://drive.example.com")
    @patch("app.routes.drive.settings.DRIVE_AUDIENCE", "drive")
    @patch("app.routes.drive.get_token")
    @patch("app.routes.drive.DriveClient")
    def test_drive_documents_various_mimetypes(
        self,
        mock_drive_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint with various file types and mimetypes."""
        # Mock token exchange
        mock_get_token.return_value = "test-drive-token"

        # Mock DriveClient with various document types
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            Document(
                title="Document.pdf",
                url="https://drive.example.com/files/pdf-1",
                mimetype="application/pdf",
                updated_at="2024-11-01T16:00:00Z",
            ),
            Document(
                title="Spreadsheet.xlsx",
                url="https://drive.example.com/files/excel-1",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                updated_at="2024-11-01T16:15:00Z",
            ),
            Document(
                title="Presentation.pptx",
                url="https://drive.example.com/files/powerpoint-1",
                mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                updated_at="2024-11-01T16:30:00Z",
            ),
            Document(
                title="Text.txt",
                url="https://drive.example.com/files/text-1",
                mimetype="text/plain",
                updated_at="2024-11-01T16:45:00Z",
            ),
        ]
        mock_drive_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/drive/documents")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4

        # Verify different file types
        file_types = {doc["title"]: doc["mimetype"] for doc in data}
        assert file_types["Document.pdf"] == "application/pdf"
        assert file_types["Spreadsheet.xlsx"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        assert (
            file_types["Presentation.pptx"]
            == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        assert file_types["Text.txt"] == "text/plain"

    # Test the service disabled check in the route itself (redundant check)
    @patch("app.routes.drive.settings.DRIVE_URL", None)
    def test_drive_documents_route_level_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test the redundant service disabled check in the route itself."""
        response = authenticated_client.get("/api/v1/drive/documents")
        assert response.status_code == 503
