"""OCS (Open Collaboration Services) client for NextCloud API.

Reference: https://docs.nextcloud.com/server/latest/developer_manual/client_apis/index.html
"""

import logging
from typing import cast

from app.clients.base import BaseAPIClient
from app.models.activity import Activity
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
