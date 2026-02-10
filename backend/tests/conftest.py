import os
from collections.abc import Generator
from unittest.mock import AsyncMock, patch

# Set test environment before importing anything from the app
os.environ["ENVIRONMENT"] = "test"

import pytest
from app.core import session
from app.main import app
from app.models.user import AuthState, User
from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment() -> None:
    """Ensure we're running in test environment."""
    # Verify the environment is set correctly
    from app.core.config import settings

    assert settings.ENVIRONMENT == "test", f"Expected test environment, got {settings.ENVIRONMENT}"
    assert settings.is_testing, "Expected is_testing to be True"


@pytest.fixture(scope="session", autouse=True)
def mock_redis_connection() -> Generator[None]:
    """Mock Redis ping during app startup."""
    redis_client = AsyncMock()
    redis_client.ping = AsyncMock(return_value=True)

    with patch("app.core.lifespan.get_redis_client", return_value=redis_client):
        yield


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def fresh_client() -> Generator[TestClient]:
    """Create a fresh test client for each test to avoid session pollution."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def mock_auth_state() -> AuthState:
    return AuthState(
        sub="test-user-123",
        user=User(name="Test User", email="test@example.com"),
        access_token="test-token",
        refresh_token="test-refresh-token",
        expires_at=9999999999,
    )


@pytest.fixture
def authenticated_client(mock_auth_state: AuthState) -> Generator[TestClient]:
    with patch.object(session, "get_auth", new=AsyncMock(return_value=mock_auth_state)), TestClient(app) as c:
        yield c
