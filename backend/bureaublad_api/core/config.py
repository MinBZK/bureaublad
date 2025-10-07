import json
import secrets
from typing import Annotated, Any, Literal, cast

from jose.constants import ALGORITHMS
from pydantic import AnyUrl, BeforeValidator, HttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from bureaublad_api.types import LoggingLevelType


def parse_string_or_list(v: Any) -> list[str]:  # noqa: ANN401
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    if isinstance(v, list):
        for idx, item in enumerate(v):  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
            if not isinstance(item, str):
                raise TypeError(f"List item at index {idx} must be string, got {type(item)}")  # pyright: ignore[reportUnknownArgumentType]
        return cast(list[str], v)
    raise ValueError(f"Must be string or list, got {type(v)}")


def _validate_sidebar_link(link: Any, idx: int) -> None:  # noqa: ANN401
    """Validate that a single sidebar link has correct structure and valid URL."""
    if not isinstance(link, dict):
        raise TypeError(f"Link at index {idx} must be an object")

    required = {"icon", "url", "title"}
    if not required.issubset(link.keys()):  # pyright: ignore[reportUnknownArgumentType]
        raise ValueError(f"Link at index {idx} missing fields: {required - link.keys()}")

    try:
        HttpUrl(link["url"])  # pyright: ignore[reportUnknownArgumentType]
    except Exception as e:
        raise ValueError(f"Link at index {idx} has invalid URL: {e}") from e


def parse_sidebar_links(v: Any) -> list[dict[str, str]]:  # noqa: ANN401
<<<<<<< HEAD:backend/app/config.py
    if isinstance(v, str):
        if not v.strip():
            return []
        try:
            parsed: Any = json.loads(v)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in SIDEBAR_LINKS_JSON: {e}") from e

        if not isinstance(parsed, list):
            raise TypeError("SIDEBAR_LINKS_JSON must be a JSON array")

        for idx, link in enumerate(parsed):  # type: ignore[misc]
            if not isinstance(link, dict):
                raise TypeError(f"Link at index {idx} must be an object")
            required = {"icon", "url", "title"}
            if not required.issubset(link.keys()):  # type: ignore[arg-type]
                raise ValueError(f"Link at index {idx} missing fields: {required - link.keys()}")

            # Validate URL is valid http/https
            try:
                HttpUrl(link["url"])  # type: ignore[arg-type]
            except Exception as e:
                raise ValueError(f"Link at index {idx} has invalid URL: {e}") from e

        return parsed  # type: ignore[return-value]

=======
>>>>>>> d47f213 (🎨(structure) restructure backend code):backend/bureaublad_api/core/config.py
    if isinstance(v, list):
        return cast(list[dict[str, str]], v)

    if not isinstance(v, str):
        raise TypeError(f"SIDEBAR_LINKS_JSON must be string or list, got {type(v)}")

    if not v.strip():
        return []

    try:
        parsed: Any = json.loads(v)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in SIDEBAR_LINKS_JSON: {e}") from e

    if not isinstance(parsed, list):
        raise TypeError("SIDEBAR_LINKS_JSON must be a JSON array")

    for idx, link in enumerate(parsed):  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
        _validate_sidebar_link(link, idx)

    return cast(list[dict[str, str]], parsed)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = False
    ENVIRONMENT: Literal["dev", "prod"] = "prod"

    LOGGING_LEVEL: LoggingLevelType = "INFO"
    LOGGING_CONFIG: dict[str, Any] | None = None

    # OpenID Connect
    OIDC_CLIENT_ID: str = "bureaublad"
    OIDC_CLIENT_SECRET: str | None = None
    OIDC_AUTHORIZATION_ENDPOINT: str = ""
    OIDC_TOKEN_ENDPOINT: str = ""
    OIDC_PUBLIC_TOKEN_ENDPOINT: str | None = None
    OIDC_JWKS_ENDPOINT: str = ""
    OIDC_USERNAME_CLAIM: str = "preferred_username"
    OIDC_SCOPES: dict[str, str] = {"openid": "", "profile": "", "email": ""}
    OIDC_AUDIENCE: str = "bureaublad"
    OIDC_ISSUER: str = ""
    OIDC_SIGNATURE_ALGORITM: str | list[str] = [ALGORITHMS.RS256, ALGORITHMS.HS256]

    # La Suite Services
    OCS_URL: str | None = None
    OCS_AUDIENCE: str = "files"
    DOCS_URL: str | None = None
    DOCS_AUDIENCE: str = "docs"
    CALENDAR_URL: str | None = None
    CALENDAR_AUDIENCE: str = "openxchange"
    TASK_URL: str | None = None
    TASK_AUDIENCE: str = "openxchange"
    DRIVE_URL: str | None = None
    DRIVE_AUDIENCE: str = "drive"
    MEET_URL: str | None = None
    MEET_AUDIENCE: str = "meet"
    GRIST_URL: str | None = None
    GRIST_AUDIENCE: str = "grist"

    # AI Integration
    AI_BASE_URL: str | None = "https://api.openai.com/v1/"
    AI_MODEL: str | None = "gpt-4o"
    AI_API_KEY: str | None = None

    THEME_CSS_URL: str = ""

    SIDEBAR_LINKS_JSON: Annotated[list[dict[str, str]], BeforeValidator(parse_sidebar_links)] = []

    CORS_ALLOW_ORIGINS: Annotated[list[AnyUrl], BeforeValidator(parse_string_or_list)] = []
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    TRUSTED_HOSTS: Annotated[list[str], BeforeValidator(parse_string_or_list)] = ["*"]

    @computed_field
    @property
    def ocs_enabled(self) -> bool:
        return self.OCS_URL is not None

    @computed_field
    @property
    def docs_enabled(self) -> bool:
        return self.DOCS_URL is not None

    @computed_field
    @property
    def calendar_enabled(self) -> bool:
        return self.CALENDAR_URL is not None

    @computed_field
    @property
    def task_enabled(self) -> bool:
        return self.TASK_URL is not None

    @computed_field
    @property
    def drive_enabled(self) -> bool:
        return self.DRIVE_URL is not None

    @computed_field
    @property
    def meet_enabled(self) -> bool:
        return self.MEET_URL is not None

    @computed_field
    @property
    def ai_enabled(self) -> bool:
        return self.AI_BASE_URL is not None and self.AI_MODEL is not None and self.AI_API_KEY is not None

    @computed_field
    @property
    def grist_enabled(self) -> bool:
        return self.GRIST_URL is not None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def parsed_oidc_public_token_endpoint(self) -> str:
        return self.OIDC_PUBLIC_TOKEN_ENDPOINT or self.OIDC_TOKEN_ENDPOINT

    @computed_field
    @property
    def oidc_discovery_endpoint(self) -> str:
        if self.OIDC_ISSUER:
            return f"{self.OIDC_ISSUER.rstrip('/')}/.well-known/openid-configuration"
        return ""

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.CORS_ALLOW_ORIGINS]


settings = Settings()
