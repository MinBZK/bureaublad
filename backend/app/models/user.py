from pydantic import BaseModel


class User(BaseModel):
    sub: str
    access_token: str
