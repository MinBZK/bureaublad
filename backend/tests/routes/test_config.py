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
        assert "enabled" in app
        assert "icon" in app
        assert "url" in app
        assert "title" in app
        assert "iframe" in app
        assert isinstance(app["id"], str)
        assert isinstance(app["enabled"], bool)
        assert app["icon"] is None or isinstance(app["icon"], str)
        assert app["url"] is None or isinstance(app["url"], str)
        assert app["title"] is None or isinstance(app["title"], str)
        assert isinstance(app["iframe"], bool)

    # Verify theme_css is a string
    assert isinstance(data["theme_css"], str)
