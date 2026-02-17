import secrets
from typing import Annotated, Any, Literal, cast

from jose.constants import ALGORITHMS
from pydantic import AnyUrl, BeforeValidator, RedisDsn, computed_field
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
    SESSION_MAX_AGE: int = 24 * 60 * 60 * 7  # 7 days (should be >= refresh token lifetime)

    LOGGING_LEVEL: LoggingLevelType = "INFO"
    LOGGING_CONFIG: dict[str, Any] | None = None

    # Redis
    REDIS_URL: RedisDsn = RedisDsn("redis://redis:6379")

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
    OCS_AUDIENCE: str = "nextcloud"
    OCS_ICON: str = "folder"
    OCS_TITLE: str = "NextCloud"
    OCS_IFRAME: bool = False
    OCS_CARD: bool = True

    DOCS_URL: str | None = None
    DOCS_AUDIENCE: str = "docs"
    DOCS_ICON: str = "description"
    DOCS_TITLE: str = "Docs"
    DOCS_IFRAME: bool = False
    DOCS_CARD: bool = True

    CALENDAR_URL: str | None = None
    CALENDAR_AUDIENCE: str = "openxchange"
    CALENDAR_ICON: str = "calendar_today"
    CALENDAR_TITLE: str = "Calendar"
    CALENDAR_IFRAME: bool = False
    CALENDAR_CARD: bool = False

    TASK_URL: str | None = None
    TASK_AUDIENCE: str = "openxchange"
    TASK_ICON: str = "check_circle"
    TASK_TITLE: str = "Tasks"
    TASK_IFRAME: bool = False
    TASK_CARD: bool = False

    DRIVE_URL: str | None = None
    DRIVE_AUDIENCE: str = "drive"
    DRIVE_ICON: str = "cloud_drive"
    DRIVE_TITLE: str = "Drive"
    DRIVE_IFRAME: bool = False
    DRIVE_CARD: bool = True

    MEET_URL: str | None = None
    MEET_AUDIENCE: str = "meet"
    MEET_ICON: str = "video_call"
    MEET_TITLE: str = "Meet"
    MEET_IFRAME: bool = False
    MEET_CARD: bool = True

    GRIST_URL: str | None = None
    GRIST_AUDIENCE: str = "grist"
    GRIST_ICON: str = "table_chart"
    GRIST_TITLE: str = "Grist"
    GRIST_IFRAME: bool = False
    GRIST_CARD: bool = False

    CONVERSATION_URL: str | None = None
    CONVERSATION_AUDIENCE: str = "conversation"
    CONVERSATION_ICON: str = "chat"
    CONVERSATION_TITLE: str = "Conversation"
    CONVERSATION_IFRAME: bool = False
    CONVERSATION_CARD: bool = True

    MATRIX_URL: str | None = None
    MATRIX_AUDIENCE: str = "matrix"
    MATRIX_ICON: str = "forum"
    MATRIX_TITLE: str = "Matrix"
    MATRIX_IFRAME: bool = False
    MATRIX_CARD: bool = False

    # AI Integration
    AI_URL: str | None = "https://api.openai.com/v1/"
    AI_ICON: str = "smart_toy"
    AI_CARD: bool = True
    AI_MODEL: str | None = "gpt-4o"
    AI_API_KEY: str | None = None

    THEME_CSS_URL: str = ""
    HELPDESK_URL: str = ""
    REDIRECT_TO_ACCOUNT_PAGE: str = ""

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
        return self.AI_URL is not None and self.AI_MODEL is not None and self.AI_API_KEY is not None

    @computed_field
    @property
    def grist_enabled(self) -> bool:
        return self.GRIST_URL is not None

    @computed_field
    @property
    def matrix_enabled(self) -> bool:
        return self.MATRIX_URL is not None

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
