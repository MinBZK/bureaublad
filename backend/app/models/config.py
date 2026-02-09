from pydantic import BaseModel


class Component(BaseModel):
    name: str
    enabled: bool


class Service(BaseModel):
    name: str
    enabled: bool


class ApplicationsConfig(BaseModel):
    enabled: bool = False
    id: str
    icon: str | None = None
    url: str | None = None
    title: str | None = None
    iframe: bool = False


class OIDCConfig(BaseModel):
    discovery_endpoint: str
    username_claim: str


class ConfigResponse(BaseModel):
    applications: list[ApplicationsConfig]
    helpdesk_url: str
    theme_css: str
    silent_login: bool = False
