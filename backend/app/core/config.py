import json
import secrets
from typing import Annotated, Any, Literal, cast

from jose.constants import ALGORITHMS
from pydantic import AnyUrl, BeforeValidator, HttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.types import LoggingLevelType


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

    required = {"id", "icon", "url", "title"}
    if not required.issubset(link.keys()):  # pyright: ignore[reportUnknownArgumentType]
        raise ValueError(f"Link at index {idx} missing fields: {required - link.keys()}")

    try:
        HttpUrl(link["url"])  # pyright: ignore[reportUnknownArgumentType]
    except Exception as e:
        raise ValueError(f"Link at index {idx} has invalid URL: {e}") from e


def parse_sidebar_links(v: Any) -> list[dict[str, str | bool]]:  # noqa: ANN401
    # Parse input into a list
    if isinstance(v, list):
        parsed = v  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
    elif isinstance(v, str):
        if not v.strip():
            return []
        try:
            parsed = json.loads(v)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in SIDEBAR_LINKS_JSON: {e}") from e
    else:
        raise TypeError(f"SIDEBAR_LINKS_JSON must be string or list, got {type(v)}")

    if not isinstance(parsed, list):
        raise TypeError("SIDEBAR_LINKS_JSON must be a JSON array")

    # Validate all entries (runs for both string and list inputs)
    for idx, link in enumerate(parsed):  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
        _validate_sidebar_link(link, idx)

    return cast(list[dict[str, str | bool]], parsed)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = False
    ENVIRONMENT: Literal["dev", "test", "prod"] = "prod"

    # Session configuration
    SESSION_MAX_AGE: int = 1 * 60 * 60  # 1 hours (should be >= refresh token lifetime)

    LOGGING_LEVEL: LoggingLevelType = "INFO"
    LOGGING_CONFIG: dict[str, Any] | None = None

    # OpenID Connect
    OIDC_CLIENT_ID: str = "bureaublad"
    OIDC_CLIENT_SECRET: str | None = None
    OIDC_AUTHORIZATION_ENDPOINT: str = ""
    OIDC_LOGOUT_ENDPOINT: str = ""
    OIDC_POST_LOGOUT_REDIRECT_URI: str | None = None
    OIDC_POST_LOGIN_REDIRECT_URI: str = "/"
    OIDC_TOKEN_ENDPOINT: str = ""
    OIDC_REVOCATION_ENDPOINT: str | None = None  # RFC 7009 token revocation
    OIDC_JWKS_ENDPOINT: str = ""
    OIDC_USERNAME_CLAIM: str = "preferred_username"
    OIDC_NAME_CLAIM: str = "name"
    OIDC_EMAIL_CLAIM: str = "email"
    OIDC_SCOPES: str = "openid profile email"
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
    CONVERSATION_URL: str | None = None
    CONVERSATION_AUDIENCE: str = "conversation"

    # AI Integration
    AI_BASE_URL: str | None = "https://api.openai.com/v1/"
    AI_MODEL: str | None = "gpt-4o"
    AI_API_KEY: str | None = None

    THEME_CSS_URL: str = ""

    SIDEBAR_LINKS_JSON: Annotated[list[dict[str, str | bool]], BeforeValidator(parse_sidebar_links)] = []

    CORS_ALLOW_ORIGINS: Annotated[list[AnyUrl], BeforeValidator(parse_string_or_list)] = []
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    TRUSTED_HOSTS: Annotated[list[str], BeforeValidator(parse_string_or_list)] = ["*"]

    @computed_field
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "dev"

    @computed_field
    @property
    def is_testing(self) -> bool:
        """Check if running in test environment."""
        return self.ENVIRONMENT == "test"

    @computed_field
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "prod"

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(**kwargs)
        self._apply_environment_defaults()

    def _apply_environment_defaults(self) -> None:
        """Apply environment-specific default values after initialization."""
        if self.ENVIRONMENT == "test":
            # Test environment defaults - always include testserver for test client
            if "testserver" not in self.TRUSTED_HOSTS:
                self.TRUSTED_HOSTS = ["testserver", *self.TRUSTED_HOSTS]  # pyright: ignore[reportConstantRedefinition]

            # Override DEBUG for tests unless explicitly set
            if not hasattr(self, "_debug_set"):
                self.DEBUG = True  # pyright: ignore[reportConstantRedefinition]

            # Use a more verbose logging level for tests
            if self.LOGGING_LEVEL == "INFO":
                self.LOGGING_LEVEL = "DEBUG"  # pyright: ignore[reportConstantRedefinition]

        elif self.ENVIRONMENT == "dev":
            # Development environment defaults
            if not hasattr(self, "_debug_set"):
                self.DEBUG = True  # pyright: ignore[reportConstantRedefinition]

        elif self.ENVIRONMENT == "prod":
            # Production environment defaults - ensure security
            if not hasattr(self, "_debug_set"):
                self.DEBUG = False  # pyright: ignore[reportConstantRedefinition]

    @classmethod
    def for_testing(cls, **overrides: Any) -> "Settings":  # noqa: ANN401
        """Create settings instance specifically for testing with safe defaults."""
        test_defaults = {
            "ENVIRONMENT": "test",
            "DEBUG": True,
            "TRUSTED_HOSTS": ["testserver", "localhost", "127.0.0.1"],
            "LOGGING_LEVEL": "DEBUG",
            "SECRET_KEY": "test-secret-key-not-for-production",
            **overrides,
        }
        return cls(**test_defaults)

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
    def conversation_enabled(self) -> bool:
        return self.CONVERSATION_URL is not None

    @computed_field
    @property
    def ai_enabled(self) -> bool:
        return self.AI_BASE_URL is not None and self.AI_MODEL is not None and self.AI_API_KEY is not None

    @computed_field
    @property
    def grist_enabled(self) -> bool:
        return self.GRIST_URL is not None

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
