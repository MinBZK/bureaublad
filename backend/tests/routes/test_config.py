from unittest.mock import patch

from fastapi.testclient import TestClient


def test_config_get_unauthenticated(client: TestClient) -> None:
    """Test that config endpoint returns 401 when not authenticated."""
    response = client.get("/api/v1/config")
    assert response.status_code == 401


def test_config_get_authenticated(authenticated_client: TestClient) -> None:
    """Test config endpoint with authenticated session."""
    response = authenticated_client.get("/api/v1/config")

    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "applications" in data
    assert "theme_css" in data
    assert "silent_login" in data
    assert data["silent_login"] is True

    # Verify applications is a list
    assert isinstance(data["applications"], list)

    # Verify each application has the correct structure
    for app in data["applications"]:
        assert "id" in app
        assert "icon" in app
        assert "url" in app
        assert "title" in app
        assert "beta" in app
        assert isinstance(app["id"], str)
        assert app["icon"] is None or isinstance(app["icon"], str)
        assert app["url"] is None or isinstance(app["url"], str)
        assert app["title"] is None or isinstance(app["title"], str)
        assert isinstance(app["beta"], bool)

    # Verify theme_css is a string
    assert isinstance(data["theme_css"], str)


@patch("app.routes.config.settings.DICTAPHONE_URL", "https://dictaphone.example.com")
@patch("app.routes.config.settings.DICTAPHONE_TITLE", "Dicaphone")
def test_config_includes_dictaphone_when_configured(authenticated_client: TestClient) -> None:
    """Test dictaphone app is returned when configured."""
    response = authenticated_client.get("/api/v1/config")
    assert response.status_code == 200

    data = response.json()
    dictaphone = next((app for app in data["applications"] if app["id"] == "dictaphone"), None)

    assert dictaphone is not None
    assert dictaphone["url"] == "https://dictaphone.example.com"
    assert dictaphone["title"] == "Dicaphone"


@patch("app.routes.config.settings.EMAIL_URL", "https://email.example.com")
@patch("app.routes.config.settings.EMAIL_TITLE", "Email")
def test_config_includes_email_when_configured(authenticated_client: TestClient) -> None:
    """Test email app is returned when configured."""
    response = authenticated_client.get("/api/v1/config")
    assert response.status_code == 200

    data = response.json()
    email = next((app for app in data["applications"] if app["id"] == "email"), None)

    assert email is not None
    assert email["url"] == "https://email.example.com"
    assert email["title"] == "Email"


@patch("app.routes.config.settings.DOCS_URL", "https://docs.example.com")
@patch("app.routes.config.settings.DOCS_BETA", True)
def test_config_marks_beta_applications(authenticated_client: TestClient) -> None:
    """Test configured beta applications are marked as beta."""
    response = authenticated_client.get("/api/v1/config")
    assert response.status_code == 200

    data = response.json()
    docs = next((app for app in data["applications"] if app["id"] == "docs"), None)

    assert docs is not None
    assert docs["beta"] is True
