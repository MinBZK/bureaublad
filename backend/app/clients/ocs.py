import httpx
from app.models import Activity, FileSearchResult, SearchResults
from pydantic import TypeAdapter


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
            return TypeAdapter(list[Activity]).validate_python([])

        results = response.json().get("ocs", []).get("data", [])

        notes: list[Activity] = TypeAdapter(list[Activity]).validate_python(results)

        return notes

    def search_files(self, term: str, path: str = "ocs/v2.php/search/providers/files/search") -> list[SearchResults]:
        url = httpx.URL(f"{self.base_url}/{path}", params={"term": term})

        response = self.client.request("GET", url)
        if response.status_code != 200:
            return TypeAdapter(list[FileSearchResult]).validate_python([])

        results = response.json().get("ocs", []).get("data", []).get("entries", [])

        search_results: list[SearchResults] = TypeAdapter(list[FileSearchResult]).validate_python(results)

        return search_results

    def search_calendar(
        self, term: str, path: str = "ocs/v2.php/search/providers/calendar/search"
    ) -> list[SearchResults]:
        url = httpx.URL(f"{self.base_url}/{path}", params={"term": term})

        response = self.client.request("GET", url)

        if response.status_code != 200:
            return TypeAdapter(list[FileSearchResult]).validate_python([])

        results = response.json().get("ocs", []).get("data", []).get("entries", [])

        search_results: list[SearchResults] = TypeAdapter(list[FileSearchResult]).validate_python(results)

        return search_results

    def search_tasks(self, term: str, path: str = "ocs/v2.php/search/providers/tasks/search") -> list[SearchResults]:
        url = httpx.URL(f"{self.base_url}/{path}", params={"term": term})

        response = self.client.request("GET", url)
        if response.status_code != 200:
            return TypeAdapter(list[FileSearchResult]).validate_python([])

        results = response.json().get("ocs", []).get("data", []).get("entries", [])

        search_results: list[SearchResults] = TypeAdapter(list[FileSearchResult]).validate_python(results)

        return search_results
