"""OCS (Open Collaboration Services) client for NextCloud API.

Reference: https://docs.nextcloud.com/server/latest/developer_manual/client_apis/index.html
"""

import logging
from typing import cast

from app.clients.base import BaseAPIClient
from app.models.activity import Activity, File, FileListResponse
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

    async def get_activities(
        self,
        path: str = "ocs/v2.php/apps/activity/api/v2/activity",
        limit: int = 5,
        since: int = 0,
        filter: None | str = "files",
    ) -> list[Activity]:
        url_string = f"{path}/{filter}" if filter else path

        params = {"format": "json"}
        if since:
            params["since"] = str(since)
        if limit:
            params["limit"] = str(limit)

        notes = await self._get_resource(
            path=url_string,
            model_type=list[Activity],
            params=params,
            response_parser=lambda data: data.get("ocs", {}).get("data", []),
        )
        return notes

    async def get_files(
        self,
        page: int = 1,
        page_size: int = 3,
    ) -> FileListResponse:
        """Get unique files from activities, sorted by most recent activity.

        Fetches activities, filters to only file activities, extracts all files
        (including from multi-file activities), deduplicates by file ID keeping
        the most recent, and returns a paginated list.
        """
        # Fetch more activities than needed to ensure we get enough unique files
        fetch_limit = max(50, page_size * page * 3)

        activities = await self.get_activities(
            limit=fetch_limit,
            since=0,
            filter="files",
        )

        # Extract unique files from activities (first occurrence = most recent)
        files_dict: dict[int, File] = {}

        for activity in activities:
            if activity.app != "files":
                continue

            if activity.objects:
                for file_id_str, file_path in activity.objects.items():
                    file_id = int(file_id_str)
                    if file_id not in files_dict:
                        files_dict[file_id] = File(
                            id=file_id,
                            name=file_path.lstrip("/"),
                            path=file_path,
                            updated_at=activity.datetime,
                            action=activity.type,
                        )
            else:
                file_id = activity.object_id
                if file_id not in files_dict:
                    files_dict[file_id] = File(
                        id=file_id,
                        name=activity.object_name.lstrip("/"),
                        path=activity.object_name,
                        updated_at=activity.datetime,
                        action=activity.type,
                    )

        # Sort by updated_at descending
        all_files = sorted(files_dict.values(), key=lambda f: f.updated_at, reverse=True)

        # Paginate
        total_count = len(all_files)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_files = all_files[start_idx:end_idx]

        return FileListResponse(results=paginated_files, count=total_count)

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
