from pydantic import BaseModel


class PaginatedResponse[T](BaseModel):
    count: int
    results: list[T]
