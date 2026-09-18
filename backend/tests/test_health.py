from app.dolibarr import DolibarrConnectionError


def test_health_ok(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_dolibarr_ok(client, mock_dolibarr):
    mock_dolibarr.get.return_value = []
    response = client.get("/api/v1/health/dolibarr")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_dolibarr_error_does_not_raise(client, mock_dolibarr):
    mock_dolibarr.get.side_effect = DolibarrConnectionError("unreachable")
    response = client.get("/api/v1/health/dolibarr")
    assert response.status_code == 200
    assert response.json()["status"] == "error"
