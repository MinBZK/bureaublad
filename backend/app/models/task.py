from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    title: str
    start: datetime | None
    end: datetime | None
