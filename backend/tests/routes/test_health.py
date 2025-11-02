from fastapi.testclient import TestClient


def test_health_get_startup(client: TestClient) -> None:
    response = client.get("/startup")
    assert response.status_code == 204


def test_health_get_readiness(client: TestClient) -> None:
    response = client.get("/readiness")

    assert response.status_code == 204


def test_health_get_liveness(client: TestClient) -> None:
    response = client.get("/liveness")

    assert response.status_code == 204
