from datetime import datetime

from pydantic import BaseModel, computed_field

from app.config import settings


class Activity(BaseModel):
    activity_id: int
    app: str
    type: str
    user: str
    subject: str
    message: str
    link: str
    object_type: str
    object_id: int
    object_name: str
    datetime: datetime

    @computed_field
    @property
    def url(self) -> str:
        return f"{settings.OCS_URL}/f/{self.object_id}"

    @computed_field
    @property
    def date(self) -> str:
        return self.datetime.strftime("%d %b %Y")

    @computed_field
    @property
    def time(self) -> str:
        return self.datetime.strftime("%H:%M:%S")

    @computed_field
    @property
    def object_filename(self) -> str:
        return self.object_name.split("/")[-1]
