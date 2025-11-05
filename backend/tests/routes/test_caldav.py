"""Tests for the CalDAV endpoints."""

from datetime import datetime
from unittest.mock import MagicMock, patch

from app.models.calendar import Calendar
from app.models.task import Task
from fastapi.testclient import TestClient


class TestCaldavEndpoints:
    """Test cases for CalDAV endpoints."""

    def test_caldav_calendar_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that calendar endpoint requires authentication."""
        response = fresh_client.get("/api/v1/caldav/calendars/2024-11-01")
        assert response.status_code == 401

    def test_caldav_tasks_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that tasks endpoint requires authentication."""
        response = fresh_client.get("/api/v1/caldav/tasks")
        assert response.status_code == 401

    @patch("app.routes.caldav.settings.TASK_URL", None)
    def test_caldav_calendar_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test calendar endpoint when service is disabled."""
        response = authenticated_client.get("/api/v1/caldav/calendars/2024-11-01")
        assert response.status_code == 503

    @patch("app.routes.caldav.settings.TASK_URL", None)
    def test_caldav_tasks_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test tasks endpoint when service is disabled."""
        response = authenticated_client.get("/api/v1/caldav/tasks")
        assert response.status_code == 503

    @patch("app.routes.caldav.settings.TASK_URL", "https://caldav.example.com")
    @patch("app.routes.caldav.settings.TASK_AUDIENCE", "caldav")
    @patch("app.routes.caldav.get_token")
    @patch("app.routes.caldav.CaldavClient")
    def test_caldav_calendar_success(
        self,
        mock_caldav_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful calendar events retrieval."""
        # Mock token exchange
        mock_get_token.return_value = "test-caldav-token"

        # Mock CaldavClient
        mock_client_instance = MagicMock()
        mock_client_instance.get_calendars.return_value = [
            Calendar(
                title="Team Meeting",
                start=datetime(2024, 11, 1, 10, 0, 0),
                end=datetime(2024, 11, 1, 11, 0, 0),
            ),
            Calendar(
                title="Project Review",
                start=datetime(2024, 11, 1, 14, 0, 0),
                end=datetime(2024, 11, 1, 15, 30, 0),
            ),
        ]
        mock_caldav_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/caldav/calendars/2024-11-01")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Team Meeting"
        assert data[0]["start"] == "2024-11-01T10:00:00"
        assert data[0]["end"] == "2024-11-01T11:00:00"
        assert data[1]["title"] == "Project Review"
        assert data[1]["start"] == "2024-11-01T14:00:00"
        assert data[1]["end"] == "2024-11-01T15:30:00"

        # Verify CaldavClient was called correctly
        mock_client_instance.get_calendars.assert_called_once_with(check_date=datetime(2024, 11, 1, 0, 0, 0))

    @patch("app.routes.caldav.settings.TASK_URL", "https://caldav.example.com")
    @patch("app.routes.caldav.settings.TASK_AUDIENCE", "caldav")
    @patch("app.routes.caldav.get_token")
    @patch("app.routes.caldav.CaldavClient")
    def test_caldav_tasks_success(
        self,
        mock_caldav_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful tasks retrieval."""
        # Mock token exchange
        mock_get_token.return_value = "test-caldav-token"

        # Mock CaldavClient
        mock_client_instance = MagicMock()
        mock_client_instance.get_tasks.return_value = [
            Task(
                title="Complete project documentation",
                start=datetime(2024, 11, 1, 9, 0, 0),
                end=datetime(2024, 11, 5, 17, 0, 0),
            ),
            Task(
                title="Review pull requests",
                start=None,
                end=datetime(2024, 11, 2, 12, 0, 0),
            ),
        ]
        mock_caldav_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/caldav/tasks")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Complete project documentation"
        assert data[0]["start"] == "2024-11-01T09:00:00"
        assert data[0]["end"] == "2024-11-05T17:00:00"
        assert data[1]["title"] == "Review pull requests"
        assert data[1]["start"] is None
        assert data[1]["end"] == "2024-11-02T12:00:00"

        # Verify CaldavClient was called correctly
        mock_client_instance.get_tasks.assert_called_once()

    @patch("app.routes.caldav.settings.TASK_URL", "https://caldav.example.com")
    @patch("app.routes.caldav.settings.TASK_AUDIENCE", "caldav")
    @patch("app.routes.caldav.get_token")
    @patch("app.routes.caldav.CaldavClient")
    def test_caldav_calendar_empty_result(
        self,
        mock_caldav_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test calendar endpoint with no events for the day."""
        # Mock token exchange
        mock_get_token.return_value = "test-caldav-token"

        # Mock CaldavClient
        mock_client_instance = MagicMock()
        mock_client_instance.get_calendars.return_value = []
        mock_caldav_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/caldav/calendars/2024-11-01")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    @patch("app.routes.caldav.settings.TASK_URL", "https://caldav.example.com")
    @patch("app.routes.caldav.settings.TASK_AUDIENCE", "caldav")
    @patch("app.routes.caldav.get_token")
    @patch("app.routes.caldav.CaldavClient")
    def test_caldav_tasks_empty_result(
        self,
        mock_caldav_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test tasks endpoint with no tasks."""
        # Mock token exchange
        mock_get_token.return_value = "test-caldav-token"

        # Mock CaldavClient
        mock_client_instance = MagicMock()
        mock_client_instance.get_tasks.return_value = []
        mock_caldav_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/caldav/tasks")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_caldav_calendar_invalid_date_format(self, authenticated_client: TestClient) -> None:
        """Test calendar endpoint with invalid date format."""
        response = authenticated_client.get("/api/v1/caldav/calendars/invalid-date")
        assert response.status_code == 422  # Unprocessable Entity

    @patch("app.routes.caldav.settings.TASK_URL", "https://caldav.example.com")
    @patch("app.routes.caldav.settings.TASK_AUDIENCE", "caldav")
    @patch("app.routes.caldav.get_token")
    def test_caldav_calendar_token_exchange_error(
        self,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test calendar endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.get("/api/v1/caldav/calendars/2024-11-01")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.caldav.settings.TASK_URL", "https://caldav.example.com")
    @patch("app.routes.caldav.settings.TASK_AUDIENCE", "caldav")
    @patch("app.routes.caldav.get_token")
    def test_caldav_tasks_token_exchange_error(
        self,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test tasks endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.get("/api/v1/caldav/tasks")

        assert response.status_code == 403  # TokenExchangeError returns 403
