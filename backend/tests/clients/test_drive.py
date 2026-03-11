"""Tests for Drive client."""

from unittest.mock import AsyncMock, Mock

import pytest
from app.clients.drive import DriveClient
from app.models.document import Document
from app.models.pagination import PaginatedResponse


class TestDriveClient:
    """Tests for DriveClient class."""

    @pytest.fixture
    def mock_http_client(self) -> AsyncMock:
        """Create a mock HTTP client."""
        return AsyncMock()

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
        """Test successful document retrieval from recents endpoint."""
        response = Mock()
        response.status_code = 200
        response.headers = {}
        response.json.return_value = {
            "count": 1,
            "results": [
                {
                    "id": "doc1",
                    "title": "Test Document",
                    "updated_at": "2024-01-15T11:00:00Z",
                    "url": "https://drive.example.com/media/item/doc1/test.pdf",
                    "url_preview": None,
                    "mimetype": "application/pdf",
                }
            ],
        }
        mock_http_client.get.return_value = response

        result = await client.get_documents()

        assert result.count == 1
        assert len(result.results) == 1
        assert isinstance(result.results[0], Document)
        assert result.results[0].title == "Test Document"
        assert result.results[0].url == "https://drive.example.com/media/item/doc1/test.pdf"
        assert result.results[0].url_preview == "https://drive.example.com/explorer/items/files/doc1"

        # Should make exactly one HTTP call to the recents endpoint
        assert mock_http_client.get.call_count == 1
        call = mock_http_client.get.call_args_list[0]
        assert call[0][0] == "https://drive.example.com/api/v1.0/items/recents/"
        assert call[1]["headers"] == {"Authorization": "Bearer test-token"}

    async def test_get_documents_default_params(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test that default parameters are sent correctly."""
        response = Mock()
        response.status_code = 200
        response.headers = {}
        response.json.return_value = {"count": 0, "results": []}
        mock_http_client.get.return_value = response

        await client.get_documents()

        call = mock_http_client.get.call_args_list[0]
        assert call[1]["params"] == {"page": 1, "page_size": 5}

    async def test_get_documents_with_title(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval with title filter."""
        response = Mock()
        response.status_code = 200
        response.headers = {}
        response.json.return_value = {"count": 0, "results": []}
        mock_http_client.get.return_value = response

        await client.get_documents(title="search term")

        call = mock_http_client.get.call_args_list[0]
        assert call[1]["params"] == {"page": 1, "page_size": 5, "title": "search term"}

    async def test_get_documents_with_pagination(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval with custom page and page_size."""
        response = Mock()
        response.status_code = 200
        response.headers = {}
        response.json.return_value = {"count": 0, "results": []}
        mock_http_client.get.return_value = response

        await client.get_documents(page=3, page_size=10)

        call = mock_http_client.get.call_args_list[0]
        assert call[1]["params"] == {"page": 3, "page_size": 10}

    async def test_get_documents_page_clamped_to_minimum(
        self, client: DriveClient, mock_http_client: AsyncMock
    ) -> None:
        """Test that page is clamped to a minimum of 1."""
        response = Mock()
        response.status_code = 200
        response.headers = {}
        response.json.return_value = {"count": 0, "results": []}
        mock_http_client.get.return_value = response

        await client.get_documents(page=-5, page_size=0)

        call = mock_http_client.get.call_args_list[0]
        assert call[1]["params"]["page"] == 1
        assert call[1]["params"]["page_size"] == 1

    async def test_get_documents_empty_result(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test document retrieval returning no documents."""
        response = Mock()
        response.status_code = 200
        response.headers = {}
        response.json.return_value = {"count": 0, "results": []}
        mock_http_client.get.return_value = response

        result = await client.get_documents()

        assert result == PaginatedResponse[Document](count=0, results=[])

    async def test_get_documents_request_error(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test that request errors return an empty result."""
        response = Mock()
        response.status_code = 500
        mock_http_client.get.return_value = response

        result = await client.get_documents()

        assert result == PaginatedResponse[Document](count=0, results=[])
        assert mock_http_client.get.call_count == 1

    async def test_get_documents_multiple_documents(self, client: DriveClient, mock_http_client: AsyncMock) -> None:
        """Test retrieval of multiple documents."""
        response = Mock()
        response.status_code = 200
        response.headers = {}
        response.json.return_value = {
            "count": 2,
            "results": [
                {
                    "id": "doc1",
                    "title": "Document 1",
                    "updated_at": "2024-01-15T11:00:00Z",
                    "url": "https://drive.example.com/media/item/doc1/doc1.pdf",
                    "url_preview": None,
                    "mimetype": "application/pdf",
                },
                {
                    "id": "doc2",
                    "title": "Document 2",
                    "updated_at": "2024-01-16T11:00:00Z",
                    "url": "https://drive.example.com/media/item/doc2/doc2.pdf",
                    "url_preview": "https://drive.example.com/preview/doc2.png",
                    "mimetype": "application/pdf",
                },
            ],
        }
        mock_http_client.get.return_value = response

        result = await client.get_documents()

        assert result.count == 2
        assert len(result.results) == 2
        assert result.results[0].title == "Document 1"
        assert result.results[0].url_preview == "https://drive.example.com/explorer/items/files/doc1"
        assert result.results[1].title == "Document 2"
        assert result.results[1].url_preview == "https://drive.example.com/preview/doc2.png"
