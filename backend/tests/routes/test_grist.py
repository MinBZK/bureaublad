"""Tests for the Grist endpoints."""

from unittest.mock import AsyncMock, MagicMock, patch

from app.models.grist import GristDocument, GristOrganization
from fastapi.testclient import TestClient


class TestGristEndpoints:
    """Test cases for Grist endpoints."""

    def test_grist_orgs_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that organizations endpoint requires authentication."""
        response = fresh_client.get("/api/v1/grist/orgs")
        assert response.status_code == 401

    def test_grist_docs_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that documents endpoint requires authentication."""
        response = fresh_client.get("/api/v1/grist/docs?organization_id=1")
        assert response.status_code == 401

    @patch("app.routes.grist.settings.GRIST_URL", None)
    def test_grist_orgs_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test organizations endpoint when service is disabled."""
        response = authenticated_client.get("/api/v1/grist/orgs")
        assert response.status_code == 503

    @patch("app.routes.grist.settings.GRIST_URL", None)
    def test_grist_docs_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test documents endpoint when service is disabled."""
        response = authenticated_client.get("/api/v1/grist/docs?organization_id=1")
        assert response.status_code == 503

    @patch("app.routes.grist.settings.GRIST_URL", "https://grist.example.com")
    @patch("app.routes.grist.settings.GRIST_AUDIENCE", "grist")
    @patch("app.routes.grist.get_token")
    @patch("app.routes.grist.GristClient")
    def test_grist_orgs_success(
        self,
        mock_grist_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful organizations retrieval."""
        # Mock token exchange
        mock_get_token.return_value = "test-grist-token"

        # Mock GristClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_organizations.return_value = [
            GristOrganization(
                id=1,
                name="Organization 1",
                domain="org1.grist.com",
                access="owners",
                created_at="2024-01-01T10:00:00Z",
                updated_at="2024-01-15T10:00:00Z",
            ),
            GristOrganization(
                id=2,
                name="Organization 2",
                domain="org2.grist.com",
                access="editors",
                created_at="2024-02-01T10:00:00Z",
                updated_at="2024-02-15T10:00:00Z",
            ),
        ]
        mock_grist_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/grist/orgs")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[0]["name"] == "Organization 1"
        assert data[0]["domain"] == "org1.grist.com"
        assert data[0]["access"] == "owners"
        assert data[1]["id"] == 2
        assert data[1]["name"] == "Organization 2"

        # Verify GristClient was called correctly
        mock_client_instance.get_organizations.assert_called_once()

    @patch("app.routes.grist.settings.GRIST_URL", "https://grist.example.com")
    @patch("app.routes.grist.settings.GRIST_AUDIENCE", "grist")
    @patch("app.routes.grist.get_token")
    @patch("app.routes.grist.GristClient")
    def test_grist_docs_success(
        self,
        mock_grist_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful documents retrieval with pagination."""
        # Mock token exchange
        mock_get_token.return_value = "test-grist-token"

        # Mock GristClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            GristDocument(
                id="doc1",
                name="Document 1",
                access="owners",
                is_pinned=True,
                url_id="url-doc1",
                created_at="2024-01-01T10:00:00Z",
                updated_at="2024-01-20T10:00:00Z",
            ),
            GristDocument(
                id="doc2",
                name="Document 2",
                access="editors",
                is_pinned=False,
                url_id="url-doc2",
                created_at="2024-01-02T10:00:00Z",
                updated_at="2024-01-15T10:00:00Z",
            ),
        ]
        mock_grist_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/grist/docs?organization_id=1&page=1&page_size=5")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        # Should be sorted by updated_at (most recent first)
        assert data[0]["id"] == "doc1"  # Updated 2024-01-20
        assert data[0]["name"] == "Document 1"
        assert data[0]["isPinned"] is True
        assert data[0]["url"] == "https://grist.example.com/url-doc1/"
        assert data[1]["id"] == "doc2"  # Updated 2024-01-15
        assert data[1]["name"] == "Document 2"
        assert data[1]["isPinned"] is False

        # Verify GristClient was called correctly
        mock_client_instance.get_documents.assert_called_once_with(1, 1, 5)

    @patch("app.routes.grist.settings.GRIST_URL", "https://grist.example.com")
    @patch("app.routes.grist.settings.GRIST_AUDIENCE", "grist")
    @patch("app.routes.grist.get_token")
    @patch("app.routes.grist.GristClient")
    def test_grist_docs_pagination(
        self,
        mock_grist_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint with pagination."""
        # Mock token exchange
        mock_get_token.return_value = "test-grist-token"

        # Mock GristClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = [
            GristDocument(
                id="doc7",
                name="Document 7",
                access="owners",
                is_pinned=False,
                url_id="url-doc7",
                created_at="2024-01-01T10:00:00Z",
                updated_at="2024-01-07T10:00:00Z",
            ),
            GristDocument(
                id="doc6",
                name="Document 6",
                access="owners",
                is_pinned=False,
                url_id="url-doc6",
                created_at="2024-01-01T10:00:00Z",
                updated_at="2024-01-06T10:00:00Z",
            ),
            GristDocument(
                id="doc5",
                name="Document 5",
                access="owners",
                is_pinned=False,
                url_id="url-doc5",
                created_at="2024-01-01T10:00:00Z",
                updated_at="2024-01-05T10:00:00Z",
            ),
        ]
        mock_grist_client.return_value = mock_client_instance

        # Test page 1 with page_size 3
        response = authenticated_client.get("/api/v1/grist/docs?organization_id=1&page=1&page_size=3")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        # Should get the 3 most recent documents (doc7, doc6, doc5)
        assert data[0]["id"] == "doc7"
        assert data[1]["id"] == "doc6"
        assert data[2]["id"] == "doc5"

    @patch("app.routes.grist.settings.GRIST_URL", "https://grist.example.com")
    @patch("app.routes.grist.settings.GRIST_AUDIENCE", "grist")
    @patch("app.routes.grist.get_token")
    @patch("app.routes.grist.GristClient")
    def test_grist_docs_default_pagination(
        self,
        mock_grist_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint with default pagination parameters."""
        # Mock token exchange
        mock_get_token.return_value = "test-grist-token"

        # Mock GristClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.return_value = []
        mock_grist_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/grist/docs?organization_id=1")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    @patch("app.routes.grist.settings.GRIST_URL", "https://grist.example.com")
    @patch("app.routes.grist.settings.GRIST_AUDIENCE", "grist")
    @patch("app.routes.grist.get_token")
    @patch("app.routes.grist.GristClient")
    def test_grist_orgs_empty_result(
        self,
        mock_grist_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test organizations endpoint with no organizations."""
        # Mock token exchange
        mock_get_token.return_value = "test-grist-token"

        # Mock GristClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_organizations.return_value = []
        mock_grist_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/grist/orgs")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_grist_docs_missing_organization_id(self, authenticated_client: TestClient) -> None:
        """Test documents endpoint without organization_id parameter."""
        response = authenticated_client.get("/api/v1/grist/docs")
        assert response.status_code == 422  # Validation error

    @patch("app.routes.grist.settings.GRIST_URL", "https://grist.example.com")
    @patch("app.routes.grist.settings.GRIST_AUDIENCE", "grist")
    @patch("app.routes.grist.get_token")
    def test_grist_orgs_token_exchange_error(
        self,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test organizations endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.get("/api/v1/grist/orgs")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.grist.settings.GRIST_URL", "https://grist.example.com")
    @patch("app.routes.grist.settings.GRIST_AUDIENCE", "grist")
    @patch("app.routes.grist.get_token")
    def test_grist_docs_token_exchange_error(
        self,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.get("/api/v1/grist/docs?organization_id=1")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.grist.settings.GRIST_URL", "https://grist.example.com")
    @patch("app.routes.grist.settings.GRIST_AUDIENCE", "grist")
    @patch("app.routes.grist.get_token")
    @patch("app.routes.grist.GristClient")
    def test_grist_orgs_api_error(
        self,
        mock_grist_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test organizations endpoint when Grist API returns error."""
        from app.exceptions import ExternalServiceError

        # Mock token exchange
        mock_get_token.return_value = "test-grist-token"

        # Mock GristClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.get_organizations.side_effect = ExternalServiceError("Grist", "API error")
        mock_grist_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/grist/orgs")

        assert response.status_code == 502  # ExternalServiceError returns 502

    @patch("app.routes.grist.settings.GRIST_URL", "https://grist.example.com")
    @patch("app.routes.grist.settings.GRIST_AUDIENCE", "grist")
    @patch("app.routes.grist.get_token")
    @patch("app.routes.grist.GristClient")
    def test_grist_docs_api_error(
        self,
        mock_grist_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test documents endpoint when Grist API returns error."""
        from app.exceptions import ExternalServiceError

        # Mock token exchange
        mock_get_token.return_value = "test-grist-token"

        # Mock GristClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.get_documents.side_effect = ExternalServiceError("Grist", "Organization not found")
        mock_grist_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/grist/docs?organization_id=999")

        assert response.status_code == 502  # ExternalServiceError returns 502
