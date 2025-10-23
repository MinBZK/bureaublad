from pydantic import BaseModel, ConfigDict, computed_field
from pydantic.alias_generators import to_camel

from app.core.config import settings


class GristOrganization(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        alias_generator=to_camel,
    )
    id: int
    name: str
    domain: str | None
    access: str
    created_at: str
    updated_at: str


class GristDocument(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        alias_generator=to_camel,
    )
    id: str
    name: str
    access: str
    is_pinned: bool
    url_id: str | None
    created_at: str
    updated_at: str

    @computed_field
    @property
    def url(self) -> str:
        return f"{settings.GRIST_URL}/{self.url_id}/"


class GristWorkspace(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        alias_generator=to_camel,
    )
    id: int
    name: str
    access: str
    org_domain: str
    docs: list[GristDocument]
