"""Tests for the core authentication module."""

import asyncio
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.core.authentication import (
    _needs_refresh,
    _refresh_token,
    get_current_user,
    oauth2_scheme,
)
from app.exceptions import CredentialError
from app.models.user import AuthState, User
from fastapi import Request


class TestOAuth2Scheme:
    """Test cases for OAuth2 scheme configuration."""

    def test_oauth2_scheme_configuration(self) -> None:
        """Test OAuth2 scheme is properly configured."""
        assert oauth2_scheme.auto_error is False
        # Note: authorizationUrl and tokenUrl are set during initialization
        # but may not be accessible as direct attributes in all versions


class TestNeedsRefresh:
    """Test cases for the _needs_refresh function."""

    def test_needs_refresh_no_expires_at(self) -> None:
        """Test that None expires_at returns False."""
        assert _needs_refresh(None) is False

    def test_needs_refresh_token_expired(self) -> None:
        """Test that expired token needs refresh."""
        expired_time = int(time.time()) - 3600  # 1 hour ago
        assert _needs_refresh(expired_time) is True

    def test_needs_refresh_token_expiring_soon(self) -> None:
        """Test that token expiring within 60s needs refresh."""
        expiring_time = int(time.time()) + 30  # 30 seconds from now
        assert _needs_refresh(expiring_time) is True

    def test_needs_refresh_token_valid(self) -> None:
        """Test that valid token with time remaining doesn't need refresh."""
        valid_time = int(time.time()) + 3600  # 1 hour from now
        assert _needs_refresh(valid_time) is False

    def test_needs_refresh_boundary_condition(self) -> None:
        """Test boundary condition at exactly 60 seconds."""
        boundary_time = int(time.time()) + 60  # Exactly 60 seconds
        assert _needs_refresh(boundary_time) is True


