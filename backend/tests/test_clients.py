from app.models.user import UserRole
from tests.conftest import auth_headers, create_user

RAW_THIRDPARTIES = [
    {"id": "101", "name": "ACME Solaire", "email": "contact@acme.sn", "phone": "771234567", "town": "Dakar"},
    {"id": "102", "name": "Sahel Energie", "email": "info@sahel.sn", "phone": "781112233", "town": "Thies"},
]


def test_search_clients_requires_auth(client):
    response = client.get("/api/v1/clients")
    assert response.status_code in (401, 403)


def test_search_clients_returns_mapped_summary(client, db_session, mock_dolibarr):
    create_user(db_session, email="com@mga-mobile.dev", password="StrongPass123!", role=UserRole.COMMERCIAL)
    headers = auth_headers(client, "com@mga-mobile.dev", "StrongPass123!")

    mock_dolibarr.get.return_value = RAW_THIRDPARTIES

    response = client.get("/api/v1/clients", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["meta"]["page"] == 1
    assert len(body["items"]) == 2
    assert body["items"][0]["name"] == "ACME Solaire"
    mock_dolibarr.get.assert_called_once()
    called_path = mock_dolibarr.get.call_args.args[0]
    assert called_path == "/thirdparties"


def test_search_clients_filters_by_query(client, db_session, mock_dolibarr):
    create_user(db_session, email="com@mga-mobile.dev", password="StrongPass123!", role=UserRole.COMMERCIAL)
    headers = auth_headers(client, "com@mga-mobile.dev", "StrongPass123!")

    mock_dolibarr.get.return_value = RAW_THIRDPARTIES

    response = client.get("/api/v1/clients", params={"query": "sahel"}, headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["name"] == "Sahel Energie"


def test_search_clients_pagination_params(client, db_session, mock_dolibarr):
    create_user(db_session, email="com@mga-mobile.dev", password="StrongPass123!", role=UserRole.COMMERCIAL)
    headers = auth_headers(client, "com@mga-mobile.dev", "StrongPass123!")
    mock_dolibarr.get.return_value = []

    response = client.get("/api/v1/clients", params={"page": 2, "limit": 10}, headers=headers)
    assert response.status_code == 200
    kwargs = mock_dolibarr.get.call_args.kwargs
    assert kwargs["params"]["limit"] == 10
    assert kwargs["params"]["page"] == 1  # page 2 cote MGA -> page 1 cote Dolibarr (0-index)


def test_get_client_not_found(client, db_session, mock_dolibarr):
    from app.dolibarr import DolibarrNotFoundError

    create_user(db_session, email="com@mga-mobile.dev", password="StrongPass123!", role=UserRole.COMMERCIAL)
    headers = auth_headers(client, "com@mga-mobile.dev", "StrongPass123!")
    mock_dolibarr.get.side_effect = DolibarrNotFoundError("not found")

    response = client.get("/api/v1/clients/999", headers=headers)
    assert response.status_code == 404


def test_technicien_can_read_clients(client, db_session, mock_dolibarr):
    create_user(db_session, email="tech@mga-mobile.dev", password="StrongPass123!", role=UserRole.TECHNICIEN)
    headers = auth_headers(client, "tech@mga-mobile.dev", "StrongPass123!")
    mock_dolibarr.get.return_value = RAW_THIRDPARTIES

    response = client.get("/api/v1/clients", headers=headers)
    assert response.status_code == 200
