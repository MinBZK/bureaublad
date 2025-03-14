from datetime import datetime

from pydantic import BaseModel, computed_field

from app.config import settings


class Note(BaseModel):
    id: str
    # abilities: dict[str, bool]  # noqa: ERA001
    created_at: str
    # creator: str # noqa: ERA001
    # depth: int # noqa: ERA001
    # excerpt: str | None # noqa: ERA001
    # is_favorite: bool # noqa: ERA001
    # link_role: str # noqa: ERA001
    # link_reach: str # noqa: ERA001
    # nb_accesses: int # noqa: ERA001
    # numchild: int # noqa: ERA001
    path: str
    title: str
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
