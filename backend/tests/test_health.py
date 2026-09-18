from fastapi.testclient import TestClient
# Import requires a configured .env; this test is intended after environment setup.
from app.main import app

def test_health():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
