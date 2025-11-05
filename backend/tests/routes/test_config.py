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
    assert "cards" in data
    assert "silent_login" in data
    assert data["silent_login"] is True

    # Verify cards structure - all should be boolean values
    cards = data["cards"]
    expected_keys = ["ai", "docs", "drive", "calendar", "task", "meet", "ocs", "grist", "conversation"]
    for key in expected_keys:
        assert key in cards
        assert isinstance(cards[key], bool)

    # Verify applications is a list
    assert isinstance(data["applications"], list)

    # Verify theme_css is a string
    assert isinstance(data["theme_css"], str)
