from pydantic import BaseModel


class Conversation(BaseModel):
    title: str