class TestRefreshToken:
    """Test cases for the _refresh_token function."""

    @pytest.fixture
    def mock_request(self) -> Request:
        """Create a mock request object."""
        request = MagicMock(spec=Request)
        request.session = {}
        request.state = MagicMock()
        return request

    @pytest.mark.asyncio
    async def test_refresh_no_refresh_token(self, mock_request: Request) -> None:
        """Test refresh fails when no refresh token is provided."""
        with pytest.raises(CredentialError) as exc_info:
            await _refresh_token(mock_request, None)

        assert "Session expired. Please log in again." in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_refresh_empty_refresh_token(self, mock_request: Request) -> None:
        """Test refresh fails when empty refresh token is provided."""
        with pytest.raises(CredentialError) as exc_info:
            await _refresh_token(mock_request, "")

        assert "Session expired. Please log in again." in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication.oauth")
    async def test_refresh_success(self, mock_oauth: MagicMock, mock_session: AsyncMock, mock_request: Request) -> None:
        """Test successful token refresh."""
        # Mock successful token response
        new_token = {
            "access_token": "new_access_token",
            "expires_at": int(time.time()) + 3600,
            "refresh_token": "new_refresh_token",
        }
        mock_oauth.oidc.fetch_access_token = AsyncMock(return_value=new_token)
        mock_session.update_tokens = AsyncMock()

        await _refresh_token(mock_request, "old_refresh_token")

        # Verify OAuth call
        mock_oauth.oidc.fetch_access_token.assert_called_once_with(
            grant_type="refresh_token", refresh_token="old_refresh_token"
        )

        # Verify session was updated
        mock_session.update_tokens.assert_called_once_with(
            mock_request,
            access_token="new_access_token",
            expires_at=new_token["expires_at"],
            refresh_token="new_refresh_token",
        )

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication.oauth")
    async def test_refresh_success_no_new_refresh_token(
        self, mock_oauth: MagicMock, mock_session: MagicMock, mock_request: Request
    ) -> None:
        """Test successful token refresh without new refresh token."""
        # Mock token response without refresh_token
        new_token = {
            "access_token": "new_access_token",
            "expires_at": int(time.time()) + 3600,
        }
        mock_oauth.oidc.fetch_access_token = AsyncMock(return_value=new_token)
        mock_session.update_tokens = AsyncMock()

        await _refresh_token(mock_request, "old_refresh_token")

        # Verify session was updated with None for refresh_token
        mock_session.update_tokens.assert_called_once_with(
            mock_request,
            access_token="new_access_token",
            expires_at=new_token["expires_at"],
            refresh_token=None,
        )

    @pytest.mark.asyncio
    @patch("app.core.authentication.oauth")
    async def test_refresh_oauth_failure(self, mock_oauth: MagicMock, mock_request: Request) -> None:
        """Test token refresh failure due to OAuth error."""
        mock_oauth.oidc.fetch_access_token = AsyncMock(side_effect=Exception("OAuth error"))

        with pytest.raises(CredentialError) as exc_info:
            await _refresh_token(mock_request, "refresh_token")

        assert "Session expired" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch("app.core.authentication.oauth")
    @patch("app.core.authentication.session")
    async def test_refresh_token_reuse_conflict(
        self, mock_session: MagicMock, mock_oauth: MagicMock, mock_request: Request
    ) -> None:
        """Test that token reuse errors raise TokenRefreshConflictError (409), not CredentialError."""
        from app.exceptions import TokenRefreshConflictError

        # Simulate Keycloak's "reuse exceeded" error
        mock_oauth.oidc.fetch_access_token = AsyncMock(
            side_effect=Exception("invalid_grant: Maximum allowed refresh token reuse exceeded")
        )
        mock_session.clear_auth = AsyncMock()

        with pytest.raises(TokenRefreshConflictError):
            await _refresh_token(mock_request, "refresh_token")

        # Session should NOT be cleared for reuse conflicts
        mock_session.clear_auth.assert_not_called()

    @pytest.mark.asyncio
    @patch("app.core.authentication.oauth")
    @patch("app.core.authentication.session")
    async def test_refresh_invalid_grant_non_reuse(
        self, mock_session: MagicMock, mock_oauth: MagicMock, mock_request: Request
    ) -> None:
        """Test that non-reuse invalid_grant errors clear session and raise CredentialError."""
        # Simulate a non-reuse invalid_grant error (corrupted session, expired token, etc.)
        mock_oauth.oidc.fetch_access_token = AsyncMock(
            side_effect=Exception("invalid_grant: Session doesn't have required client")
        )
        mock_session.clear_auth = AsyncMock()

        with pytest.raises(CredentialError) as exc_info:
            await _refresh_token(mock_request, "refresh_token")

        # Session SHOULD be cleared for non-reuse errors
        mock_session.clear_auth.assert_called_once_with(mock_request)
        assert "Session expired" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch("app.core.authentication.oauth")
    @patch("app.core.authentication.session")
    async def test_refresh_token_not_active(
        self, mock_session: MagicMock, mock_oauth: MagicMock, mock_request: Request
    ) -> None:
        """Test that 'token is not active' errors are logged at INFO level (expected expiration)."""
        # Simulate Keycloak's "token is not active" error (common on service restart)
        mock_oauth.oidc.fetch_access_token = AsyncMock(side_effect=Exception("invalid_grant: Token is not active"))
        mock_session.clear_auth = AsyncMock()

        with pytest.raises(CredentialError) as exc_info:
            await _refresh_token(mock_request, "refresh_token")

        # Session SHOULD be cleared for expired tokens
        mock_session.clear_auth.assert_called_once_with(mock_request)
        assert "Session expired" in str(exc_info.value.detail)


