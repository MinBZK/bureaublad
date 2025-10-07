import logging
from typing import cast

import httpx
from bureaublad_api.exceptions import ExternalServiceError
from bureaublad_api.models.activity import Activity
from bureaublad_api.models.search import FileSearchResult, SearchResults
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


# https://docs.nextcloud.com/server/latest/developer_manual/client_apis/index.html
class OCSClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token
        self.client = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "OCS-APIRequest": "true",
                "Accept": "application/json",
            }
        )

    def get_activities(
        self,
        path: str = "/ocs/v2.php/apps/activity/api/v2/activity",
        limit: int = 6,
        since: int = 0,
        filter: None | str = "files",
    ) -> list[Activity]:
        url_string = f"{self.base_url}/{path}" if not filter else f"{self.base_url}/{path}/{filter}"

        url = httpx.URL(url_string, params={"format": "json"})

        if since:
            url = url.copy_add_param("since", str(since))

        if limit:
            url = url.copy_add_param("limit", str(limit))

        response = self.client.request("GET", url)
        if response.status_code != 200:
            logger.error(f"OCS activities request failed: status={response.status_code}, url={url}")
            raise ExternalServiceError("OCS", f"Failed to fetch activities (status {response.status_code})")

        results = response.json().get("ocs", []).get("data", [])

        notes: list[Activity] = TypeAdapter(list[Activity]).validate_python(results)

        return notes

    def search_files(self, term: str, path: str = "ocs/v2.php/search/providers/files/search") -> list[SearchResults]:
        url = httpx.URL(f"{self.base_url}/{path}", params={"term": term})

        response = self.client.request("GET", url)
        if response.status_code != 200:
            logger.error(f"OCS file search failed: status={response.status_code}, url={url}")
            raise ExternalServiceError("OCS", f"Failed to search files (status {response.status_code})")

        results = response.json().get("ocs", []).get("data", []).get("entries", [])

        # Validate as FileSearchResult to handle aliases, then cast to base type
        validated = TypeAdapter(list[FileSearchResult]).validate_python(results)
        return cast(list[SearchResults], validated)

    def search_calendar(
        self, term: str, path: str = "ocs/v2.php/search/providers/calendar/search"
    ) -> list[SearchResults]:
        url = httpx.URL(f"{self.base_url}/{path}", params={"term": term})

        response = self.client.request("GET", url)

        if response.status_code != 200:
            logger.error(f"OCS calendar search failed: status={response.status_code}, url={url}")
            raise ExternalServiceError("OCS", f"Failed to search calendar (status {response.status_code})")

        results = response.json().get("ocs", []).get("data", []).get("entries", [])

        # Validate as FileSearchResult to handle aliases, then cast to base type
        validated = TypeAdapter(list[FileSearchResult]).validate_python(results)
        return cast(list[SearchResults], validated)

    def search_tasks(self, term: str, path: str = "ocs/v2.php/search/providers/tasks/search") -> list[SearchResults]:
        url = httpx.URL(f"{self.base_url}/{path}", params={"term": term})

        response = self.client.request("GET", url)
        if response.status_code != 200:
            logger.error(f"OCS task search failed: status={response.status_code}, url={url}")
            raise ExternalServiceError("OCS", f"Failed to search tasks (status {response.status_code})")

        results = response.json().get("ocs", []).get("data", []).get("entries", [])

        # Validate as FileSearchResult to handle aliases, then cast to base type
        validated = TypeAdapter(list[FileSearchResult]).validate_python(results)
        return cast(list[SearchResults], validated)
