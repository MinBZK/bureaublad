"""Tests for the Grist client."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from app.clients.grist import GristClient
from app.exceptions import ExternalServiceError
from app.models.grist import GristDocument, GristOrganization, GristWorkspace


class TestGristClient:
    """Test cases for the GristClient class."""

    @pytest.fixture
    def mock_http_client(self) -> AsyncMock:
        """Create a mock HTTP client."""
        return AsyncMock(spec=httpx.AsyncClient)

    @pytest.fixture
    def grist_client(self, mock_http_client: AsyncMock) -> GristClient:
        """Create a GristClient instance for testing."""
        return GristClient(http_client=mock_http_client, base_url="https://grist.example.com", token="test-token")

    def test_init(self, mock_http_client: AsyncMock) -> None:
        """Test GristClient initialization."""
        client = GristClient(http_client=mock_http_client, base_url="https://grist.example.com/", token="test-token")

        assert client.client == mock_http_client
        assert client.base_url == "https://grist.example.com"  # Should strip trailing slash
        assert client.token == "test-token"

    def test_init_no_trailing_slash(self, mock_http_client: AsyncMock) -> None:
        """Test GristClient initialization without trailing slash."""
        client = GristClient(http_client=mock_http_client, base_url="https://grist.example.com", token="test-token")

        assert client.base_url == "https://grist.example.com"

    @pytest.mark.asyncio
    async def test_get_organizations_success(self, grist_client: GristClient, mock_http_client: AsyncMock) -> None:
        """Test successful organizations retrieval."""
        # Mock response data
        mock_response_data = [
            {
                "id": 1,
                "name": "Organization 1",
                "domain": "org1.grist.com",
                "access": "owners",
                "createdAt": "2024-01-01T10:00:00Z",
                "updatedAt": "2024-01-15T10:00:00Z",
            },
            {
                "id": 2,
                "name": "Organization 2",
                "domain": "org2.grist.com",
                "access": "editors",
                "createdAt": "2024-02-01T10:00:00Z",
                "updatedAt": "2024-02-15T10:00:00Z",
            },
        ]

        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_http_client.get.return_value = mock_response

        result = await grist_client.get_organizations()

        # Verify request was made correctly
        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://grist.example.com/api/orgs"
        assert call_args[1]["headers"] == {"Authorization": "Bearer test-token"}

        # Verify result
        assert len(result) == 2
        assert isinstance(result[0], GristOrganization)
        assert result[0].id == 1
        assert result[0].name == "Organization 1"
        assert result[0].domain == "org1.grist.com"
        assert result[0].access == "owners"
        assert result[1].id == 2
        assert result[1].name == "Organization 2"

    @pytest.mark.asyncio
    async def test_get_organizations_custom_path(self, grist_client: GristClient, mock_http_client: AsyncMock) -> None:
        """Test organizations retrieval with custom path."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_http_client.get.return_value = mock_response

        await grist_client.get_organizations("custom/path")

        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://grist.example.com/custom/path"
        assert call_args[1]["headers"] == {"Authorization": "Bearer test-token"}

    @pytest.mark.asyncio
    async def test_get_organizations_with_leading_slash_path(
        self, grist_client: GristClient, mock_http_client: AsyncMock
    ) -> None:
        """Test organizations retrieval with path starting with slash."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_http_client.get.return_value = mock_response

        await grist_client.get_organizations("/custom/path")

        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://grist.example.com/custom/path"
        assert call_args[1]["headers"] == {"Authorization": "Bearer test-token"}

    @pytest.mark.asyncio
    async def test_get_organizations_http_error(self, grist_client: GristClient, mock_http_client: AsyncMock) -> None:
        """Test organizations retrieval with HTTP error."""
        mock_http_client.get.side_effect = httpx.HTTPError("Connection failed")

        with pytest.raises(ExternalServiceError) as exc_info:
            await grist_client.get_organizations()

        assert "Grist service error" in str(exc_info.value.detail)
        assert "HTTP error" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_organizations_api_error(self, grist_client: GristClient, mock_http_client: AsyncMock) -> None:
        """Test organizations retrieval with API error response."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_http_client.get.return_value = mock_response

        with pytest.raises(ExternalServiceError) as exc_info:
            await grist_client.get_organizations()

        assert "Grist service error" in str(exc_info.value.detail)
        assert "Failed to fetch api/orgs (status 404)" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_workspaces_success(self, grist_client: GristClient, mock_http_client: AsyncMock) -> None:
        """Test successful workspaces retrieval."""
        mock_response_data = [
            {
                "id": 1,
                "name": "Workspace 1",
                "access": "owners",
                "orgDomain": "org1.grist.com",
                "docs": [
                    {
                        "id": "doc1",
                        "name": "Document 1",
                        "access": "owners",
                        "isPinned": True,
                        "urlId": "url-doc1",
                        "createdAt": "2024-01-01T10:00:00Z",
                        "updatedAt": "2024-01-20T10:00:00Z",
                    }
                ],
            }
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_http_client.get.return_value = mock_response

        result = await grist_client.get_workspaces(organization_id=123)

        # Verify request
        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://grist.example.com/api/orgs/123/workspaces"
        assert call_args[1]["headers"] == {"Authorization": "Bearer test-token"}

        # Verify result
        assert len(result) == 1
        assert isinstance(result[0], GristWorkspace)
        assert result[0].id == 1
        assert result[0].name == "Workspace 1"
        assert result[0].access == "owners"
        assert result[0].org_domain == "org1.grist.com"
        assert len(result[0].docs) == 1
        assert isinstance(result[0].docs[0], GristDocument)
        assert result[0].docs[0].id == "doc1"

    @pytest.mark.asyncio
    async def test_get_workspaces_http_error(self, grist_client: GristClient, mock_http_client: AsyncMock) -> None:
        """Test workspaces retrieval with HTTP error."""
        mock_http_client.get.side_effect = httpx.HTTPError("Connection failed")

        with pytest.raises(ExternalServiceError) as exc_info:
            await grist_client.get_workspaces(123)

        assert "Grist service error" in str(exc_info.value.detail)
        assert "HTTP error" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_documents_success(self, grist_client: GristClient, mock_http_client: AsyncMock) -> None:
        """Test successful documents retrieval with pagination."""
        # Mock workspaces response
        mock_workspaces_data = [
            {
                "id": 1,
                "name": "Workspace 1",
                "access": "owners",
                "orgDomain": "org1.grist.com",
                "docs": [
                    {
                        "id": "doc1",
                        "name": "Document 1",
                        "access": "owners",
                        "isPinned": True,
                        "urlId": "url-doc1",
                        "createdAt": "2024-01-01T10:00:00Z",
                        "updatedAt": "2024-01-20T10:00:00Z",  # Most recent
                    },
                    {
                        "id": "doc2",
                        "name": "Document 2",
                        "access": "editors",
                        "isPinned": False,
                        "urlId": "url-doc2",
                        "createdAt": "2024-01-02T10:00:00Z",
                        "updatedAt": "2024-01-15T10:00:00Z",  # Older
                    },
                ],
            },
            {
                "id": 2,
                "name": "Workspace 2",
                "access": "editors",
                "orgDomain": "org1.grist.com",
                "docs": [
                    {
                        "id": "doc3",
                        "name": "Document 3",
                        "access": "viewers",
                        "isPinned": False,
                        "urlId": "url-doc3",
                        "createdAt": "2024-01-03T10:00:00Z",
                        "updatedAt": "2024-01-18T10:00:00Z",  # Middle
                    }
                ],
            },
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_workspaces_data
        mock_http_client.get.return_value = mock_response

        result = await grist_client.get_documents(organization_id=123, page=1, page_size=2)

        # Verify request
        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://grist.example.com/api/orgs/123/workspaces"
        assert call_args[1]["headers"] == {"Authorization": "Bearer test-token"}

        # Verify result - should be sorted by updated_at descending and paginated
        assert len(result) == 2
        assert result[0].id == "doc1"  # Most recent (2024-01-20)
        assert result[1].id == "doc3"  # Middle (2024-01-18)
        # doc2 should not be included due to page_size=2

    @pytest.mark.asyncio
    async def test_get_documents_pagination_page_2(
        self, grist_client: GristClient, mock_http_client: AsyncMock
    ) -> None:
        """Test documents retrieval for page 2."""
        mock_workspaces_data = [
            {
                "id": 1,
                "name": "Workspace 1",
                "access": "owners",
                "orgDomain": "org1.grist.com",
                "docs": [
                    {
                        "id": "doc1",
                        "name": "Document 1",
                        "access": "owners",
                        "isPinned": True,
                        "urlId": "url-doc1",
                        "createdAt": "2024-01-01T10:00:00Z",
                        "updatedAt": "2024-01-20T10:00:00Z",
                    },
                    {
                        "id": "doc2",
                        "name": "Document 2",
                        "access": "editors",
                        "isPinned": False,
                        "urlId": "url-doc2",
                        "createdAt": "2024-01-02T10:00:00Z",
                        "updatedAt": "2024-01-15T10:00:00Z",
                    },
                    {
                        "id": "doc3",
                        "name": "Document 3",
                        "access": "viewers",
                        "isPinned": False,
                        "urlId": "url-doc3",
                        "createdAt": "2024-01-03T10:00:00Z",
                        "updatedAt": "2024-01-10T10:00:00Z",
                    },
                ],
            }
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_workspaces_data
        mock_http_client.get.return_value = mock_response

        result = await grist_client.get_documents(organization_id=123, page=2, page_size=2)

        # Should get the third document (page 2, offset 2)
        assert len(result) == 1
        assert result[0].id == "doc3"

    @pytest.mark.asyncio
    async def test_get_documents_empty_result(self, grist_client: GristClient, mock_http_client: AsyncMock) -> None:
        """Test documents retrieval with no documents."""
        mock_workspaces_data = [
            {"id": 1, "name": "Workspace 1", "access": "owners", "orgDomain": "org1.grist.com", "docs": []}
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_workspaces_data
        mock_http_client.get.return_value = mock_response

        result = await grist_client.get_documents(organization_id=123)

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_documents_page_out_of_bounds(
        self, grist_client: GristClient, mock_http_client: AsyncMock
    ) -> None:
        """Test documents retrieval with page out of bounds."""
        mock_workspaces_data = [
            {
                "id": 1,
                "name": "Workspace 1",
                "access": "owners",
                "orgDomain": "org1.grist.com",
                "docs": [
                    {
                        "id": "doc1",
                        "name": "Document 1",
                        "access": "owners",
                        "isPinned": True,
                        "urlId": "url-doc1",
                        "createdAt": "2024-01-01T10:00:00Z",
                        "updatedAt": "2024-01-20T10:00:00Z",
                    }
                ],
            }
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_workspaces_data
        mock_http_client.get.return_value = mock_response

        result = await grist_client.get_documents(organization_id=123, page=10, page_size=5)

        # Should return empty list when page is out of bounds
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_documents_invalid_page_defaults(
        self, grist_client: GristClient, mock_http_client: AsyncMock
    ) -> None:
        """Test documents retrieval with invalid page parameters."""
        mock_workspaces_data = [
            {
                "id": 1,
                "name": "Workspace 1",
                "access": "owners",
                "orgDomain": "org1.grist.com",
                "docs": [
                    {
                        "id": "doc1",
                        "name": "Document 1",
                        "access": "owners",
                        "isPinned": True,
                        "urlId": "url-doc1",
                        "createdAt": "2024-01-01T10:00:00Z",
                        "updatedAt": "2024-01-20T10:00:00Z",
                    }
                ],
            }
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_workspaces_data
        mock_http_client.get.return_value = mock_response

        # Test negative page number
        result = await grist_client.get_documents(organization_id=123, page=-1, page_size=0)

        # Should default to page=1, page_size=1 and return first document
        assert len(result) == 1
        assert result[0].id == "doc1"

    @pytest.mark.parametrize(
        ("page", "page_size", "expected_page", "expected_page_size"),
        [
            (0, 5, 1, 5),  # Page 0 should default to 1
            (-1, 5, 1, 5),  # Negative page should default to 1
            (2, 0, 2, 1),  # Page size 0 should default to 1
            (2, -1, 2, 1),  # Negative page size should default to 1
            (1, 3, 1, 3),  # Valid values should remain unchanged
        ],
    )
    @pytest.mark.asyncio
    async def test_get_documents_parameter_validation(
        self,
        grist_client: GristClient,
        mock_http_client: AsyncMock,
        page: int,
        page_size: int,
        expected_page: int,
        expected_page_size: int,
    ) -> None:
        """Test parameter validation for get_documents method."""
        mock_workspaces_data = [
            {
                "id": 1,
                "name": "Workspace 1",
                "access": "owners",
                "orgDomain": "org1.grist.com",
                "docs": [
                    {
                        "id": f"doc{i}",
                        "name": f"Document {i}",
                        "access": "owners",
                        "isPinned": False,
                        "urlId": f"url-doc{i}",
                        "createdAt": f"2024-01-0{i}T10:00:00Z",
                        "updatedAt": f"2024-01-1{i}T10:00:00Z",
                    }
                    for i in range(1, 6)  # Create 5 documents
                ],
            }
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_workspaces_data
        mock_http_client.get.return_value = mock_response

        result = await grist_client.get_documents(123, page, page_size)

        # Calculate expected offset and results
        offset = (expected_page - 1) * expected_page_size
        expected_count = min(expected_page_size, max(0, 5 - offset))

        assert len(result) == expected_count
