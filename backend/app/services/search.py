"""Global document search via La Suite Find.

Find authenticates users with a token exchanged with Menshen, La Suite's
OAuth 2.0 Token Exchange server (RFC 8693): the user's access token is
exchanged for a token targeting Find, with an action scope that Menshen
replaces by the granted `find:<service>:search` scopes.
"""

import logging
from typing import Any

import httpx

from app.core.config import settings
from app.core.translate import _
from app.models.search import SearchResult

logger = logging.getLogger(__name__)

FIND_SEARCH_PATH = "/api/v1.0/documents/search/"
MENSHEN_EXCHANGE_PATH = "/auth/token/exchange/"
TOKEN_EXCHANGE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:token-exchange"  # noqa: S105
ACCESS_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:access_token"  # noqa: S105

DEFAULT_NB_RESULTS = 20


class SearchUnavailableError(Exception):
    """The search service could not fulfill the request."""


async def exchange_token_for_find(client: httpx.AsyncClient, subject_token: str) -> str:
    """Exchange the user's access token with Menshen for a Find-scoped token."""
    assert settings.MENSHEN_URL  # noqa: S101 - callers check settings.search_enabled first
    response = await client.post(
        f"{settings.MENSHEN_URL.rstrip('/')}{MENSHEN_EXCHANGE_PATH}",
        auth=(settings.MENSHEN_CLIENT_ID, settings.MENSHEN_CLIENT_SECRET or ""),
        data={
            "grant_type": TOKEN_EXCHANGE_GRANT_TYPE,
            "subject_token": subject_token,
            "subject_token_type": ACCESS_TOKEN_TYPE,
            "audience": settings.FIND_AUDIENCE,
            "scope": settings.FIND_SEARCH_SCOPE,
        },
    )
    if response.status_code != 200:
        logger.warning("Menshen token exchange failed: %s %s", response.status_code, response.text[:200])
        raise SearchUnavailableError(_("Token exchange with the search service failed"))
    data: dict[str, Any] = response.json()
    token = data.get("access_token")
    if not isinstance(token, str):
        raise SearchUnavailableError(_("Token exchange with the search service returned no token"))
    return token


async def search_documents(client: httpx.AsyncClient, find_token: str, query: str) -> list[SearchResult]:
    """Search Find for documents the user may access."""
    assert settings.FIND_URL  # noqa: S101 - callers check settings.search_enabled first
    response = await client.post(
        f"{settings.FIND_URL.rstrip('/')}{FIND_SEARCH_PATH}",
        headers={"Authorization": f"Bearer {find_token}"},
        json={"q": query, "nb_results": DEFAULT_NB_RESULTS},
    )
    if response.status_code != 200:
        logger.warning("Find search failed: %s %s", response.status_code, response.text[:200])
        raise SearchUnavailableError(_("The search service returned an error"))

    results: list[SearchResult] = []
    for hit in response.json().get("results", []):
        results.append(
            SearchResult(
                id=hit["id"],
                service=hit["service"],
                title=hit["title"],
                path=hit.get("path", ""),
                updated_at=hit["updated_at"],
                url=settings.find_document_url(hit["service"], hit["id"]),
            )
        )
    return results
