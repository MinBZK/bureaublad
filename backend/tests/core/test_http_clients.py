"""Tests for StatelessTransport cookie isolation."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from app.core.http_clients import StatelessTransport


def _make_response(headers: list[tuple[str, str]], status_code: int = 200) -> httpx.Response:
    """Build a minimal httpx.Response with the given headers."""
    return httpx.Response(status_code=status_code, headers=headers)


class TestStatelessTransport:
    @pytest.mark.asyncio
    async def test_strips_single_set_cookie_header(self) -> None:
        """Set-Cookie from a response is removed before being returned."""
        inner = AsyncMock()
        inner.handle_async_request = AsyncMock(return_value=_make_response([("set-cookie", "session=abc; Path=/")]))

        transport = StatelessTransport(inner)
        response = await transport.handle_async_request(MagicMock())

        assert "set-cookie" not in response.headers

    @pytest.mark.asyncio
    async def test_strips_multiple_set_cookie_headers(self) -> None:
        """All Set-Cookie headers (e.g. Nextcloud sends 9) are removed."""
        inner = AsyncMock()
        inner.handle_async_request = AsyncMock(
            return_value=_make_response(
                [
                    ("set-cookie", "nc_session_id=abc; Path=/"),
                    ("set-cookie", "oc_sessionPassphrase=xyz; Path=/"),
                    ("set-cookie", "__Host-nc_sameSiteCookielax=true; SameSite=Lax"),
                ]
            )
        )

        transport = StatelessTransport(inner)
        response = await transport.handle_async_request(MagicMock())

        assert "set-cookie" not in response.headers

    @pytest.mark.asyncio
    async def test_preserves_other_headers(self) -> None:
        """Non-cookie headers pass through unaffected."""
        inner = AsyncMock()
        inner.handle_async_request = AsyncMock(
            return_value=_make_response(
                [
                    ("content-type", "application/json"),
                    ("set-cookie", "session=abc"),
                    ("x-request-id", "req-123"),
                ]
            )
        )

        transport = StatelessTransport(inner)
        response = await transport.handle_async_request(MagicMock())

        assert response.headers["content-type"] == "application/json"
        assert response.headers["x-request-id"] == "req-123"
        assert "set-cookie" not in response.headers

    @pytest.mark.asyncio
    async def test_response_with_no_cookies_unchanged(self) -> None:
        """Responses without Set-Cookie headers are returned as-is."""
        inner = AsyncMock()
        inner.handle_async_request = AsyncMock(return_value=_make_response([("content-type", "application/json")]))

        transport = StatelessTransport(inner)
        response = await transport.handle_async_request(MagicMock())

        assert response.headers["content-type"] == "application/json"

    @pytest.mark.asyncio
    async def test_cookies_do_not_accumulate_in_shared_client(self) -> None:
        """Verify the shared AsyncClient cookie jar stays empty after responses with Set-Cookie."""
        inner = AsyncMock()
        inner.handle_async_request = AsyncMock(
            return_value=_make_response([("set-cookie", "user_session=user_a_token; Path=/")])
        )

        transport = StatelessTransport(inner)
        client = httpx.AsyncClient(transport=transport)

        # Simulate a request — httpx will try to persist any Set-Cookie it sees
        request = httpx.Request("GET", "https://nextcloud.example.com/ocs/activities")
        await transport.handle_async_request(request)

        assert len(dict(client.cookies)) == 0
