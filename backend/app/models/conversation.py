from pydantic import BaseModel, computed_field

from app.core.config import settings


class Conversation(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str

    @computed_field
    @property
    def url(self) -> str:
        return f"{settings.CONVERSATION_URL}/chat/{self.id}/"
