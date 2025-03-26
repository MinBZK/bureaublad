import secrets
from typing import Literal

from jose.constants import ALGORITHMS
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=("dev.env", ".env", "prod.env"), extra="ignore")
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    DEBUG: bool = False

    ENVIRONMENT: Literal["dev", "prod"] = "prod"

    OIDC_CLIENT_ID: str = "bureaublad-frontend"
    OIDC_CLIENT_SECRET: str | None = None
    OIDC_AUTHORIZATION_ENDPOINT: str = (
        "https://id.la-suite.apps.digilab.network/realms/lasuite/protocol/openid-connect/auth"
    )
    OIDC_TOKEN_ENDPOINT: str = "https://id.la-suite.apps.digilab.network/realms/lasuite/protocol/openid-connect/token"  # noqa: S105
    OIDC_JWKS_ENDPOINT: str = "https://id.la-suite.apps.digilab.network/realms/lasuite/protocol/openid-connect/certs"
    OIDC_SCOPES: dict[str, str] = {"openid": "", "profile": "", "email": ""}
    OIDC_AUDIENCE: str = "account"
    OIDC_ISSUER: str = "https://id.la-suite.apps.digilab.network/realms/lasuite"
    OIDC_SIGNATURE_ALGORITM: str | list[str] = [ALGORITHMS.RS256, ALGORITHMS.HS256]

    OCS_URL: str = "https://files.la-suite.apps.digilab.network"
    OCS_AUDIENCE: str = "files"
    DOCS_URL: str = "https://docs.la-suite.apps.digilab.network"
    DOCS_AUDIENCE: str = "docs"
    CALENDAR_URL: str = "https://files.la-suite.apps.digilab.network"
    CALENDAR_AUDIENCE: str = "files"
    TASK_URL: str = "https://files.la-suite.apps.digilab.network"
    TASK_AUDIENCE: str = "files"
    AI_BASE_URL: str = "https://api.openai.com/v1/"
    AI_MODEL: str = "gpt-4o"
    AI_API_KEY: str | None = None

    CORS_ALLOW_ORIGINS: str | list[str] = "*"
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]


settings = Settings()  # type: ignore[reportCallIssue]
