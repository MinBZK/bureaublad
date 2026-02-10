from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.responses import RedirectResponse
from fastapi.testclient import TestClient


class TestAuthLogin:
    """Tests for /auth/login endpoint."""

    @patch("app.routes.authentication.oauth.oidc.authorize_redirect")
    def test_login_redirect_without_redirect_to(self, mock_redirect: MagicMock, client: TestClient) -> None:
        """Test login endpoint returns OAuth redirect without redirect_to parameter."""
        mock_redirect.return_value = RedirectResponse(url="https://auth.example.com/authorize")

        response = client.get("/api/v1/auth/login", follow_redirects=False)

        assert response.status_code == 307  # Temporary redirect
        mock_redirect.assert_called_once()

    @patch("app.routes.authentication.oauth.oidc.authorize_redirect")
    def test_login_redirect_with_valid_redirect_to(self, mock_redirect: MagicMock, client: TestClient) -> None:
        """Test login endpoint with valid redirect_to parameter."""
        mock_redirect.return_value = RedirectResponse(url="https://auth.example.com/authorize")

        response = client.get("/api/v1/auth/login?redirect_to=/dashboard", follow_redirects=False)

        assert response.status_code == 307
        mock_redirect.assert_called_once()

    def test_login_redirect_with_invalid_redirect_to(self, client: TestClient) -> None:
        """Test login endpoint rejects invalid redirect_to parameter."""
        response = client.get("/api/v1/auth/login?redirect_to=javascript:alert(1)", follow_redirects=False)

        assert response.status_code == 401  # CredentialError returns 401


class TestAuthCallback:
    """Tests for /auth/callback endpoint."""

    @patch("app.routes.authentication.oauth.oidc.authorize_access_token")
    def test_callback_failure(self, mock_token_exchange: AsyncMock, client: TestClient) -> None:
        """Test OAuth callback failure handling."""
        mock_token_exchange.side_effect = Exception("OAuth error")

        response = client.get("/api/v1/auth/callback?code=invalid&state=test-state", follow_redirects=False)

        assert response.status_code == 302
        assert "/login?error=authentication_failed" in response.headers["location"]


class TestAuthProfile:
    """Tests for /auth/profile endpoint."""

    def test_profile_unauthenticated(self, fresh_client: TestClient) -> None:
        """Test profile endpoint when not authenticated."""
        response = fresh_client.get("/api/v1/auth/profile")

        assert response.status_code == 401  # CredentialError returns 401

    def test_profile_authenticated(self, authenticated_client: TestClient) -> None:
        """Test profile endpoint when authenticated."""
        response = authenticated_client.get("/api/v1/auth/profile")

        assert response.status_code == 200

        data = response.json()
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"


class TestAuthLogout:
    """Tests for /auth/logout endpoint."""

    @patch("app.routes.authentication._build_logout_url")
    def test_logout_without_session(self, mock_build_url: MagicMock, client: TestClient) -> None:
        """Test logout when no session exists."""
        mock_build_url.return_value = "https://auth.example.com/logout"

        response = client.get("/api/v1/auth/logout", follow_redirects=False)

        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "https://auth.example.com/logout"

    @patch("app.routes.authentication.oauth.oidc._get_oauth_client")
    @patch("app.routes.authentication._build_logout_url")
    @patch("app.core.config.settings.OIDC_REVOCATION_ENDPOINT", "https://auth.example.com/revoke")
    def test_logout_with_session_and_token_revocation(
        self, mock_build_url: MagicMock, mock_get_client: MagicMock, authenticated_client: TestClient
    ) -> None:
        """Test logout with session and successful token revocation."""
        mock_oauth_client = AsyncMock()
        mock_get_client.return_value.__aenter__.return_value = mock_oauth_client
        mock_build_url.return_value = "https://auth.example.com/logout"

        response = authenticated_client.get("/api/v1/auth/logout", follow_redirects=False)

        assert response.status_code == 307
        assert response.headers["location"] == "https://auth.example.com/logout"


class TestSafeRedirectValidation:
    """Tests for redirect URL validation."""

    @patch("app.routes.authentication.oauth.oidc.authorize_redirect")
    def test_valid_redirect_urls_accepted(self, mock_redirect: MagicMock, client: TestClient) -> None:
        """Test that valid redirect URLs are accepted."""
        mock_redirect.return_value = RedirectResponse(url="https://auth.example.com/authorize")

        valid_urls = ["/dashboard", "/api/v1/config", "https://example.com/callback"]

        for url in valid_urls:
            response = client.get(f"/api/v1/auth/login?redirect_to={url}", follow_redirects=False)
            assert response.status_code == 307, f"Valid URL {url} was rejected"

    def test_invalid_redirect_urls_rejected(self, client: TestClient) -> None:
        """Test that invalid redirect URLs are rejected."""
        # Mock the OAuth client to prevent configuration errors
        with patch("app.routes.authentication.oauth.oidc.authorize_redirect") as mock_oauth:
            mock_oauth.return_value = RedirectResponse(url="http://mocked-oauth-url")

            invalid_urls = [
                "javascript:alert(1)",
                "//evil.com/redirect",
                "http://insecure.com",  # HTTP not allowed
            ]

            for url in invalid_urls:
                response = client.get(f"/api/v1/auth/login?redirect_to={url}", follow_redirects=False)
                assert response.status_code == 401, f"Invalid URL {url} was not rejected"
                # OAuth should not be called for invalid URLs
                mock_oauth.assert_not_called()

            # Test empty string separately - currently treated as no redirect_to parameter
            response = client.get("/api/v1/auth/login?redirect_to=", follow_redirects=False)
            # Empty string is treated as falsy, so it uses default redirect behavior
            assert response.status_code == 307, "Empty redirect_to is treated as no redirect_to parameter"
            mock_oauth.assert_called_once()  # OAuth should be called for this case
