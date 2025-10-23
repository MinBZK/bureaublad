from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class GristOrganization(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        alias_generator=to_camel,
    )
    name: str
    domain: str | None
    access: str
    created_at: str
    updated_at: str
