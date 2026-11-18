from datetime import datetime

from pydantic import BaseModel


class SearchResult(BaseModel):
    id: str
    service: str
    title: str
    path: str
    updated_at: datetime
    url: str | None = None


class SearchResponse(BaseModel):
    results: list[SearchResult]
