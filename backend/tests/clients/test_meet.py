"""Tests for Meet client."""

from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from app.clients.meet import MeetClient
from app.exceptions import ExternalServiceError
from app.models.room import Room


class TestMeetClient:
    """Tests for MeetClient class."""

    @pytest.fixture
    def mock_http_client(self) -> AsyncMock:
        """Create a mock HTTP client."""
        return AsyncMock(spec=httpx.AsyncClient)

    @pytest.fixture
    def client(self, mock_http_client: AsyncMock) -> MeetClient:
        """Create a MeetClient instance for testing."""
        return MeetClient(
            http_client=mock_http_client,
            base_url="https://meet.example.com",
            token="test-token",
        )

    def test_init(self, mock_http_client: AsyncMock, client: MeetClient) -> None:
        """Test MeetClient initialization."""
        assert client.client is mock_http_client
        assert client.base_url == "https://meet.example.com"
        assert client.token == "test-token"

    def test_init_strips_trailing_slash(self, mock_http_client: AsyncMock) -> None:
        """Test that trailing slash is stripped from base_url."""
        client = MeetClient(
            http_client=mock_http_client,
            base_url="https://meet.example.com/",
            token="test-token",
        )
        assert client.base_url == "https://meet.example.com"

    async def test_get_rooms_success(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test successful room retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "room1",
                    "name": "Test Room",
                    "url": "https://meet.example.com/room1",
                    "created_at": "2024-01-15T10:00:00Z",
                    "slug": "test-room-slug",
                    "pin_code": "123456",
                }
            ]
        }
        mock_http_client.get.return_value = mock_response

        # Test
        result = await client.get_rooms()

        # Assertions
        assert len(result) == 1
        room = result[0]
        assert isinstance(room, Room)
        assert room.id == "room1"
        assert room.name == "Test Room"

        # Verify HTTP call
        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://meet.example.com/api/v1.0/rooms/"
        assert call_args[1]["params"] == {"page": 1, "page_size": 5}
        assert call_args[1]["headers"] == {"Authorization": "Bearer test-token"}

    async def test_get_rooms_with_custom_params(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test room retrieval with custom parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_http_client.get.return_value = mock_response

        # Test with custom parameters
        await client.get_rooms(path="custom/rooms/", page=2)

        # Verify HTTP call with custom parameters
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://meet.example.com/custom/rooms/"
        assert call_args[1]["params"] == {"page": 2, "page_size": 5}

    async def test_get_rooms_strips_leading_slash_from_path(
        self, client: MeetClient, mock_http_client: AsyncMock
    ) -> None:
        """Test that leading slash is stripped from path."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_http_client.get.return_value = mock_response

        await client.get_rooms(path="/api/v1.0/rooms/")

        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "https://meet.example.com/api/v1.0/rooms/"

    async def test_get_rooms_page_normalization(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test that invalid page numbers are normalized."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_http_client.get.return_value = mock_response

        # Test with None page
        await client.get_rooms()
        call_args = mock_http_client.get.call_args
        assert call_args[1]["params"] == {"page": 1, "page_size": 5}

        # Reset mock
        mock_http_client.reset_mock()
        mock_http_client.get.return_value = mock_response

        # Test with page < 1
        await client.get_rooms(page=0)
        call_args = mock_http_client.get.call_args
        assert call_args[1]["params"] == {"page": 1, "page_size": 5}

    async def test_get_rooms_error_response(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test room retrieval with error response."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_http_client.get.return_value = mock_response

        # Test - should raise exception for non-200 status codes
        with pytest.raises(ExternalServiceError) as exc_info:
            await client.get_rooms()

        assert "Meet" in str(exc_info.value)
        assert "Failed to fetch api/v1.0/rooms/ (status 404)" in str(exc_info.value)

    async def test_get_rooms_multiple_rooms(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test retrieval of multiple rooms."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "room1",
                    "name": "Room 1",
                    "url": "https://meet.example.com/room1",
                    "created_at": "2024-01-15T10:00:00Z",
                    "slug": "test-room-slug",
                    "pin_code": "123456",
                },
                {
                    "id": "room2",
                    "name": "Room 2",
                    "url": "https://meet.example.com/room2",
                    "created_at": "2024-01-16T10:00:00Z",
                    "slug": "test-room-slug",
                    "pin_code": "123456",
                },
            ]
        }
        mock_http_client.get.return_value = mock_response

        result = await client.get_rooms()

        assert len(result) == 2
        assert result[0].id == "room1"
        assert result[0].name == "Room 1"
        assert result[1].id == "room2"
        assert result[1].name == "Room 2"

    async def test_get_rooms_no_results(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test room retrieval when no results returned."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_http_client.get.return_value = mock_response

        result = await client.get_rooms()

        assert result == []

    async def test_get_rooms_missing_results_key(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test room retrieval when results key is missing."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # No results key
        mock_http_client.get.return_value = mock_response

        result = await client.get_rooms()

        assert result == []

    async def test_post_room_success(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test successful room creation."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "new-room",
            "name": "New Room",
            "url": "https://meet.example.com/new-room",
            "created_at": "2024-01-15T10:00:00Z",
            "slug": "test-room-slug",
            "pin_code": "123456",
        }
        mock_http_client.post.return_value = mock_response

        # Test
        result = await client.post_room(name="New Room")

        # Assertions
        assert isinstance(result, Room)
        assert result.id == "new-room"
        assert result.name == "New Room"

        # Verify HTTP call
        mock_http_client.post.assert_called_once()
        call_args = mock_http_client.post.call_args
        assert call_args[0][0] == "https://meet.example.com/api/v1.0/rooms/"
        assert call_args[1]["json"] == {"name": "New Room"}
        assert call_args[1]["headers"] == {"Authorization": "Bearer test-token"}

    async def test_post_room_with_custom_path(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test room creation with custom path."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "new-room",
            "name": "New Room",
            "url": "https://meet.example.com/new-room",
            "created_at": "2024-01-15T10:00:00Z",
            "slug": "test-room-slug",
            "pin_code": "123456",
        }
        mock_http_client.post.return_value = mock_response

        await client.post_room(name="New Room", path="custom/create/")

        call_args = mock_http_client.post.call_args
        assert call_args[0][0] == "https://meet.example.com/custom/create/"

    async def test_post_room_strips_leading_slash_from_path(
        self, client: MeetClient, mock_http_client: AsyncMock
    ) -> None:
        """Test that leading slash is stripped from path in post_room."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "new-room",
            "name": "New Room",
            "url": "https://meet.example.com/new-room",
            "created_at": "2024-01-15T10:00:00Z",
            "slug": "test-room-slug",
            "pin_code": "123456",
        }
        mock_http_client.post.return_value = mock_response

        await client.post_room(name="New Room", path="/api/v1.0/rooms/")

        call_args = mock_http_client.post.call_args
        assert call_args[0][0] == "https://meet.example.com/api/v1.0/rooms/"

    async def test_post_room_error_response(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test room creation with error response."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_http_client.post.return_value = mock_response

        # Test
        with pytest.raises(ExternalServiceError) as exc_info:
            await client.post_room(name="New Room")

        # Assertions
        assert "Meet" in str(exc_info.value)
        assert "Failed to create room (status 400)" in str(exc_info.value)

    async def test_post_room_server_error(self, client: MeetClient, mock_http_client: AsyncMock) -> None:
        """Test room creation with server error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_http_client.post.return_value = mock_response

        with pytest.raises(ExternalServiceError) as exc_info:
            await client.post_room(name="New Room")

        assert "Failed to create room (status 500)" in str(exc_info.value)
