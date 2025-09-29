from pydantic import BaseModel


class Meeting(BaseModel):
    title: str