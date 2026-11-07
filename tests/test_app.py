from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_fallback(monkeypatch):
    monkeypatch.setenv("PRIMARY_MODE", "error")

    response = client.get("/ask", params={"question": "Hello"})

    assert response.status_code == 200
    assert response.json()["provider"] == "secondary"
