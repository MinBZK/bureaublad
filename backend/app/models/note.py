from datetime import datetime

from pydantic import BaseModel, computed_field

from app.core.config import settings


class Note(BaseModel):
    id: str
    created_at: str
    path: str
    title: str | None
    updated_at: str
    user_roles: list[str]

    @computed_field
    @property
    def url(self) -> str:
        return f"{settings.DOCS_URL}/docs/{self.id}/"

    @computed_field
    @property
    def updated_date(self) -> str:
        return datetime.fromisoformat(self.updated_at).strftime("%d %b %Y")
