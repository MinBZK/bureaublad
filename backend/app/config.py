import secrets
from typing import Literal

from jose.constants import ALGORITHMS
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, extra="ignore")
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    DEBUG: bool = False

    VERSION: str = "0.1.0"

    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    OIDC_CLIENT_ID: str = "bureaublad"
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

    NEXTCLOUD_URL: str = "https://files.la-suite.apps.digilab.network"
    DOCS_URL: str = "https://docs.la-suite.apps.digilab.network"
    MATRIX_URL: str = "https://matrix.chat.la-suite.apps.digilab.network"


settings = Settings()
