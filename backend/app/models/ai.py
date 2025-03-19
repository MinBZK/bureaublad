from pydantic import BaseModel


class ChatCompletionRequest(BaseModel):
    prompt: str
