from pydantic import BaseModel, computed_field

from app.core.config import settings


class Room(BaseModel):
    id: str
    name: str
    slug: str
    pin_code: str | None = None

    @computed_field
    @property
    def url(self) -> str:
        return f"{settings.MEET_URL}/{self.slug}"
