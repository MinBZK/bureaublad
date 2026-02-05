from datetime import datetime
from typing import Any, cast

from pydantic import BaseModel, computed_field

from app.core.config import settings


class FileInfo(BaseModel):
    """Single file reference within an activity."""

    id: int
    name: str
    path: str
    link: str | None = None  # Direct link from Nextcloud, may be absent


class Activity(BaseModel):
    """Raw Nextcloud activity - for parsing API response."""

    activity_id: int
    app: str
    type: str
    user: str
    subject: str
    message: str | None = None
    link: str
    object_type: str
    object_id: int
    object_name: str
    datetime: datetime
    objects: dict[str, str] | None = None
    subject_rich: list[Any] | None = None

    @computed_field
    @property
    def url(self) -> str:
        return f"{settings.OCS_URL}/f/{self.object_id}"

    @computed_field
    @property
    def date(self) -> str:
        return self.datetime.strftime("%d %b %Y")

    @computed_field
    @property
    def time(self) -> str:
        return self.datetime.strftime("%H:%M:%S")

    @computed_field
    @property
    def object_filename(self) -> str:
        return self.object_name.split("/")[-1]

    def extract_files(self) -> list[FileInfo]:
        """Extract all files from this activity.

        Priority: subject_rich (has metadata) -> objects dict -> single object
        Uses link directly from Nextcloud when available, null otherwise.
        """
        files: list[FileInfo] = []

        # Try subject_rich first (has file metadata including link)
        if self.subject_rich and len(self.subject_rich) >= 2:
            placeholders = self.subject_rich[1]
            if isinstance(placeholders, dict):
                typed_placeholders = cast(dict[str, Any], placeholders)
                for value in typed_placeholders.values():
                    if isinstance(value, dict):
                        file_data = cast(dict[str, str], value)
                        if file_data.get("type") != "file":
                            continue
                        file_id = file_data["id"]
                        file_name = file_data["name"]
                        file_path = file_data.get("path", file_name)
                        file_link: str | None = file_data.get("link")
                        files.append(
                            FileInfo(
                                id=int(file_id),
                                name=file_name,
                                path=file_path,
                                link=file_link,
                            )
                        )

        # Fallback to objects dict (no links available)
        if not files and self.objects:
            for file_id_str, file_path in self.objects.items():
                files.append(
                    FileInfo(
                        id=int(file_id_str),
                        name=file_path.lstrip("/").split("/")[-1],
                        path=file_path.lstrip("/"),
                        link=None,  # objects dict doesn't have links
                    )
                )

        # Ultimate fallback: single object
        if not files:
            files.append(
                FileInfo(
                    id=self.object_id,
                    name=self.object_name.lstrip("/").split("/")[-1],
                    path=self.object_name.lstrip("/"),
                    link=None,  # No link available
                )
            )

        return files


class FileActivity(BaseModel):
    """A file activity which may contain multiple files.

    Respects Nextcloud API contract: limit=5 means 5 activities.
    Each activity contains all affected files in the 'files' array.
    """

    activity_id: int
    datetime: datetime
    action: str  # file_created, file_changed, shared, etc.
    files: list[FileInfo]  # All files in this activity


class FileActivityResponse(BaseModel):
    """Response for file activities with cursor-based pagination."""

    results: list[FileActivity]
    last_given: int | None = None
