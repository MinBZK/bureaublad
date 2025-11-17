from datetime import datetime

from pydantic import BaseModel, computed_field


class Document(BaseModel):
    id: str
    title: str
    url: str | None
    mimetype: str | None
    updated_at: str

    @computed_field
    @property
    def updated_date(self) -> str:
        return datetime.fromisoformat(self.updated_at).strftime("%d %b %Y %H:%M")
