"""Tests for the Meet endpoints."""

from unittest.mock import AsyncMock, MagicMock, patch

from app.models.pagination import PaginatedResponse
from app.models.room import Room
from fastapi.testclient import TestClient


class TestMeetEndpoints:
    """Test cases for Meet endpoints."""

    def test_meet_get_rooms_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that get rooms endpoint requires authentication."""
        response = fresh_client.get("/api/v1/meet/rooms")
        assert response.status_code == 401

    def test_meet_post_rooms_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that post rooms endpoint requires authentication."""
        response = fresh_client.post("/api/v1/meet/rooms")
        assert response.status_code == 401

    @patch("app.routes.meet.settings.MEET_URL", None)
    def test_meet_get_rooms_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test get rooms endpoint when service is disabled."""
        response = authenticated_client.get("/api/v1/meet/rooms")
        assert response.status_code == 503

    @patch("app.routes.meet.settings.MEET_URL", None)
    def test_meet_post_rooms_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test post rooms endpoint when service is disabled."""
        response = authenticated_client.post("/api/v1/meet/rooms")
        assert response.status_code == 503

    @patch("app.routes.meet.settings.MEET_URL", "https://meet.example.com")
    @patch("app.routes.meet.settings.MEET_AUDIENCE", "meet")
    @patch("app.routes.meet.get_token")
    @patch("app.routes.meet.MeetClient")
    def test_meet_get_rooms_success(
        self,
        mock_meet_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful rooms retrieval."""
        # Mock token exchange
        mock_get_token.return_value = "test-meet-token"

        # Mock MeetClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_rooms.return_value = PaginatedResponse(
            count=2,
            results=[
                Room(
                    id="room-123",
                    name="Daily Standup",
                    slug="daily-standup-123",
                    pin_code="123456",
                ),
                Room(
                    id="room-456",
                    name="Project Review",
                    slug="project-review-456",
                    pin_code="789012",
                ),
            ],
        )
        mock_meet_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/meet/rooms")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2
        assert len(data["results"]) == 2
        assert data["results"][0]["id"] == "room-123"
        assert data["results"][0]["name"] == "Daily Standup"
        assert data["results"][0]["slug"] == "daily-standup-123"
        assert data["results"][0]["pin_code"] == "123456"
        assert data["results"][1]["id"] == "room-456"
        assert data["results"][1]["name"] == "Project Review"

        # Verify MeetClient was called correctly
        mock_client_instance.get_rooms.assert_called_once_with(page=1, page_size=5)

    @patch("app.routes.meet.settings.MEET_URL", "https://meet.example.com")
    @patch("app.routes.meet.settings.MEET_AUDIENCE", "meet")
    @patch("app.routes.meet.get_token")
    @patch("app.routes.meet.MeetClient")
    def test_meet_get_rooms_with_pagination(
        self,
        mock_meet_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test rooms retrieval with pagination."""
        # Mock token exchange
        mock_get_token.return_value = "test-meet-token"

        # Mock MeetClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_rooms.return_value = PaginatedResponse(
            count=1,
            results=[
                Room(
                    id="room-123",
                    name="Daily Standup",
                    slug="daily-standup-123",
                    pin_code="123456",
                ),
            ],
        )
        mock_meet_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/meet/rooms?page=2&page_size=1")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["id"] == "room-123"

        # Verify MeetClient was called correctly with page parameter
        mock_client_instance.get_rooms.assert_called_once_with(page=2, page_size=1)

    @patch("app.routes.meet.settings.MEET_URL", "https://meet.example.com")
    @patch("app.routes.meet.settings.MEET_AUDIENCE", "meet")
    @patch("app.routes.meet.get_token")
    @patch("app.routes.meet.MeetClient")
    def test_meet_get_rooms_empty_result(
        self,
        mock_meet_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test rooms endpoint with no rooms."""
        # Mock token exchange
        mock_get_token.return_value = "test-meet-token"

        # Mock MeetClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_rooms.return_value = PaginatedResponse[Room](count=0, results=[])
        mock_meet_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/meet/rooms")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["results"] == []

    @patch("app.routes.meet.settings.MEET_URL", "https://meet.example.com")
    @patch("app.routes.meet.settings.MEET_AUDIENCE", "meet")
    @patch("app.routes.meet.settings.MEET_URL", "https://meet.example.com")
    @patch("app.routes.meet.get_token")
    @patch("app.routes.meet.MeetClient")
    @patch("app.routes.meet.generate_random_room_name")
    def test_meet_post_room_success(
        self,
        mock_generate_name: MagicMock,
        mock_meet_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful room creation."""
        # Mock room name generation
        mock_generate_name.return_value = "abc-defg-hij"

        # Mock token exchange
        mock_get_token.return_value = "test-meet-token"

        # Mock MeetClient
        mock_client_instance = AsyncMock()
        mock_client_instance.post_room.return_value = Room(
            id="room-789",
            name="abc-defg-hij",
            slug="abc-defg-hij-789",
            pin_code="345678",
        )
        mock_meet_client.return_value = mock_client_instance

        response = authenticated_client.post("/api/v1/meet/rooms")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "room-789"
        assert data["name"] == "abc-defg-hij"
        assert data["slug"] == "abc-defg-hij-789"
        assert data["pin_code"] == "345678"
        assert data["url"] == "https://meet.example.com/abc-defg-hij-789"

        # Verify MeetClient was called correctly
        mock_client_instance.post_room.assert_called_once_with(name="abc-defg-hij")

    @patch("app.routes.meet.settings.MEET_URL", "https://meet.example.com")
    @patch("app.routes.meet.settings.MEET_AUDIENCE", "meet")
    @patch("app.routes.meet.get_token")
    def test_meet_get_rooms_token_exchange_error(
        self,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test get rooms endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.get("/api/v1/meet/rooms")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.meet.settings.MEET_URL", "https://meet.example.com")
    @patch("app.routes.meet.settings.MEET_AUDIENCE", "meet")
    @patch("app.routes.meet.get_token")
    def test_meet_post_room_token_exchange_error(
        self,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test post room endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.post("/api/v1/meet/rooms")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.meet.settings.MEET_URL", "https://meet.example.com")
    @patch("app.routes.meet.settings.MEET_AUDIENCE", "meet")
    @patch("app.routes.meet.get_token")
    @patch("app.routes.meet.MeetClient")
    def test_meet_get_rooms_api_error(
        self,
        mock_meet_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test get rooms endpoint when Meet API returns error."""
        from app.exceptions import ExternalServiceError

        # Mock token exchange
        mock_get_token.return_value = "test-meet-token"

        # Mock MeetClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.get_rooms.side_effect = ExternalServiceError("Meet", "API error")
        mock_meet_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/meet/rooms")

        assert response.status_code == 502  # ExternalServiceError returns 502

    @patch("app.routes.meet.settings.MEET_URL", "https://meet.example.com")
    @patch("app.routes.meet.settings.MEET_AUDIENCE", "meet")
    @patch("app.routes.meet.get_token")
    @patch("app.routes.meet.MeetClient")
    @patch("app.routes.meet.generate_random_room_name")
    def test_meet_post_room_api_error(
        self,
        mock_generate_name: MagicMock,
        mock_meet_client: MagicMock,
        mock_get_token: AsyncMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test post room endpoint when Meet API returns error."""
        from app.exceptions import ExternalServiceError

        # Mock room name generation
        mock_generate_name.return_value = "abc-defg-hij"

        # Mock token exchange
        mock_get_token.return_value = "test-meet-token"

        # Mock MeetClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.post_room.side_effect = ExternalServiceError("Meet", "Failed to create room")
        mock_meet_client.return_value = mock_client_instance

        response = authenticated_client.post("/api/v1/meet/rooms")

        assert response.status_code == 502  # ExternalServiceError returns 502

    def test_generate_random_room_name_format(self) -> None:
        """Test that generate_random_room_name produces correct format."""
        from app.routes.meet import generate_random_room_name

        # Test multiple generations to ensure format consistency
        for _ in range(10):
            name = generate_random_room_name()
            parts = name.split("-")
            assert len(parts) == 3
            assert len(parts[0]) == 3  # First part: 3 letters
            assert len(parts[1]) == 4  # Second part: 4 letters
            assert len(parts[2]) == 3  # Third part: 3 letters
            # Check all parts contain only lowercase letters
            for part in parts:
                assert part.islower()
                assert part.isalpha()
