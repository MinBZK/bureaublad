from pydantic import BaseModel


class Component(BaseModel):
    name: str
    enabled: bool


class Service(BaseModel):
    name: str
    enabled: bool


class SidebarLink(BaseModel):
    icon: str
    url: str
    title: str
    iframe: bool = False


class OIDCConfig(BaseModel):
    discovery_endpoint: str
    username_claim: str


class ApplicationsConfig(BaseModel):
    ai: bool = False
    docs: bool = False
    drive: bool = False
    calendar: bool = False
    task: bool = False
    meet: bool = False
    ocs: bool = False
    grist: bool = False
    conversation: bool = False


class ConfigResponse(BaseModel):
    applications: list[SidebarLink]
    theme_css: str
    cards: ApplicationsConfig
    silent_login: bool = False
