"""OCS (Open Collaboration Services) client for NextCloud API.

Reference: https://docs.nextcloud.com/server/latest/developer_manual/client_apis/index.html
"""

import logging
from typing import cast

from app.clients.base import BaseAPIClient
from app.models.activity import Activity, FileActivity, FileActivityResponse
from app.models.search import FileSearchResult, SearchResults

logger = logging.getLogger(__name__)


class OCSClient(BaseAPIClient):
    """Client for NextCloud OCS API.

    Handles business logic for activities, file search, calendar search, and task search.
    """

    service_name = "NextCloud OCS"

    def _auth_headers(self) -> dict[str, str]:
        headers = super()._auth_headers()
        headers["OCS-APIRequest"] = "true"
        headers["Accept"] = "application/json"
        return headers

    async def get_file_activities(
        self,
        limit: int = 5,
        since: int = 0,
    ) -> FileActivityResponse:
        """Get file activities with cursor-based pagination.

        Fetches activities, filters to file-related activities (including sharing),
        and returns with all files per activity preserved.
        """
        url_string = "ocs/v2.php/apps/activity/api/v2/activity/files"

        params: dict[str, str] = {"format": "json"}
        if since:
            params["since"] = str(since)
        if limit:
            params["limit"] = str(limit)

        activities, headers = await self._get_resource_with_headers(
            path=url_string,
            model_type=list[Activity],
            params=params,
            response_parser=lambda data: data.get("ocs", {}).get("data", []),
        )

        # Filter by object_type == "files" (includes files + files_sharing apps)
        file_activities: list[FileActivity] = []
        for activity in activities:
            if activity.object_type == "files":
                file_activities.append(
                    FileActivity(
                        activity_id=activity.activity_id,
                        datetime=activity.datetime,
                        action=activity.type,
                        files=activity.extract_files(),
                    )
                )

        # Get last_given from header for cursor-based pagination
        # Note: httpx returns headers in lowercase
        last_given_str = headers.get("x-activity-last-given")
        last_given = int(last_given_str) if last_given_str else None

        return FileActivityResponse(results=file_activities, last_given=last_given)

    async def search_files(
        self, term: str, path: str = "ocs/v2.php/search/providers/files/search"
    ) -> list[SearchResults]:
        validated = await self._get_resource(
            path=path,
            model_type=list[FileSearchResult],
            params={"term": term},
            response_parser=lambda data: data.get("ocs", {}).get("data", {}).get("entries", []),
        )
        return cast(list[SearchResults], validated)
