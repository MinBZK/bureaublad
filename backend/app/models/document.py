from datetime import datetime

from pydantic import BaseModel, computed_field


class Document(BaseModel):
    title: str
    url: str
    mimetype: str
    updated_at: str

    @computed_field
    @property
    def updated_date(self) -> str:
        return datetime.fromisoformat(self.updated_at).strftime("%d %b %Y")
