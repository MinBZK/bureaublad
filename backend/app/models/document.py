from datetime import datetime
from urllib.parse import urlparse

from pydantic import BaseModel, computed_field, model_validator

from app.core.config import settings


class Document(BaseModel):
    id: str
    title: str
    url: str | None
    url_preview: str | None = None
    mimetype: str | None
    updated_at: str

    @model_validator(mode="after")
    def set_url_preview(self) -> "Document":
        if not self.url:  # folders do not have an URL, but we want to be able to preview them as well
            self.url = f"{settings.DRIVE_URL}/explorer/items/{self.id}"
            self.url_preview = f"{settings.DRIVE_URL}/explorer/items/{self.id}"

        if not self.url_preview and self.url:
            parsed = urlparse(self.url)
            self.url_preview = f"{parsed.scheme}://{parsed.netloc}/explorer/items/files/{self.id}"
        return self

    @computed_field
    @property
    def updated_date(self) -> str:
        return datetime.fromisoformat(self.updated_at).strftime("%d %b %Y %H:%M")
