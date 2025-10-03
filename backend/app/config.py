import json
import secrets
from typing import Annotated, Any, Literal

from jose.constants import ALGORITHMS
from pydantic import AnyUrl, BeforeValidator, HttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors_origins(v: Any) -> list[str] | str:  # noqa: ANN401
    if isinstance(v, str):
        if v == "*":
            return "*"
        if not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
    if isinstance(v, list):
        for idx, item in enumerate(v):  # type: ignore[misc]
            if not isinstance(item, str):
                raise TypeError(f"CORS_ALLOW_ORIGINS list item at index {idx} must be string, got {type(item)}")  # type: ignore[arg-type]
        return v  # type: ignore[return-value]
    raise ValueError(f"CORS_ALLOW_ORIGINS must be string or list, got {type(v)}")


def parse_sidebar_links(v: Any) -> list[dict[str, str]]:  # noqa: ANN401
    if isinstance(v, str):
        if not v.strip():
            return []
        try:
            parsed: Any = json.loads(v)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in SIDEBAR_LINKS_JSON: {e}")

        if not isinstance(parsed, list):
            raise ValueError("SIDEBAR_LINKS_JSON must be a JSON array")

        for idx, link in enumerate(parsed):  # type: ignore[misc]
            if not isinstance(link, dict):
                raise ValueError(f"Link at index {idx} must be an object")
            required = {"icon", "url", "title"}
            if not required.issubset(link.keys()):  # type: ignore[arg-type]
                raise ValueError(f"Link at index {idx} missing fields: {required - link.keys()}")

            # Validate URL is valid http/https
            try:
                HttpUrl(link["url"])  # type: ignore[arg-type]
            except Exception as e:
                raise ValueError(f"Link at index {idx} has invalid URL: {e}")

        return parsed  # type: ignore[return-value]

    if isinstance(v, list):
        return v  # type: ignore[return-value]

    raise ValueError(f"SIDEBAR_LINKS_JSON must be string or list, got {type(v)}")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("dev.env", ".env", "prod.env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = False
    ENVIRONMENT: Literal["dev", "prod"] = "prod"

    # OpenID Connect
    OIDC_CLIENT_ID: str = "bureaublad-frontend"
    OIDC_CLIENT_SECRET: str | None = None
    OIDC_AUTHORIZATION_ENDPOINT: str = ""
    OIDC_TOKEN_ENDPOINT: str = ""
    OIDC_JWKS_ENDPOINT: str = ""
    OIDC_USERNAME_CLAIM: str = "preferred_username"
    OIDC_SCOPES: dict[str, str] = {"openid": "", "profile": "", "email": ""}
    OIDC_AUDIENCE: str = "account"
    OIDC_ISSUER: str = ""
    OIDC_SIGNATURE_ALGORITM: str | list[str] = [ALGORITHMS.RS256, ALGORITHMS.HS256]

    # La Suite Services
    OCS_URL: str | None = None
    OCS_AUDIENCE: str = "files"
    DOCS_URL: str | None = None
    DOCS_AUDIENCE: str = "docs"
    CALENDAR_URL: str | None = None
    CALENDAR_AUDIENCE: str = "files"
    TASK_URL: str | None = None
    TASK_AUDIENCE: str = "files"
    DRIVE_URL: str | None = None
    DRIVE_AUDIENCE: str = "drive"
    MEET_URL: str | None = None
    MEET_AUDIENCE: str = "meet"

    # AI Integration
    AI_BASE_URL: str | None = "https://api.openai.com/v1/"
    AI_MODEL: str | None = "gpt-4o"
    AI_API_KEY: str | None = None

    # Grist
    GRIST_BASE_URL: str | None = None

    THEME_CSS_URL: str = ""

    SIDEBAR_LINKS_JSON: Annotated[list[dict[str, str]], BeforeValidator(parse_sidebar_links)] = []

    CORS_ALLOW_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors_origins)] = []
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def ocs_enabled(self) -> bool:
        return self.OCS_URL is not None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def docs_enabled(self) -> bool:
        return self.DOCS_URL is not None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def calendar_enabled(self) -> bool:
        return self.CALENDAR_URL is not None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def task_enabled(self) -> bool:
        return self.TASK_URL is not None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def drive_enabled(self) -> bool:
        return self.DRIVE_URL is not None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def meet_enabled(self) -> bool:
        return self.MEET_URL is not None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def ai_enabled(self) -> bool:
        return self.AI_BASE_URL is not None and self.AI_MODEL is not None and self.AI_API_KEY is not None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def grist_enabled(self) -> bool:
        return self.GRIST_BASE_URL is not None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def oidc_discovery_endpoint(self) -> str:
        if self.OIDC_ISSUER:
            return f"{self.OIDC_ISSUER.rstrip('/')}/.well-known/openid-configuration"
        return ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        if isinstance(self.CORS_ALLOW_ORIGINS, str):
            return [self.CORS_ALLOW_ORIGINS]
        return [str(origin).rstrip("/") for origin in self.CORS_ALLOW_ORIGINS]


settings = Settings()  # type: ignore[reportCallIssue]
