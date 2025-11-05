"""Tests for Drive client."""

from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from app.clients.drive import DriveClient
from app.models.document import Document


class TestDriveClient:
    """Tests for DriveClient class."""

    @pytest.fixture
    def mock_http_client(self) -> AsyncMock:
        """Create a mock HTTP client."""
        return AsyncMock(spec=httpx.AsyncClient)

    @pytest.fixture
    def client(self, mock_http_client: AsyncMock) -> DriveClient:
        """Create a DriveClient instance for testing."""
        return DriveClient(
            http_client=mock_http_client,
            base_url="https://drive.example.com",
            token="test-token",
        )

    def test_init(self, mock_http_client: AsyncMock, client: DriveClient) -> None:
        """Test DriveClient initialization."""
        assert client.client is mock_http_client
        assert client.base_url == "https://drive.example.com"
        assert client.token == "test-token"

    def test_init_strips_trailing_slash(self, mock_http_client: AsyncMock) -> None:
        """Test that trailing slash is stripped from base_url."""
        client = DriveClient(
            http_client=mock_http_client,
            base_url="https://drive.example.com/",
            token="test-token",
        )
        assert client.base_url == "https://drive.example.com"

    async def test_get_documents_success(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test successful document retrieval."""
        # Mock first response (workspace)
        workspace_response = Mock()
        workspace_response.status_code = 200
        workspace_response.json.return_value = {"results": [{"id": "workspace123"}]}

        # Mock second response (documents)
        documents_response = Mock()
        documents_response.status_code = 200
        documents_response.json.return_value = {
            "results": [
                {
                    "id": "doc1",
                    "title": "Test Document",
                    "created_at": "2024-01-15T10:00:00Z",
                    "updated_at": "2024-01-15T11:00:00Z",
                    "url": "https://drive.example.com/doc",
                    "mimetype": "application/pdf",
                }
            ]
        }

        # Configure mock to return different responses for different calls
        mock_http_client.get.side_effect = [workspace_response, documents_response]

        # Test
        result = await client.get_documents()

        # Assertions
        assert len(result) == 1
        document = result[0]
        assert isinstance(document, Document)
        assert document.title == "Test Document"

        # Verify HTTP calls
        assert mock_http_client.get.call_count == 2

        # First call should be to the items endpoint
        first_call = mock_http_client.get.call_args_list[0]
        assert first_call[0][0] == "https://drive.example.com/api/v1.0/items/"
        assert first_call[1]["headers"] == {"Authorization": "Bearer test-token"}

        # Second call should be to the children endpoint
        second_call = mock_http_client.get.call_args_list[1]
        assert second_call[0][0] == "https://drive.example.com/api/v1.0/items/workspace123/children/"
        assert second_call[1]["headers"] == {"Authorization": "Bearer test-token"}

    async def test_get_documents_with_custom_params(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval with custom parameters."""
        workspace_response = Mock()
        workspace_response.status_code = 200
        workspace_response.json.return_value = {"results": [{"id": "workspace123"}]}

        documents_response = Mock()
        documents_response.status_code = 200
        documents_response.json.return_value = {"results": []}

        mock_http_client.get.side_effect = [workspace_response, documents_response]

        # Test with custom parameters
        await client.get_documents(
            path="custom/path/",
            page=2,
            page_size=10,
            ordering="name",
            title="search term",
            is_creator_me=True,
            is_favorite=True,
        )

        # Verify first HTTP call with custom parameters
        first_call = mock_http_client.get.call_args_list[0]
        assert first_call[0][0] == "https://drive.example.com/custom/path/"

        expected_params = {
            "page": 2,
            "page_size": 10,
            "ordering": "name",
            "title": "search term",
            "is_creator_me": "True",
            "is_favorite": "True",
        }
        assert first_call[1]["params"] == expected_params

    async def test_get_documents_minimal_params(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval with minimal parameters."""
        workspace_response = Mock()
        workspace_response.status_code = 200
        workspace_response.json.return_value = {"results": [{"id": "workspace123"}]}

        documents_response = Mock()
        documents_response.status_code = 200
        documents_response.json.return_value = {"results": []}

        mock_http_client.get.side_effect = [workspace_response, documents_response]

        # Test with default parameters
        await client.get_documents()

        # Verify first HTTP call with default parameters
        first_call = mock_http_client.get.call_args_list[0]
        expected_params = {
            "page": 1,
            "page_size": 5,
            "ordering": "-updated_at",
        }
        assert first_call[1]["params"] == expected_params

    async def test_get_documents_strips_leading_slash_from_path(
        self, client: DriveClient, mock_http_client: AsyncMock
    ) -> None:
        """Test that leading slash is stripped from path."""
        workspace_response = Mock()
        workspace_response.status_code = 200
        workspace_response.json.return_value = {"results": [{"id": "workspace123"}]}

        documents_response = Mock()
        documents_response.status_code = 200
        documents_response.json.return_value = {"results": []}

        mock_http_client.get.side_effect = [workspace_response, documents_response]

        await client.get_documents(path="/api/v1.0/items/")

        first_call = mock_http_client.get.call_args_list[0]
        assert first_call[0][0] == "https://drive.example.com/api/v1.0/items/"

    async def test_get_documents_first_request_error(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval when first request fails."""
        workspace_response = Mock()
        workspace_response.status_code = 404
        mock_http_client.get.return_value = workspace_response

        # Test
        result = await client.get_documents()

        # Should return empty list for non-200 status codes
        assert result == []

        # Should only make one HTTP call
        assert mock_http_client.get.call_count == 1

    async def test_get_documents_no_workspace_results(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval when no workspace found."""
        workspace_response = Mock()
        workspace_response.status_code = 200
        workspace_response.json.return_value = {"results": []}
        mock_http_client.get.return_value = workspace_response

        # Test
        result = await client.get_documents()

        # Should return empty list when no workspace found
        assert result == []

        # Should only make one HTTP call
        assert mock_http_client.get.call_count == 1

    async def test_get_documents_missing_results_key_first_request(
        self, client: DriveClient, mock_http_client: AsyncMock
    ) -> None:
        """Test document retrieval when first response has no results key."""
        workspace_response = Mock()
        workspace_response.status_code = 200
        workspace_response.json.return_value = {}  # No results key
        mock_http_client.get.return_value = workspace_response

        result = await client.get_documents()

        assert result == []
        assert mock_http_client.get.call_count == 1

    async def test_get_documents_second_request_error(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval when second request fails."""
        workspace_response = Mock()
        workspace_response.status_code = 200
        workspace_response.json.return_value = {"results": [{"id": "workspace123"}]}

        documents_response = Mock()
        documents_response.status_code = 500

        mock_http_client.get.side_effect = [workspace_response, documents_response]

        # Test
        result = await client.get_documents()

        # Should return empty list when second request fails
        assert result == []
        assert mock_http_client.get.call_count == 2

    async def test_get_documents_no_document_results(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval when no documents found."""
        workspace_response = Mock()
        workspace_response.status_code = 200
        workspace_response.json.return_value = {"results": [{"id": "workspace123"}]}

        documents_response = Mock()
        documents_response.status_code = 200
        documents_response.json.return_value = {"results": []}

        mock_http_client.get.side_effect = [workspace_response, documents_response]

        result = await client.get_documents()

        assert result == []
        assert mock_http_client.get.call_count == 2

    async def test_get_documents_missing_results_key_second_request(
        self, client: DriveClient, mock_http_client: AsyncMock
    ) -> None:
        """Test document retrieval when second response has no results key."""
        workspace_response = Mock()
        workspace_response.status_code = 200
        workspace_response.json.return_value = {"results": [{"id": "workspace123"}]}

        documents_response = Mock()
        documents_response.status_code = 200
        documents_response.json.return_value = {}  # No results key

        mock_http_client.get.side_effect = [workspace_response, documents_response]

        result = await client.get_documents()

        assert result == []
        assert mock_http_client.get.call_count == 2

    async def test_get_documents_multiple_documents(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test retrieval of multiple documents."""
        workspace_response = Mock()
        workspace_response.status_code = 200
        workspace_response.json.return_value = {"results": [{"id": "workspace123"}]}

        documents_response = Mock()
        documents_response.status_code = 200
        documents_response.json.return_value = {
            "results": [
                {
                    "id": "doc1",
                    "title": "Document 1",
                    "created_at": "2024-01-15T10:00:00Z",
                    "updated_at": "2024-01-15T11:00:00Z",
                    "url": "https://drive.example.com/doc",
                    "mimetype": "application/pdf",
                },
                {
                    "id": "doc2",
                    "title": "Document 2",
                    "created_at": "2024-01-16T10:00:00Z",
                    "updated_at": "2024-01-16T11:00:00Z",
                    "url": "https://drive.example.com/doc",
                    "mimetype": "application/pdf",
                },
            ]
        }

        mock_http_client.get.side_effect = [workspace_response, documents_response]

        result = await client.get_documents()

        assert len(result) == 2
        assert result[0].title == "Document 1"
        assert result[1].title == "Document 2"
