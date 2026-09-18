from app.models.user import UserRole
from tests.conftest import auth_headers, create_user

RAW_PRODUCTS = [
    {
        "id": "501",
        "ref": "PV-JKM-620",
        "label": "Panneau Jinko 620W",
        "price": "150000",
        "cost_price": "110000",
        "tva_tx": "18",
        "stock_reel": "42",
    },
    {
        "id": "502",
        "ref": "ONDUL-DEYE-20K",
        "label": "Onduleur Deye triphase 20kW",
        "price": "2500000",
        "cost_price": "1900000",
        "tva_tx": "18",
        "stock_reel": "5",
    },
]


def test_search_products_requires_auth(client):
    response = client.get("/api/v1/products")
    assert response.status_code in (401, 403)


def test_technicien_does_not_see_purchase_price(client, db_session, mock_dolibarr):
    create_user(db_session, email="tech@mga-mobile.dev", password="StrongPass123!", role=UserRole.TECHNICIEN)
    headers = auth_headers(client, "tech@mga-mobile.dev", "StrongPass123!")
    mock_dolibarr.get.return_value = RAW_PRODUCTS

    response = client.get("/api/v1/products", headers=headers)
    assert response.status_code == 200
    for item in response.json()["items"]:
        assert item["purchase_price"] is None
        assert item["margin_amount"] is None


def test_admin_sees_purchase_price_and_margin(client, db_session, mock_dolibarr):
    create_user(db_session, email="admin@mga-mobile.dev", password="StrongPass123!", role=UserRole.ADMIN)
    headers = auth_headers(client, "admin@mga-mobile.dev", "StrongPass123!")
    mock_dolibarr.get.return_value = RAW_PRODUCTS

    response = client.get("/api/v1/products", headers=headers)
    assert response.status_code == 200
    item = response.json()["items"][0]
    assert item["purchase_price"] == 110000.0
    assert item["margin_amount"] == 40000.0


def test_search_products_by_query(client, db_session, mock_dolibarr):
    create_user(db_session, email="admin@mga-mobile.dev", password="StrongPass123!", role=UserRole.ADMIN)
    headers = auth_headers(client, "admin@mga-mobile.dev", "StrongPass123!")
    mock_dolibarr.get.return_value = RAW_PRODUCTS

    response = client.get("/api/v1/products", params={"query": "deye"}, headers=headers)
    assert response.status_code == 200
    kwargs = mock_dolibarr.get.call_args.kwargs
    assert "sqlfilters" in kwargs["params"]


def test_get_product_not_found(client, db_session, mock_dolibarr):
    from app.dolibarr import DolibarrNotFoundError

    create_user(db_session, email="admin@mga-mobile.dev", password="StrongPass123!", role=UserRole.ADMIN)
    headers = auth_headers(client, "admin@mga-mobile.dev", "StrongPass123!")
    mock_dolibarr.get.side_effect = DolibarrNotFoundError("not found")

    response = client.get("/api/v1/products/999", headers=headers)
    assert response.status_code == 404