class TestGetCurrentUser:
    """Test cases for the get_current_user function."""

    @pytest.fixture
    def mock_request(self) -> Request:
        """Create a mock request object."""
        request = MagicMock(spec=Request)
        request.session = {"_session_id": "test_session_123"}
        request.state = MagicMock()
        return request

    @pytest.fixture
    def sample_user(self) -> User:
        """Create a sample user for testing."""
        return User(name="Test User", email="test@example.com")

    @pytest.fixture
    def valid_auth_state(self, sample_user: User) -> AuthState:
        """Create a valid auth state."""
        return AuthState(
            sub="user123",
            user=sample_user,
            access_token="valid_token",
            refresh_token="valid_refresh_token",
            expires_at=int(time.time()) + 3600,  # Valid for 1 hour
        )

    @pytest.fixture
    def expired_auth_state(self, sample_user: User) -> AuthState:
        """Create an expired auth state."""
        return AuthState(
            sub="user123",
            user=sample_user,
            access_token="expired_token",
            refresh_token="valid_refresh_token",
            expires_at=int(time.time()) - 100,  # Expired 100 seconds ago
        )

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    async def test_get_current_user_not_authenticated(self, mock_session: MagicMock, mock_request: Request) -> None:
        """Test get_current_user when not authenticated."""
        mock_session.get_auth = AsyncMock(return_value=None)

        with pytest.raises(CredentialError) as exc_info:
            await get_current_user(mock_request, None)

        assert "Not authenticated" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    async def test_get_current_user_valid_token(
        self, mock_session: MagicMock, mock_request: Request, valid_auth_state: AuthState
    ) -> None:
        """Test get_current_user with valid token that doesn't need refresh."""
        mock_session.get_auth = AsyncMock(return_value=valid_auth_state)
        mock_session.update_tokens = AsyncMock()

        result = await get_current_user(mock_request, None)

        assert result == valid_auth_state.user
        assert mock_request.state.user == valid_auth_state.user
        # Should not attempt refresh
        mock_session.update_tokens.assert_not_called()

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._refresh_token")
    async def test_get_current_user_token_refresh_needed(
        self,
        mock_refresh: AsyncMock,
        mock_session: MagicMock,
        mock_request: Request,
        expired_auth_state: AuthState,
        valid_auth_state: AuthState,
    ) -> None:
        """Test get_current_user when token refresh is needed."""
        # Configure the flow: initial auth, re-check after lock, auth after refresh
        mock_session.get_auth = AsyncMock(
            side_effect=[
                expired_auth_state,  # Initial check
                expired_auth_state,  # Re-check after acquiring lock
                valid_auth_state,  # After refresh
            ]
        )

        result = await get_current_user(mock_request, None)

        # Verify refresh was called
        mock_refresh.assert_called_once_with(mock_request, expired_auth_state.refresh_token)

        # Verify result
        assert result == valid_auth_state.user
        assert mock_request.state.user == valid_auth_state.user

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._refresh_token")
    async def test_get_current_user_session_lost_after_refresh(
        self,
        mock_refresh: AsyncMock,
        mock_session: MagicMock,
        mock_request: Request,
        expired_auth_state: AuthState,
    ) -> None:
        """Test get_current_user when session is lost after refresh."""
        # Configure flow: initial auth, session lost after refresh
        mock_session.get_auth = AsyncMock(
            side_effect=[
                expired_auth_state,  # Initial check
                None,  # Session lost after refresh
            ]
        )

        with pytest.raises(CredentialError) as exc_info:
            await get_current_user(mock_request, None)

        # Error gets caught and re-raised with generic message
        assert "Session expired. Please log in again." in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._refresh_token")
    async def test_get_current_user_concurrent_refresh_conflict(
        self,
        mock_refresh: AsyncMock,
        mock_session: MagicMock,
        mock_request: Request,
        expired_auth_state: AuthState,
        valid_auth_state: AuthState,
    ) -> None:
        """Test that concurrent refresh requests result in 409 for conflicting requests."""
        from app.exceptions import TokenRefreshConflictError
        from fastapi import HTTPException

        # First request succeeds, second gets conflict
        mock_refresh.side_effect = [
            None,  # First refresh succeeds
            TokenRefreshConflictError(),  # Second gets conflict (uses default detail message)
        ]

        # Both requests see expired token initially
        mock_session.get_auth = AsyncMock(
            side_effect=[
                expired_auth_state,  # Request 1: initial check
                valid_auth_state,  # Request 1: after refresh
                expired_auth_state,  # Request 2: initial check
            ]
        )

        # Start two concurrent requests
        task1 = asyncio.create_task(get_current_user(mock_request, None))
        task2 = asyncio.create_task(get_current_user(mock_request, None))

        results = await asyncio.gather(task1, task2, return_exceptions=True)

        # First should succeed
        assert results[0] == valid_auth_state.user

        # Second should get 409 conflict
        assert isinstance(results[1], HTTPException)
        assert results[1].status_code == 409
        assert "conflict" in results[1].detail.lower()

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._refresh_token")
    async def test_get_current_user_no_session_id(
        self,
        mock_refresh: AsyncMock,
        mock_session: MagicMock,
        expired_auth_state: AuthState,
        valid_auth_state: AuthState,
    ) -> None:
        """Test get_current_user when request has no session ID."""
        # Create request without session ID
        request = MagicMock(spec=Request)
        request.session = {}  # No _session_id
        request.state = MagicMock()

        mock_session.get_auth.side_effect = [
            expired_auth_state,  # Initial check
            expired_auth_state,  # Re-check after lock
            valid_auth_state,  # After refresh
        ]
        mock_session.get_auth = AsyncMock(side_effect=mock_session.get_auth.side_effect)

        result = await get_current_user(request, None)

        # Should still work
        assert result == valid_auth_state.user
        mock_refresh.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._refresh_token")
    async def test_get_current_user_refresh_not_needed(
        self,
        mock_refresh: AsyncMock,
        mock_session: MagicMock,
        mock_request: Request,
        valid_auth_state: AuthState,
    ) -> None:
        """Test that refresh is skipped if token is valid."""
        # Token is valid, no refresh needed
        mock_session.get_auth = AsyncMock(return_value=valid_auth_state)

        result = await get_current_user(mock_request, None)

        # Token is valid, so no refresh needed
        mock_refresh.assert_not_called()
        assert result == valid_auth_state.user

    @pytest.mark.parametrize(
        "should_refresh",
        [True, False],
    )
    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._needs_refresh")
    async def test_get_current_user_refresh_logic(
        self,
        mock_needs_refresh: MagicMock,
        mock_session: MagicMock,
        mock_request: Request,
        sample_user: User,
        should_refresh: bool,
    ) -> None:
        """Test refresh logic with different scenarios."""
        auth_state = AuthState(
            sub="user123",
            user=sample_user,
            access_token="token",
            refresh_token="refresh_token",
            expires_at=int(time.time()) + 3600,  # Valid token
        )

        mock_needs_refresh.return_value = should_refresh

        if should_refresh:
            # Mock refresh scenario
            valid_auth = AuthState(
                sub="user123",
                user=sample_user,
                access_token="new_token",
                refresh_token="new_refresh_token",
                expires_at=int(time.time()) + 3600,
            )
            mock_session.get_auth = AsyncMock(
                side_effect=[
                    auth_state,  # Initial check
                    auth_state,  # Re-check after lock
                    valid_auth,  # After refresh
                ]
            )

            with patch("app.core.authentication._refresh_token") as mock_refresh:
                result = await get_current_user(mock_request, None)

            mock_refresh.assert_called_once()
        else:
            # No refresh needed
            mock_session.get_auth = AsyncMock(return_value=auth_state)
            result = await get_current_user(mock_request, None)

        assert result == sample_user

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._refresh_token")
    async def test_concurrent_refresh_returns_409_for_conflicts(
        self,
        mock_refresh: AsyncMock,
        mock_session: MagicMock,
        mock_request: Request,
        expired_auth_state: AuthState,
        valid_auth_state: AuthState,
    ) -> None:
        """Test that concurrent refresh requests return 409 for conflicting refreshes.

        With the 409 pattern, we accept that concurrent refreshes may happen.
        The first succeeds, others get TokenRefreshConflictError which becomes 409.
        Frontend is expected to retry 409 responses.
        """
        from app.exceptions import TokenRefreshConflictError
        from fastapi import HTTPException

        # First refresh succeeds, others get conflict
        refresh_effects = [
            None,  # First succeeds
            TokenRefreshConflictError("Token already used"),  # Conflict
            TokenRefreshConflictError("Token already used"),  # Conflict
            TokenRefreshConflictError("Token already used"),  # Conflict
            TokenRefreshConflictError("Token already used"),  # Conflict
        ]
        mock_refresh.side_effect = refresh_effects

        # All requests see expired token initially
        get_auth_effects = []
        for i in range(5):
            get_auth_effects.append(expired_auth_state)  # Initial check
            if i == 0:
                get_auth_effects.append(valid_auth_state)  # After successful refresh

        mock_session.get_auth = AsyncMock(side_effect=get_auth_effects)

        # Start 5 concurrent requests
        tasks = [get_current_user(mock_request, None) for _ in range(5)]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # First should succeed
        assert isinstance(results[0], User)

        # Others should get 409 (which frontend will retry)
        for i in range(1, 5):
            assert isinstance(results[i], HTTPException)
            assert results[i].status_code == 409
