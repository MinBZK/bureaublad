import asyncio
import json
import time
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[dict[str, Any]]
    stream: bool = False


async def generate_stream_response():
    """Generate a simple mock streaming response in OpenAI format."""
    chunk_id = "chatcmpl-mock-123"
    created = int(time.time())
    model = "gpt-4o-mini"

    # Simple static response split into 3 chunks
    response_chunks = ["This is a mock response ", "from the AI ", "mock server."]

    # First chunk with role
    first_chunk = {
        "id": chunk_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "system_fingerprint": "fp_mock",
        "choices": [
            {
                "index": 0,
                "delta": {"role": "assistant", "content": ""},
                "logprobs": None,
                "finish_reason": None,
            }
        ],
    }
    yield f"data: {json.dumps(first_chunk)}\n\n"
    await asyncio.sleep(0.05)

    # Stream content in 3 chunks
    for content in response_chunks:
        content_chunk = {
            "id": chunk_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "system_fingerprint": "fp_mock",
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": content},
                    "logprobs": None,
                    "finish_reason": None,
                }
            ],
        }
        yield f"data: {json.dumps(content_chunk)}\n\n"
        await asyncio.sleep(0.05)

    # Final chunk with finish_reason
    final_chunk = {
        "id": chunk_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "system_fingerprint": "fp_mock",
        "choices": [
            {"index": 0, "delta": {}, "logprobs": None, "finish_reason": "stop"}
        ],
    }
    yield f"data: {json.dumps(final_chunk)}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Mock OpenAI chat completions endpoint with streaming support."""
    if request.stream:
        return StreamingResponse(
            generate_stream_response(), media_type="text/event-stream"
        )

    # Non-streaming response (fallback)
    return {
        "id": "chatcmpl-mock-123",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response from the AI mock server.",
                },
                "finish_reason": "stop",
            }
        ],
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
