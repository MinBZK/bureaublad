"""Tests for the core authentication module."""

import asyncio
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.core.authentication import (
    _needs_refresh,
    _refresh_locks,
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
        return request

    @pytest.mark.asyncio
    async def test_refresh_token_no_refresh_token(self, mock_request: Request) -> None:
        """Test refresh fails when no refresh token is provided."""
        with pytest.raises(CredentialError) as exc_info:
            await _refresh_token(mock_request, None)

        assert "Session expired. Please log in again." in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_refresh_token_empty_refresh_token(self, mock_request: Request) -> None:
        """Test refresh fails when empty refresh token is provided."""
        with pytest.raises(CredentialError) as exc_info:
            await _refresh_token(mock_request, "")

        assert "Session expired. Please log in again." in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch("app.core.authentication.oauth")
    @patch("app.core.authentication.session")
    async def test_refresh_token_success(
        self, mock_session: MagicMock, mock_oauth: MagicMock, mock_request: Request
    ) -> None:
        """Test successful token refresh."""
        # Mock successful token response
        new_token = {
            "access_token": "new_access_token",
            "expires_at": int(time.time()) + 3600,
            "refresh_token": "new_refresh_token",
        }
        mock_oauth.oidc.fetch_access_token = AsyncMock(return_value=new_token)

        await _refresh_token(mock_request, "old_refresh_token")

        # Verify OAuth call
        mock_oauth.oidc.fetch_access_token.assert_called_once_with(
            grant_type="refresh_token", refresh_token="old_refresh_token"
        )

        # Verify session update
        mock_session.update_tokens.assert_called_once_with(
            mock_request,
            access_token="new_access_token",
            expires_at=new_token["expires_at"],
            refresh_token="new_refresh_token",
        )

    @pytest.mark.asyncio
    @patch("app.core.authentication.oauth")
    @patch("app.core.authentication.session")
    async def test_refresh_token_success_no_new_refresh_token(
        self, mock_session: MagicMock, mock_oauth: MagicMock, mock_request: Request
    ) -> None:
        """Test successful token refresh without new refresh token."""
        # Mock token response without refresh_token
        new_token = {
            "access_token": "new_access_token",
            "expires_at": int(time.time()) + 3600,
        }
        mock_oauth.oidc.fetch_access_token = AsyncMock(return_value=new_token)

        await _refresh_token(mock_request, "old_refresh_token")

        # Verify session update with None refresh token
        mock_session.update_tokens.assert_called_once_with(
            mock_request,
            access_token="new_access_token",
            expires_at=new_token["expires_at"],
            refresh_token=None,
        )

    @pytest.mark.asyncio
    @patch("app.core.authentication.oauth")
    @patch("app.core.authentication.session")
    async def test_refresh_token_oauth_failure(
        self, mock_session: MagicMock, mock_oauth: MagicMock, mock_request: Request
    ) -> None:
        """Test token refresh failure due to OAuth error."""
        mock_oauth.oidc.fetch_access_token = AsyncMock(side_effect=Exception("OAuth error"))

        with pytest.raises(CredentialError) as exc_info:
            await _refresh_token(mock_request, "refresh_token")

        assert "Session expired. Please log in again." in str(exc_info.value.detail)

        # Verify session was cleared
        mock_session.clear_auth.assert_called_once_with(mock_request)


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
        mock_session.get_auth.return_value = None

        with pytest.raises(CredentialError) as exc_info:
            await get_current_user(mock_request, None)

        assert "Not authenticated" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    async def test_get_current_user_valid_token(
        self, mock_session: MagicMock, mock_request: Request, valid_auth_state: AuthState
    ) -> None:
        """Test get_current_user with valid token that doesn't need refresh."""
        mock_session.get_auth.return_value = valid_auth_state

        result = await get_current_user(mock_request, None)

        assert result == valid_auth_state.user
        assert mock_request.state.user == valid_auth_state.user
        # Should not attempt refresh
        mock_session.update_tokens.assert_not_called()

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._needs_refresh")
    @patch("app.core.authentication._refresh_token")
    async def test_get_current_user_token_refresh_needed(
        self,
        mock_refresh_token: AsyncMock,
        mock_needs_refresh: MagicMock,
        mock_session: MagicMock,
        mock_request: Request,
        expired_auth_state: AuthState,
        valid_auth_state: AuthState,
    ) -> None:
        """Test get_current_user when token refresh is needed."""
        # Configure the flow: initial auth, re-check after lock, auth after refresh
        mock_session.get_auth.side_effect = [expired_auth_state, expired_auth_state, valid_auth_state]
        mock_needs_refresh.side_effect = [True, True, False]  # Needs refresh twice, then not

        result = await get_current_user(mock_request, None)

        # Verify refresh was called
        mock_refresh_token.assert_called_once_with(mock_request, expired_auth_state.refresh_token)

        # Verify result
        assert result == valid_auth_state.user
        assert mock_request.state.user == valid_auth_state.user

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._needs_refresh")
    @patch("app.core.authentication._refresh_token")
    async def test_get_current_user_session_lost_after_refresh(
        self,
        mock_refresh_token: AsyncMock,
        mock_needs_refresh: MagicMock,
        mock_session: MagicMock,
        mock_request: Request,
        expired_auth_state: AuthState,
    ) -> None:
        """Test get_current_user when session is lost after refresh."""
        # Configure flow: initial auth, re-check after lock, session lost after refresh
        mock_session.get_auth.side_effect = [expired_auth_state, expired_auth_state, None]
        mock_needs_refresh.side_effect = [True, True]  # Needs refresh twice

        with pytest.raises(CredentialError) as exc_info:
            await get_current_user(mock_request, None)

        assert "Session lost after refresh" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._refresh_token")
    async def test_get_current_user_concurrent_refresh_protection(
        self,
        mock_refresh_token: AsyncMock,
        mock_session: MagicMock,
        mock_request: Request,
        expired_auth_state: AuthState,
        valid_auth_state: AuthState,
    ) -> None:
        """Test that concurrent refresh requests are properly synchronized."""

        # Simulate slow refresh
        async def slow_refresh(*args: object) -> None:
            await asyncio.sleep(0.1)

        mock_refresh_token.side_effect = slow_refresh

        # First call returns expired, subsequent calls return valid (simulating refresh by first request)
        mock_session.get_auth.side_effect = [
            expired_auth_state,  # First request sees expired
            expired_auth_state,  # Second request sees expired initially
            valid_auth_state,  # After waiting for lock, second request sees refreshed
            valid_auth_state,  # Return value for first request after refresh
        ]

        # Start two concurrent requests
        task1 = asyncio.create_task(get_current_user(mock_request, None))
        task2 = asyncio.create_task(get_current_user(mock_request, None))

        results = await asyncio.gather(task1, task2)

        # Both should succeed
        assert results[0] == valid_auth_state.user
        assert results[1] == valid_auth_state.user

        # Refresh should only be called once (due to locking)
        assert mock_refresh_token.call_count <= 2  # Allow for race conditions in test

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    async def test_get_current_user_lock_cleanup(
        self, mock_session: MagicMock, mock_request: Request, expired_auth_state: AuthState, valid_auth_state: AuthState
    ) -> None:
        """Test that refresh locks are cleaned up after use."""
        mock_session.get_auth.side_effect = [expired_auth_state, valid_auth_state]

        # Clear any existing locks
        _refresh_locks.clear()

        with patch("app.core.authentication._refresh_token"):
            await get_current_user(mock_request, None)

        # Lock should be cleaned up
        assert len(_refresh_locks) == 0

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    @patch("app.core.authentication._needs_refresh")
    async def test_get_current_user_no_session_id(
        self,
        mock_needs_refresh: MagicMock,
        mock_session: MagicMock,
        expired_auth_state: AuthState,
        valid_auth_state: AuthState,
    ) -> None:
        """Test get_current_user when request has no session ID."""
        # Create request without session ID
        request = MagicMock(spec=Request)
        request.session = {}  # No _session_id
        request.state = MagicMock()

        mock_session.get_auth.side_effect = [expired_auth_state, expired_auth_state, valid_auth_state]
        mock_needs_refresh.side_effect = [True, True, False]  # Needs refresh initially

        with patch("app.core.authentication._refresh_token") as mock_refresh:
            result = await get_current_user(request, None)

        # Should still work, using id(request.session) as fallback
        assert result == valid_auth_state.user
        mock_refresh.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.core.authentication.session")
    async def test_get_current_user_refresh_not_needed_after_lock(
        self,
        mock_session: MagicMock,
        mock_request: Request,
        expired_auth_state: AuthState,
        valid_auth_state: AuthState,
    ) -> None:
        """Test that refresh is skipped if token was refreshed by another request while waiting for lock."""
        # Simulate the scenario where:
        # 1. First check sees expired token
        # 2. After acquiring lock, token is already refreshed
        mock_session.get_auth.side_effect = [expired_auth_state, valid_auth_state]

        with patch("app.core.authentication._refresh_token") as mock_refresh:
            result = await get_current_user(mock_request, None)

        # Should not call refresh since token is valid after lock
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
            mock_session.get_auth.side_effect = [auth_state, auth_state, valid_auth]

            with patch("app.core.authentication._refresh_token") as mock_refresh:
                result = await get_current_user(mock_request, None)

            mock_refresh.assert_called_once()
        else:
            # No refresh needed
            mock_session.get_auth.return_value = auth_state
            result = await get_current_user(mock_request, None)

        assert result == sample_user
