from datetime import datetime

from pydantic import BaseModel, computed_field

from app.core.config import settings


class Activity(BaseModel):
    activity_id: int
    app: str
    type: str
    user: str
    subject: str
    message: str | None
    link: str
    object_type: str
    object_id: int
    object_name: str
    datetime: datetime
    objects: dict[str, str] | None = None

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


class File(BaseModel):
    """Represents a unique file extracted from Nextcloud activities."""

    id: int
    name: str
    path: str
    updated_at: datetime
    action: str

    @computed_field
    @property
    def url(self) -> str:
        return f"{settings.OCS_URL}/f/{self.id}"

    @computed_field
    @property
    def title(self) -> str:
        """Filename without path, for consistency with other widgets."""
        return self.name.split("/")[-1]


class FileListResponse(BaseModel):
    """Paginated response for file list."""

    results: list[File]
    count: int
