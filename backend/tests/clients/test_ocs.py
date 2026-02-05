"""Tests for OCS client."""

from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from app.clients.ocs import OCSClient
from app.exceptions import ExternalServiceError
from app.models.activity import Activity
from app.models.search import SearchResults


def create_mock_response(
    status_code: int = 200,
    json_data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> Mock:
    """Create a mock HTTP response with headers."""
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data or {}
    mock_response.headers = headers or {}
    return mock_response


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

    async def test_search_files_success(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test successful file search."""
        mock_response = create_mock_response(
            status_code=200,
            json_data={
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
            },
        )
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
        assert call_args[1]["params"] == {"format": "json", "term": "test"}

    async def test_search_files_with_custom_path(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test file search with custom path."""
        mock_response = create_mock_response(status_code=200, json_data={"ocs": {"data": {"entries": []}}})
        mock_http_client.get.return_value = mock_response

        await client.search_files(term="test", path="custom/search/path")

        call_args = mock_http_client.get.call_args
        expected_url = "https://nextcloud.example.com/custom/search/path"
        assert call_args[0][0] == expected_url

    async def test_search_files_strips_leading_slash(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test that leading slash is stripped from path in search_files."""
        mock_response = create_mock_response(status_code=200, json_data={"ocs": {"data": {"entries": []}}})
        mock_http_client.get.return_value = mock_response

        await client.search_files(term="test", path="/ocs/v2.php/search/providers/files/search")

        call_args = mock_http_client.get.call_args
        expected_url = "https://nextcloud.example.com/ocs/v2.php/search/providers/files/search"
        assert call_args[0][0] == expected_url

    async def test_search_files_error_response(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test file search with error response."""
        mock_response = create_mock_response(status_code=500)
        mock_http_client.get.return_value = mock_response

        with pytest.raises(ExternalServiceError) as exc_info:
            await client.search_files(term="test")

        assert "OCS" in str(exc_info.value)
        assert "Failed to fetch ocs/v2.php/search/providers/files/search (status 500)" in str(exc_info.value)

    async def test_search_files_multiple_results(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test file search with multiple results."""
        mock_response = create_mock_response(
            status_code=200,
            json_data={
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
            },
        )
        mock_http_client.get.return_value = mock_response

        result = await client.search_files(term="test")

        assert len(result) == 2
        assert result[0].name == "file1.txt"
        assert result[1].name == "file2.txt"

    async def test_search_files_no_results(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test file search when no results found."""
        mock_response = create_mock_response(status_code=200, json_data={"ocs": {"data": {"entries": []}}})
        mock_http_client.get.return_value = mock_response

        result = await client.search_files(term="nonexistent")

        assert result == []

    async def test_get_file_activities_single_file(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test file activities with a single file per activity."""
        mock_response = create_mock_response(
            status_code=200,
            json_data={
                "ocs": {
                    "data": [
                        {
                            "activity_id": 2282,
                            "app": "files",
                            "type": "file_changed",
                            "user": "testuser",
                            "subject": "You changed test.docx",
                            "message": None,
                            "link": "https://nextcloud.example.com/f/31826",
                            "object_type": "files",
                            "object_id": 31826,
                            "object_name": "/test.docx",
                            "datetime": "2026-01-20T13:15:50+00:00",
                        }
                    ]
                }
            },
            headers={"x-activity-last-given": "2281"},
        )
        mock_http_client.get.return_value = mock_response

        result = await client.get_file_activities(limit=5)

        assert len(result.results) == 1
        assert result.last_given == 2281
        activity = result.results[0]
        assert activity.activity_id == 2282
        assert activity.action == "file_changed"
        assert len(activity.files) == 1
        assert activity.files[0].id == 31826
        assert activity.files[0].name == "test.docx"
        assert activity.files[0].path == "test.docx"

    async def test_get_file_activities_multi_file_with_subject_rich(
        self, client: OCSClient, mock_http_client: AsyncMock
    ) -> None:
        """Test file activities with multiple files using subject_rich."""
        mock_response = create_mock_response(
            status_code=200,
            json_data={
                "ocs": {
                    "data": [
                        {
                            "activity_id": 2217,
                            "app": "files",
                            "type": "file_created",
                            "user": "testuser",
                            "subject": "You created Drive.png, Docs.png and 3 more",
                            "message": None,
                            "link": "https://nextcloud.example.com/f/33485",
                            "object_type": "files",
                            "object_id": 33485,
                            "object_name": "/Drive.png",
                            "datetime": "2026-01-13T16:07:43+00:00",
                            "subject_rich": [
                                "You created {file1}, {file2} and {count} more",
                                {
                                    "file1": {
                                        "type": "file",
                                        "id": "33485",
                                        "name": "Drive.png",
                                        "path": "Drive.png",
                                        "link": "https://nextcloud.example.com/f/33485",
                                    },
                                    "file2": {
                                        "type": "file",
                                        "id": "33482",
                                        "name": "Docs.png",
                                        "path": "Docs.png",
                                        "link": "https://nextcloud.example.com/f/33482",
                                    },
                                    "file3": {
                                        "type": "file",
                                        "id": "33483",
                                        "name": "element.png",
                                        "path": "element.png",
                                        "link": "https://nextcloud.example.com/f/33483",
                                    },
                                    "count": {"type": "highlight", "id": "3", "name": "3"},
                                },
                            ],
                        }
                    ]
                }
            },
            headers={"x-activity-last-given": "2199"},
        )
        mock_http_client.get.return_value = mock_response

        result = await client.get_file_activities(limit=5)

        assert len(result.results) == 1
        activity = result.results[0]
        assert activity.activity_id == 2217
        assert activity.action == "file_created"
        # Should have 3 files from subject_rich (only type=file entries)
        assert len(activity.files) == 3
        assert activity.files[0].id == 33485
        assert activity.files[0].name == "Drive.png"
        assert activity.files[0].link == "https://nextcloud.example.com/f/33485"
        assert activity.files[1].id == 33482
        assert activity.files[1].name == "Docs.png"
        assert activity.files[2].id == 33483
        assert activity.files[2].name == "element.png"

    async def test_get_file_activities_multi_file_with_objects_dict(
        self, client: OCSClient, mock_http_client: AsyncMock
    ) -> None:
        """Test file activities with multiple files using objects dict fallback."""
        mock_response = create_mock_response(
            status_code=200,
            json_data={
                "ocs": {
                    "data": [
                        {
                            "activity_id": 2217,
                            "app": "files",
                            "type": "file_created",
                            "user": "testuser",
                            "subject": "You created multiple files",
                            "message": None,
                            "link": "https://nextcloud.example.com/f/33485",
                            "object_type": "files",
                            "object_id": 33485,
                            "object_name": "/Drive.png",
                            "datetime": "2026-01-13T16:07:43+00:00",
                            "objects": {
                                "33485": "/Drive.png",
                                "33482": "/Docs.png",
                                "33483": "/element.png",
                            },
                        }
                    ]
                }
            },
            headers={"x-activity-last-given": "2199"},
        )
        mock_http_client.get.return_value = mock_response

        result = await client.get_file_activities(limit=5)

        assert len(result.results) == 1
        activity = result.results[0]
        assert len(activity.files) == 3
        # Files from objects dict should have no links
        file_ids = {f.id for f in activity.files}
        assert file_ids == {33485, 33482, 33483}
        for f in activity.files:
            assert f.link is None

    async def test_get_file_activities_sharing_included(self, client: OCSClient, mock_http_client: AsyncMock) -> None:
        """Test that sharing activities are included (object_type=files filter)."""
        mock_response = create_mock_response(
            status_code=200,
            json_data={
                "ocs": {
                    "data": [
                        {
                            "activity_id": 2191,
                            "app": "files_sharing",
                            "type": "shared",
                            "user": "testuser",
                            "subject": "You shared document.docx",
                            "message": None,
                            "link": "https://nextcloud.example.com/f/22137",
                            "object_type": "files",
                            "object_id": 22137,
                            "object_name": "/document.docx",
                            "datetime": "2026-01-07T15:15:54+00:00",
                        }
                    ]
                }
            },
            headers={"x-activity-last-given": "2190"},
        )
        mock_http_client.get.return_value = mock_response

        result = await client.get_file_activities(limit=5)

        # Sharing activity should be included (app=files_sharing but object_type=files)
        assert len(result.results) == 1
        activity = result.results[0]
        assert activity.activity_id == 2191
        assert activity.action == "shared"
        assert len(activity.files) == 1
        assert activity.files[0].name == "document.docx"

    async def test_get_file_activities_filters_non_file_object_types(
        self, client: OCSClient, mock_http_client: AsyncMock
    ) -> None:
        """Test that activities with non-file object_type are filtered out."""
        mock_response = create_mock_response(
            status_code=200,
            json_data={
                "ocs": {
                    "data": [
                        {
                            "activity_id": 2282,
                            "app": "files",
                            "type": "file_changed",
                            "user": "testuser",
                            "subject": "You changed test.docx",
                            "message": None,
                            "link": "https://nextcloud.example.com/f/31826",
                            "object_type": "files",
                            "object_id": 31826,
                            "object_name": "/test.docx",
                            "datetime": "2026-01-20T13:15:50+00:00",
                        },
                        {
                            "activity_id": 2283,
                            "app": "comments",
                            "type": "comment_added",
                            "user": "testuser",
                            "subject": "You commented",
                            "message": None,
                            "link": "https://nextcloud.example.com/comment/123",
                            "object_type": "comment",
                            "object_id": 123,
                            "object_name": "comment",
                            "datetime": "2026-01-20T13:16:00+00:00",
                        },
                    ]
                }
            },
            headers={"x-activity-last-given": "2281"},
        )
        mock_http_client.get.return_value = mock_response

        result = await client.get_file_activities(limit=5)

        # Only file activity should be included
        assert len(result.results) == 1
        assert result.results[0].activity_id == 2282


class TestActivityExtractFiles:
    """Tests for Activity.extract_files() method."""

    def test_extract_files_from_subject_rich(self) -> None:
        """Test extracting files from subject_rich field."""
        activity = Activity(
            activity_id=2217,
            app="files",
            type="file_created",
            user="testuser",
            subject="You created files",
            message=None,
            link="https://nextcloud.example.com/f/33485",
            object_type="files",
            object_id=33485,
            object_name="/Drive.png",
            datetime=datetime(2026, 1, 13, 16, 7, 43),
            subject_rich=[
                "You created {file1}, {file2}",
                {
                    "file1": {
                        "type": "file",
                        "id": "33485",
                        "name": "Drive.png",
                        "path": "Drive.png",
                        "link": "https://nextcloud.example.com/f/33485",
                    },
                    "file2": {
                        "type": "file",
                        "id": "33482",
                        "name": "Docs.png",
                        "path": "Docs.png",
                        "link": "https://nextcloud.example.com/f/33482",
                    },
                },
            ],
        )

        files = activity.extract_files()

        assert len(files) == 2
        assert files[0].id == 33485
        assert files[0].name == "Drive.png"
        assert files[0].link == "https://nextcloud.example.com/f/33485"
        assert files[1].id == 33482
        assert files[1].name == "Docs.png"

    def test_extract_files_from_objects_dict(self) -> None:
        """Test extracting files from objects dict when no subject_rich."""
        activity = Activity(
            activity_id=2217,
            app="files",
            type="file_created",
            user="testuser",
            subject="You created files",
            message=None,
            link="https://nextcloud.example.com/f/33485",
            object_type="files",
            object_id=33485,
            object_name="/Drive.png",
            datetime=datetime(2026, 1, 13, 16, 7, 43),
            objects={
                "33485": "/Drive.png",
                "33482": "/Documents/Docs.png",
            },
        )

        files = activity.extract_files()

        assert len(files) == 2
        file_by_id = {f.id: f for f in files}
        assert file_by_id[33485].name == "Drive.png"
        assert file_by_id[33485].path == "Drive.png"
        assert file_by_id[33485].link is None
        assert file_by_id[33482].name == "Docs.png"
        assert file_by_id[33482].path == "Documents/Docs.png"

    def test_extract_files_fallback_to_single_object(self) -> None:
        """Test fallback to single object when no subject_rich or objects."""
        activity = Activity(
            activity_id=2282,
            app="files",
            type="file_changed",
            user="testuser",
            subject="You changed test.docx",
            message=None,
            link="https://nextcloud.example.com/f/31826",
            object_type="files",
            object_id=31826,
            object_name="/Documents/test.docx",
            datetime=datetime(2026, 1, 20, 13, 15, 50),
        )

        files = activity.extract_files()

        assert len(files) == 1
        assert files[0].id == 31826
        assert files[0].name == "test.docx"
        assert files[0].path == "Documents/test.docx"
        assert files[0].link is None

    def test_extract_files_ignores_non_file_types_in_subject_rich(self) -> None:
        """Test that non-file types in subject_rich are ignored."""
        activity = Activity(
            activity_id=2217,
            app="files",
            type="file_created",
            user="testuser",
            subject="You created files",
            message=None,
            link="https://nextcloud.example.com/f/33485",
            object_type="files",
            object_id=33485,
            object_name="/Drive.png",
            datetime=datetime(2026, 1, 13, 16, 7, 43),
            subject_rich=[
                "You created {file1} and {count} more",
                {
                    "file1": {
                        "type": "file",
                        "id": "33485",
                        "name": "Drive.png",
                        "path": "Drive.png",
                        "link": "https://nextcloud.example.com/f/33485",
                    },
                    "count": {"type": "highlight", "id": "3", "name": "3"},
                },
            ],
        )

        files = activity.extract_files()

        # Only the file should be extracted, not the highlight
        assert len(files) == 1
        assert files[0].id == 33485
        assert files[0].name == "Drive.png"
