"""Tests for OCS client."""

from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from app.clients.ocs import OCSClient
from app.exceptions import ExternalServiceError
from app.models.activity import Activity
from app.models.search import SearchResults


class TestOCSClient:
    """Tests for OCSClient class."""

    @pytest.fixture
    def mock_http_client(self) -> AsyncMock:
        """Create a mock HTTP client."""
        return AsyncMock(spec=httpx.AsyncClient)

    @pytest.fixture
    def client(self, mock_http_client: AsyncMock) -> OCSClient:
        """Create an OCSClient instance for testing."""
        return OCSClient(
            http_client=mock_http_client,
            base_url="https://nextcloud.example.com",
            token="test-token",
        )

    def test_init(self, mock_http_client: AsyncMock, client: OCSClient) -> None:
        """Test OCSClient initialization."""
        assert client.client is mock_http_client
        assert client.base_url == "https://nextcloud.example.com"
        assert client.token == "test-token"

    def test_init_strips_trailing_slash(self, mock_http_client: AsyncMock) -> None:
        """Test that trailing slash is stripped from base_url."""
        client = OCSClient(
            http_client=mock_http_client,
            base_url="https://nextcloud.example.com/",
            token="test-token",
        )
        assert client.base_url == "https://nextcloud.example.com"

    async def test_get_activities_success(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test successful activities retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ocs": {
                "data": [
                    {
                        "activity_id": 1,
                        "subject": "Test Activity",
                        "timestamp": 1642234800,
                        "type": "file",
                        "user": "testuser",
                        "app": "files",
                        "message": "Test message",
                        "link": "https://example.com/link",
                        "object_type": "file",
                        "object_id": 123,
                        "object_name": "test.txt",
                        "datetime": "2024-01-15T10:00:00",
                    }
                ]
            }
        }
        mock_http_client.get.return_value = mock_response

        # Test
        result = await client.get_activities()

        # Assertions
        assert len(result) == 1
        activity = result[0]
        assert isinstance(activity, Activity)
        assert activity.activity_id == 1
        assert activity.subject == "Test Activity"

        # Verify HTTP call
        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        expected_url = "https://nextcloud.example.com/ocs/v2.php/apps/activity/api/v2/activity/files"
        assert call_args[0][0] == expected_url

        expected_headers = {
            "Authorization": "Bearer test-token",
            "OCS-APIRequest": "true",
            "Accept": "application/json",
        }
        assert call_args[1]["headers"] == expected_headers

        expected_params = {"format": "json", "limit": "5"}
        assert call_args[1]["params"] == expected_params

    async def test_get_activities_with_custom_params(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test activities retrieval with custom parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ocs": {"data": []}}
        mock_http_client.get.return_value = mock_response

        # Test with custom parameters
        await client.get_activities(
            path="custom/activity/path",
            limit=10,
            since=123456,
            filter="calendar",
        )

        # Verify HTTP call with custom parameters
        call_args = mock_http_client.get.call_args
        expected_url = "https://nextcloud.example.com/custom/activity/path/calendar"
        assert call_args[0][0] == expected_url

        expected_params = {"format": "json", "since": "123456", "limit": "10"}
        assert call_args[1]["params"] == expected_params

    async def test_get_activities_no_filter(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test activities retrieval without filter."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ocs": {"data": []}}
        mock_http_client.get.return_value = mock_response

        await client.get_activities(filter=None)

        call_args = mock_http_client.get.call_args
        expected_url = "https://nextcloud.example.com/ocs/v2.php/apps/activity/api/v2/activity"
        assert call_args[0][0] == expected_url

    async def test_get_activities_strips_leading_slash(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test that leading slash is stripped from path."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ocs": {"data": []}}
        mock_http_client.get.return_value = mock_response

        await client.get_activities(path="/ocs/v2.php/apps/activity/api/v2/activity")

        call_args = mock_http_client.get.call_args
        expected_url = "https://nextcloud.example.com/ocs/v2.php/apps/activity/api/v2/activity/files"
        assert call_args[0][0] == expected_url

    async def test_get_activities_minimal_params(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test activities retrieval with minimal parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ocs": {"data": []}}
        mock_http_client.get.return_value = mock_response

        await client.get_activities(since=0, limit=0)

        call_args = mock_http_client.get.call_args
        # since=0 should not be included in params, limit=0 should not be included
        expected_params = {"format": "json"}
        assert call_args[1]["params"] == expected_params

    async def test_get_activities_error_response(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test activities retrieval with error response."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_http_client.get.return_value = mock_response

        with pytest.raises(ExternalServiceError) as exc_info:
            await client.get_activities()

        assert "OCS" in str(exc_info.value)
        assert "Failed to fetch ocs/v2.php/apps/activity/api/v2/activity/files (status 404)" in str(exc_info.value)

    async def test_get_activities_multiple_activities(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test retrieval of multiple activities."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ocs": {
                "data": [
                    {
                        "activity_id": 1,
                        "subject": "Activity 1",
                        "timestamp": 1642234800,
                        "type": "file",
                        "user": "user1",
                        "app": "files",
                        "message": "Test message",
                        "link": "https://example.com/link",
                        "object_type": "file",
                        "object_id": 123,
                        "object_name": "test.txt",
                        "datetime": "2024-01-15T10:00:00",
                    },
                    {
                        "activity_id": 2,
                        "subject": "Activity 2",
                        "timestamp": 1642234900,
                        "type": "calendar",
                        "user": "user2",
                        "app": "files",
                        "message": "Test message",
                        "link": "https://example.com/link",
                        "object_type": "file",
                        "object_id": 123,
                        "object_name": "test.txt",
                        "datetime": "2024-01-15T10:00:00",
                    },
                ]
            }
        }
        mock_http_client.get.return_value = mock_response

        result = await client.get_activities()

        assert len(result) == 2
        assert result[0].activity_id == 1
        assert result[0].subject == "Activity 1"
        assert result[1].activity_id == 2
        assert result[1].subject == "Activity 2"

    async def test_get_activities_no_data(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test activities retrieval when no data returned."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ocs": {"data": []}}
        mock_http_client.get.return_value = mock_response

        result = await client.get_activities()

        assert result == []

    async def test_get_activities_missing_data_key(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test activities retrieval when data key is missing."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ocs": {}}  # No data key
        mock_http_client.get.return_value = mock_response

        result = await client.get_activities()

        assert result == []

    async def test_search_files_success(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test successful file search."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ocs": {
                "data": {
                    "entries": [
                        {
                            "title": "test-file.txt",
                            "subline": "/Documents/test-file.txt",
                            "resourceUrl": "https://nextcloud.example.com/f/12345",
                            "icon": "text-plain",
                            "thumbnailUrl": None,
                            "attributes": {},
                        }
                    ]
                }
            }
        }
        mock_http_client.get.return_value = mock_response

        # Test
        result = await client.search_files(term="test")

        # Assertions
        assert len(result) == 1
        search_result = result[0]
        assert isinstance(search_result, SearchResults)
        assert search_result.name == "test-file.txt"
        # Note: subline is not a field in the model, only name and url

        # Verify HTTP call
        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        expected_url = "https://nextcloud.example.com/ocs/v2.php/search/providers/files/search"
        assert call_args[0][0] == expected_url

        expected_headers = {
            "Authorization": "Bearer test-token",
            "OCS-APIRequest": "true",
            "Accept": "application/json",
        }
        assert call_args[1]["headers"] == expected_headers
        assert call_args[1]["params"] == {"term": "test"}

    async def test_search_files_with_custom_path(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test file search with custom path."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ocs": {"data": {"entries": []}}}
        mock_http_client.get.return_value = mock_response

        await client.search_files(term="test", path="custom/search/path")

        call_args = mock_http_client.get.call_args
        expected_url = "https://nextcloud.example.com/custom/search/path"
        assert call_args[0][0] == expected_url

    async def test_search_files_strips_leading_slash(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test that leading slash is stripped from path in search_files."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ocs": {"data": {"entries": []}}}
        mock_http_client.get.return_value = mock_response

        await client.search_files(term="test", path="/ocs/v2.php/search/providers/files/search")

        call_args = mock_http_client.get.call_args
        expected_url = "https://nextcloud.example.com/ocs/v2.php/search/providers/files/search"
        assert call_args[0][0] == expected_url

    async def test_search_files_error_response(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test file search with error response."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_http_client.get.return_value = mock_response

        with pytest.raises(ExternalServiceError) as exc_info:
            await client.search_files(term="test")

        assert "OCS" in str(exc_info.value)
        assert "Failed to fetch ocs/v2.php/search/providers/files/search (status 500)" in str(exc_info.value)

    async def test_search_files_multiple_results(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test file search with multiple results."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ocs": {
                "data": {
                    "entries": [
                        {
                            "title": "file1.txt",
                            "subline": "/Documents/file1.txt",
                            "resourceUrl": "https://nextcloud.example.com/f/12345",
                            "icon": "text-plain",
                            "thumbnailUrl": None,
                            "attributes": {},
                        },
                        {
                            "title": "file2.txt",
                            "subline": "/Documents/file2.txt",
                            "resourceUrl": "https://nextcloud.example.com/f/67890",
                            "icon": "text-plain",
                            "thumbnailUrl": None,
                            "attributes": {},
                        },
                    ]
                }
            }
        }
        mock_http_client.get.return_value = mock_response

        result = await client.search_files(term="test")

        assert len(result) == 2
        assert result[0].name == "file1.txt"
        assert result[1].name == "file2.txt"

    async def test_search_files_no_results(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test file search when no results found."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ocs": {"data": {"entries": []}}}
        mock_http_client.get.return_value = mock_response

        result = await client.search_files(term="nonexistent")

        assert result == []
