from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_api_key_required():
    response = client.post("/api/leads", json={"name":"A","email":"a@example.com","message":"Need pricing please"})
    assert response.status_code == 401

def test_lead_validation_requires_message():
    response = client.post("/api/leads", headers={"X-API-Key":"local-demo-key-change-me"},
                           json={"name":"A","email":"a@example.com","message":"x"})
    assert response.status_code == 422
