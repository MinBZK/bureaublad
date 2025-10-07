"""OCS (Open Collaboration Services) client for NextCloud API.

Reference: https://docs.nextcloud.com/server/latest/developer_manual/client_apis/index.html
"""

import logging
from typing import cast

import httpx
from app.exceptions import ExternalServiceError
from app.models.activity import Activity
from app.models.search import FileSearchResult, SearchResults
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


class OCSClient:
    """Client for NextCloud OCS API.

    Handles business logic for activities, file search, calendar search, and task search.
    """

    def __init__(self, http_client: httpx.AsyncClient, base_url: str, token: str) -> None:
        """Initialize OCSClient.

        Args:
            http_client: Shared httpx.AsyncClient instance
            base_url: Base URL for the OCS service
            token: Authentication token for this request
        """
        self.client = http_client
        self.base_url = base_url.rstrip("/")
        self.token = token

    async def get_activities(
        self,
        path: str = "/ocs/v2.php/apps/activity/api/v2/activity",
        limit: int = 6,
        since: int = 0,
        filter: None | str = "files",
    ) -> list[Activity]:
        url_string = f"{path}/{filter}" if filter else path

        params = {"format": "json"}
        if since:
            params["since"] = str(since)
        if limit:
            params["limit"] = str(limit)

        url = f"{self.base_url}/{url_string.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "OCS-APIRequest": "true",
            "Accept": "application/json",
        }
        response = await self.client.get(
            url,
            params=params,
            headers=headers,
        )

        if response.status_code != 200:
            logger.error(f"OCS activities request failed: status={response.status_code}, url={url_string}")
            raise ExternalServiceError("OCS", f"Failed to fetch activities (status {response.status_code})")

        results = response.json().get("ocs", []).get("data", [])

        notes: list[Activity] = TypeAdapter(list[Activity]).validate_python(results)

        return notes

    async def search_files(
        self, term: str, path: str = "ocs/v2.php/search/providers/files/search"
    ) -> list[SearchResults]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "OCS-APIRequest": "true",
            "Accept": "application/json",
        }
        response = await self.client.get(
            url,
            params={"term": term},
            headers=headers,
        )

        if response.status_code != 200:
            logger.error(f"OCS file search failed: status={response.status_code}, url={url}")
            raise ExternalServiceError("OCS", f"Failed to search files (status {response.status_code})")

        results = response.json().get("ocs", []).get("data", []).get("entries", [])

        # Validate as FileSearchResult to handle aliases, then cast to base type
        validated = TypeAdapter(list[FileSearchResult]).validate_python(results)
        return cast(list[SearchResults], validated)

    async def search_calendar(
        self, term: str, path: str = "ocs/v2.php/search/providers/calendar/search"
    ) -> list[SearchResults]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "OCS-APIRequest": "true",
            "Accept": "application/json",
        }
        response = await self.client.get(
            url,
            params={"term": term},
            headers=headers,
        )

        if response.status_code != 200:
            logger.error(f"OCS calendar search failed: status={response.status_code}, url={url}")
            raise ExternalServiceError("OCS", f"Failed to search calendar (status {response.status_code})")

        results = response.json().get("ocs", []).get("data", []).get("entries", [])

        # Validate as FileSearchResult to handle aliases, then cast to base type
        validated = TypeAdapter(list[FileSearchResult]).validate_python(results)
        return cast(list[SearchResults], validated)

    async def search_tasks(
        self, term: str, path: str = "ocs/v2.php/search/providers/tasks/search"
    ) -> list[SearchResults]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "OCS-APIRequest": "true",
            "Accept": "application/json",
        }
        response = await self.client.get(
            url,
            params={"term": term},
            headers=headers,
        )

        if response.status_code != 200:
            logger.error(f"OCS task search failed: status={response.status_code}, url={url}")
            raise ExternalServiceError("OCS", f"Failed to search tasks (status {response.status_code})")

        results = response.json().get("ocs", []).get("data", []).get("entries", [])

        # Validate as FileSearchResult to handle aliases, then cast to base type
        validated = TypeAdapter(list[FileSearchResult]).validate_python(results)
        return cast(list[SearchResults], validated)
