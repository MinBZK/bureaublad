"""Tests for Docs client."""

from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from app.clients.docs import DocsClient
from app.exceptions import ExternalServiceError
from app.models.note import Note


class TestDocsClient:
    """Tests for DocsClient class."""

    @pytest.fixture
    def mock_http_client(self) -> AsyncMock:
        """Create a mock HTTP client."""
        return AsyncMock(spec=httpx.AsyncClient)

    @pytest.fixture
    def client(self, mock_http_client: AsyncMock) -> DocsClient:
        """Create a DocsClient instance for testing."""
        return DocsClient(
            http_client=mock_http_client,
            base_url="https://docs.example.com",
            token="test-token",
        )

    def test_init(self, mock_http_client: AsyncMock, client: DocsClient) -> None:
        """Test DocsClient initialization."""
        assert client.client is mock_http_client
        assert client.base_url == "https://docs.example.com"
        assert client.token == "test-token"

    def test_init_strips_trailing_slash(self, mock_http_client: AsyncMock) -> None:
        """Test that trailing slash is stripped from base_url."""
        client = DocsClient(
            http_client=mock_http_client,
            base_url="https://docs.example.com/",
            token="test-token",
        )
        assert client.base_url == "https://docs.example.com"

    async def test_get_documents_success(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test successful document retrieval."""
        # Mock response data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            "count": 1,
            "results": [
                {
                    "id": "1",
                    "title": "Test Document",
                    "path": "/test/doc.md",
                    "created_at": "2024-01-15T10:00:00Z",
                    "updated_at": "2024-01-15T11:00:00Z",
                    "user_role": "owner",
                }
            ],
        }
        mock_http_client.get.return_value = mock_response

        # Test
        result = await client.get_documents()

        # Assertions
        assert result.count == 1
        assert len(result.results) == 1
        note = result.results[0]
        assert isinstance(note, Note)
        assert note.id == "1"
        assert note.title == "Test Document"

        # Verify HTTP call
        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://docs.example.com/api/v1.0/documents/all/"
        assert call_args[1]["headers"] == {"Authorization": "Bearer test-token"}

    async def test_get_documents_with_custom_params(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval with custom parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"results": []}
        mock_http_client.get.return_value = mock_response

        # Test with custom parameters
        await client.get_documents(
            path="custom/path/",
            page=2,
            page_size=10,
            title="search term",
            is_favorite=True,
            is_creator_me=True,
            ordering="title",
        )

        # Verify HTTP call with custom parameters
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://docs.example.com/custom/path/"

        expected_params = {
            "page": 2,
            "page_size": 10,
            "ordering": "title",
            "title": "search term",
            "is_favorite": "True",
            "is_creator_me": "True",
        }
        assert call_args[1]["params"] == expected_params

    async def test_get_documents_minimal_params(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval with minimal parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"results": []}
        mock_http_client.get.return_value = mock_response

        # Test with default parameters
        await client.get_documents()

        # Verify HTTP call with default parameters
        call_args = mock_http_client.get.call_args
        expected_params = {
            "page": 1,
            "page_size": 5,
            "ordering": "-updated_at",
        }
        assert call_args[1]["params"] == expected_params

    async def test_get_documents_strips_leading_slash_from_path(
        self, client: DocsClient, mock_http_client: AsyncMock
    ) -> None:
        """Test that leading slash is stripped from path."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"results": []}
        mock_http_client.get.return_value = mock_response

        await client.get_documents(path="/api/v1.0/documents/all/")

        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://docs.example.com/api/v1.0/documents/all/"

    async def test_get_documents_error_response(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval with error response."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_http_client.get.return_value = mock_response

        # Test - should raise exception for non-200 status codes
        with pytest.raises(ExternalServiceError) as exc_info:
            await client.get_documents()

        assert "Docs" in str(exc_info.value)
        assert "Failed to fetch api/v1.0/documents/all/ (status 404)" in str(exc_info.value)

    async def test_get_documents_multiple_documents(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test retrieval of multiple documents."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            "count": 2,
            "results": [
                {
                    "id": "1",
                    "title": "Document 1",
                    "created_at": "2024-01-15T10:00:00Z",
                    "updated_at": "2024-01-15T11:00:00Z",
                    "path": "/test/doc.md",
                    "user_role": "owner",
                },
                {
                    "id": "2",
                    "title": "Document 2",
                    "created_at": "2024-01-16T10:00:00Z",
                    "updated_at": "2024-01-16T11:00:00Z",
                    "path": "/test/doc.md",
                    "user_role": "owner",
                },
            ],
        }
        mock_http_client.get.return_value = mock_response

        result = await client.get_documents()

        assert result.count == 2
        assert len(result.results) == 2
        assert result.results[0].id == "1"
        assert result.results[0].title == "Document 1"
        assert result.results[1].id == "2"
        assert result.results[1].title == "Document 2"

    async def test_get_documents_no_results(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval when no results returned."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"results": []}
        mock_http_client.get.return_value = mock_response

        result = await client.get_documents()

        assert result.count == 0
        assert result.results == []

    async def test_get_documents_missing_results_key(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval when results key is missing."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}  # No results key
        mock_http_client.get.return_value = mock_response

        result = await client.get_documents()

        assert result.count == 0
        assert result.results == []

    async def test_post_document_success(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test successful document creation."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "1",
            "title": "New Document",
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z",
            "path": "/test/doc.md",
            "user_role": "owner",
        }
        mock_http_client.post.return_value = mock_response

        # Test
        result = await client.post_document()

        # Assertions
        assert isinstance(result, Note)
        assert result.id == "1"
        assert result.title == "New Document"

        # Verify HTTP call
        mock_http_client.post.assert_called_once()
        call_args = mock_http_client.post.call_args
        assert call_args[0][0] == "https://docs.example.com/api/v1.0/documents/"
        assert call_args[1]["headers"] == {"Authorization": "Bearer test-token"}

    async def test_post_document_with_custom_path(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test document creation with custom path."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "1",
            "title": "New Document",
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z",
            "path": "/test/doc.md",
            "user_role": "owner",
        }
        mock_http_client.post.return_value = mock_response

        await client.post_document(path="custom/create/")

        call_args = mock_http_client.post.call_args
        assert call_args[0][0] == "https://docs.example.com/custom/create/"

    async def test_post_document_strips_leading_slash_from_path(
        self, client: DocsClient, mock_http_client: AsyncMock
    ) -> None:
        """Test that leading slash is stripped from path in post_document."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "1",
            "title": "New Document",
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z",
            "path": "/test/doc.md",
            "user_role": "owner",
        }
        mock_http_client.post.return_value = mock_response

        await client.post_document(path="/api/v1.0/documents/")

        call_args = mock_http_client.post.call_args
        assert call_args[0][0] == "https://docs.example.com/api/v1.0/documents/"

    async def test_post_document_error_response(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test document creation with error response."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_http_client.post.return_value = mock_response

        # Test
        with pytest.raises(ExternalServiceError) as exc_info:
            await client.post_document()

        # Assertions
        assert "Docs" in str(exc_info.value)
        assert "Failed to create document (status 400)" in str(exc_info.value)

    async def test_post_document_server_error(self, client: DocsClient, mock_http_client: AsyncMock) -> None:
        """Test document creation with server error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_http_client.post.return_value = mock_response

        with pytest.raises(ExternalServiceError) as exc_info:
            await client.post_document()

        assert "Failed to create document (status 500)" in str(exc_info.value)
