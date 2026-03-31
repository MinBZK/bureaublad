"""OCS (Open Collaboration Services) client for NextCloud API.

Reference: https://docs.nextcloud.com/server/latest/developer_manual/client_apis/index.html
"""

import logging
import xml.etree.ElementTree as ET

from app.clients.base import BaseAPIClient
from app.exceptions import ExternalServiceError
from app.models.activity import Activity, FileActivity, FileActivityResponse, FileInfo
from app.models.search import FileSearchResult

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
        limit: int = 50,
        since: int = 0,
        is_favorite: bool = False,
    ) -> FileActivityResponse:
        """Get file activities with cursor-based pagination.

        When is_favorite=True, fetches favorite files via WebDAV REPORT instead of the activity feed.
        Otherwise fetches activities, filters to file-related activities (including sharing),
        and returns with all files per activity preserved.
        """
        if is_favorite:
            return await self._get_favorite_files()

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

    async def _get_favorite_files(self) -> FileActivityResponse:
        """Fetch favorite files using Nextcloud WebDAV REPORT.

        Reference: https://docs.nextcloud.com/server/latest/developer_manual/client_apis/webdav/index.html
        """
        # Resolve current user ID
        url = self._build_url("ocs/v2.php/cloud/user")
        user_response = await self.client.get(url, params={"format": "json"}, headers=self._auth_headers())
        if user_response.status_code != 200:
            raise ExternalServiceError(self.service_name, f"Failed to resolve current user (status {user_response.status_code})")
        user_id = user_response.json().get("ocs", {}).get("data", {}).get("id", "")

        # WebDAV REPORT to filter favorite files
        xml_body = (
            '<?xml version="1.0"?>'
            '<oc:filter-files xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">'
            "<d:prop>"
            "<d:getlastmodified/><d:getcontenttype/><d:displayname/><oc:fileid/><oc:favorite/>"
            "</d:prop>"
            "<oc:filter-rules><oc:favorite>1</oc:favorite></oc:filter-rules>"
            "</oc:filter-files>"
        )
        report_url = self._build_url(f"remote.php/dav/files/{user_id}/")
        headers = self._auth_headers()
        headers["Content-Type"] = "application/xml"
        headers["Depth"] = "infinity"

        response = await self.client.request("REPORT", report_url, content=xml_body.encode(), headers=headers)
        if response.status_code not in (200, 207):
            raise ExternalServiceError(self.service_name, f"Failed to fetch favorites (status {response.status_code})")

        # Parse WebDAV multistatus XML response
        DAV = "DAV:"
        OC = "http://owncloud.org/ns"
        root = ET.fromstring(response.text)
        base_path = f"/remote.php/dav/files/{user_id}/"
        file_activities: list[FileActivity] = []

        for resp in root.findall(f"{{{DAV}}}response"):
            href = resp.findtext(f"{{{DAV}}}href") or ""
            propstat = resp.find(f"{{{DAV}}}propstat")
            if propstat is None:
                continue
            if "200" not in (propstat.findtext(f"{{{DAV}}}status") or ""):
                continue
            prop = propstat.find(f"{{{DAV}}}prop")
            if prop is None:
                continue

            display_name = prop.findtext(f"{{{DAV}}}displayname") or href.rstrip("/").split("/")[-1]
            file_id_str = prop.findtext(f"{{{OC}}}fileid")
            file_id = int(file_id_str) if file_id_str else None
            path = href[len(base_path):] if href.startswith(base_path) else href
            link = f"{self.base_url}/f/{file_id}" if file_id else None

            file_activities.append(FileActivity(files=[FileInfo(id=file_id, name=display_name, path=path, link=link)]))

        return FileActivityResponse(results=file_activities, last_given=None)

    async def search_files(
        self, term: str, path: str = "ocs/v2.php/search/providers/files/search"
    ) -> FileActivityResponse:
        validated = await self._get_resource(
            path=path,
            model_type=list[FileSearchResult],
            params={"format": "json", "term": term},
            response_parser=lambda data: data.get("ocs", {}).get("data", {}).get("entries", []),
        )
        search_results: list[FileSearchResult] = validated
        file_activities = [FileActivity(files=[FileInfo(name=entry.name, link=entry.url)]) for entry in search_results]
        return FileActivityResponse(results=file_activities, last_given=None)
