"""Tests for the Docs endpoints."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
from app.models.note import Note
from fastapi.testclient import TestClient


class TestDocsEndpoints:
    """Test cases for Docs endpoints."""

    def test_docs_get_documents_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that documents endpoint requires authentication."""
        response = fresh_client.get("/api/v1/docs/documents")
        assert response.status_code == 401

    @patch("app.routes.docs.settings.DOCS_URL", None)
    def test_docs_get_documents_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test documents endpoint when service is disabled."""
        response = authenticated_client.get("/api/v1/docs/documents")
        assert response.status_code == 503

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    @patch("app.routes.docs.DocsClient")
    def test_docs_get_documents_success(
        self,
        mock_docs_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful documents retrieval."""
        # Mock token exchange
        mock_get_token.return_value = "test-docs-token"

        # Mock DocsClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            Note(
                id="doc-123",
                created_at="2024-11-01T10:00:00Z",
                path="/documents/doc-123",
                title="Test Document",
                updated_at="2024-11-01T10:00:00Z",
                user_role="owner",
            )
        ]
        mock_docs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/docs/documents")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "doc-123"
        assert data[0]["title"] == "Test Document"
        assert data[0]["user_role"] == "owner"

        # Verify DocsClient was called correctly
        mock_client_instance.get_documents.assert_called_once_with(title=None, is_favorite=False)

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    @patch("app.routes.docs.DocsClient")
    def test_docs_get_documents_with_title_filter(
        self,
        mock_docs_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents retrieval with title filter."""
        # Mock token exchange
        mock_get_token.return_value = "test-docs-token"

        # Mock DocsClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            Note(
                id="doc-456",
                created_at="2024-11-01T11:00:00Z",
                path="/documents/doc-456",
                title="Filtered Document",
                updated_at="2024-11-01T11:00:00Z",
                user_role="editor",
            )
        ]
        mock_docs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/docs/documents?title=Filtered%20Document")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Filtered Document"

        # Verify DocsClient was called with title filter
        mock_client_instance.get_documents.assert_called_once_with(title="Filtered Document", is_favorite=False)

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    @patch("app.routes.docs.DocsClient")
    def test_docs_get_documents_with_favorite_filter(
        self,
        mock_docs_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents retrieval with is_favorite filter."""
        # Mock token exchange
        mock_get_token.return_value = "test-docs-token"

        # Mock DocsClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            Note(
                id="doc-789",
                created_at="2024-11-01T12:00:00Z",
                path="/documents/doc-789",
                title="Favorite Document",
                updated_at="2024-11-01T12:00:00Z",
                user_role="owner",
            )
        ]
        mock_docs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/docs/documents?is_favorite=true")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Favorite Document"

        # Verify DocsClient was called with is_favorite=True
        mock_client_instance.get_documents.assert_called_once_with(title=None, is_favorite=True)

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    @patch("app.routes.docs.DocsClient")
    def test_docs_get_documents_empty_result(
        self,
        mock_docs_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint with empty result."""
        # Mock token exchange
        mock_get_token.return_value = "test-docs-token"

        # Mock DocsClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = []
        mock_docs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/docs/documents")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    def test_docs_get_documents_token_exchange_error(
        self,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.get("/api/v1/docs/documents")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    @patch("app.routes.docs.DocsClient")
    def test_docs_get_documents_client_error(
        self,
        mock_docs_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint when DocsClient raises an exception."""
        # Mock token exchange
        mock_get_token.return_value = "test-docs-token"

        # Mock DocsClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.side_effect = httpx.HTTPError("Docs service error")
        mock_docs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/docs/documents")

        assert response.status_code == 502  # HTTPError returns 502 Bad Gateway

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    @patch("app.routes.docs.DocsClient")
    def test_docs_get_documents_with_computed_fields(
        self,
        mock_docs_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint returns computed fields correctly."""
        # Mock token exchange
        mock_get_token.return_value = "test-docs-token"

        # Mock DocsClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            Note(
                id="doc-computed",
                created_at="2024-11-01T10:00:00Z",
                path="/documents/doc-computed",
                title="Test Computed Fields",
                updated_at="2024-11-01T10:30:00Z",
                user_role="owner",
            )
        ]
        mock_docs_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/docs/documents")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "doc-computed"
        assert data[0]["title"] == "Test Computed Fields"
        assert data[0]["updated_at"] == "2024-11-01T10:30:00Z"

        # Verify computed fields are included
        assert "url" in data[0]
        assert data[0]["url"] == "https://docs.example.com/docs/doc-computed/"
        assert "updated_date" in data[0]
        assert data[0]["updated_date"] == "01 Nov 2024 10:30"

    # POST /docs/documents tests

    def test_docs_post_documents_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that POST documents endpoint requires authentication."""
        response = fresh_client.post("/api/v1/docs/documents")
        assert response.status_code == 401

    @patch("app.routes.docs.settings.DOCS_URL", None)
    def test_docs_post_documents_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test POST documents endpoint when service is disabled."""
        response = authenticated_client.post("/api/v1/docs/documents")
        assert response.status_code == 503

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    @patch("app.routes.docs.DocsClient")
    def test_docs_post_documents_success(
        self,
        mock_docs_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful document creation."""
        # Mock token exchange
        mock_get_token.return_value = "test-docs-token"

        # Mock DocsClient
        mock_client_instance = AsyncMock()
        mock_client_instance.post_document.return_value = Note(
            id="new-doc-123",
            created_at="2024-11-01T15:00:00Z",
            path="/documents/new-doc-123",
            title="New Document",
            updated_at="2024-11-01T15:00:00Z",
            user_role="owner",
        )
        mock_docs_client.return_value = mock_client_instance

        response = authenticated_client.post("/api/v1/docs/documents")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "new-doc-123"
        assert data["title"] == "New Document"
        assert data["user_role"] == "owner"

        # Verify DocsClient was called correctly
        mock_client_instance.post_document.assert_called_once()

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    def test_docs_post_documents_token_exchange_error(
        self,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test POST documents endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.post("/api/v1/docs/documents")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    @patch("app.routes.docs.DocsClient")
    def test_docs_post_documents_client_error(
        self,
        mock_docs_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test POST documents endpoint when DocsClient raises an exception."""
        # Mock token exchange
        mock_get_token.return_value = "test-docs-token"

        # Mock DocsClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.post_document.side_effect = httpx.HTTPError("Docs service error")
        mock_docs_client.return_value = mock_client_instance

        response = authenticated_client.post("/api/v1/docs/documents")

        assert response.status_code == 502  # HTTPError returns 502 Bad Gateway

    @patch("app.routes.docs.settings.DOCS_URL", "https://docs.example.com")
    @patch("app.routes.docs.settings.DOCS_AUDIENCE", "docs")
    @patch("app.routes.docs.get_token")
    @patch("app.routes.docs.DocsClient")
    def test_docs_post_documents_external_service_error(
        self,
        mock_docs_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test POST documents endpoint when external service returns an error."""
        from app.exceptions import ExternalServiceError

        # Mock token exchange
        mock_get_token.return_value = "test-docs-token"

        # Mock DocsClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.post_document.side_effect = ExternalServiceError("Docs", "Failed to create document")
        mock_docs_client.return_value = mock_client_instance

        response = authenticated_client.post("/api/v1/docs/documents")

        assert response.status_code == 502  # ExternalServiceError returns 502
