from pydantic import BaseModel, computed_field

from app.core.config import settings


class Room(BaseModel):
    id: str
    name: str
    slug: str

    @computed_field
    @property
    def url(self) -> str:
        return f"{settings.CONVERSATION_URL}/{self.slug}"
