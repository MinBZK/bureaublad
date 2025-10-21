from pydantic import BaseModel


class ChatCompletionRequest(BaseModel):
    prompt: str


class StreamChunk(BaseModel):
    id: str
    content: str | None = None
    finish_reason: str | None = None
