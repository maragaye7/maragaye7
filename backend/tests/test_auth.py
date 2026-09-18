from app.models.user import UserRole
from tests.conftest import auth_headers, create_user


def test_login_success(client, db_session):
    create_user(db_session, email="admin@mga-mobile.dev", password="StrongPass123!", role=UserRole.ADMIN)
    response = client.post(
        "/api/v1/auth/login", json={"email": "admin@mga-mobile.dev", "password": "StrongPass123!"}
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body


def test_login_invalid_password(client, db_session):
    create_user(db_session, email="admin@mga-mobile.dev", password="StrongPass123!")
    response = client.post(
        "/api/v1/auth/login", json={"email": "admin@mga-mobile.dev", "password": "wrong"}
    )
    assert response.status_code == 401


def test_login_unknown_user(client):
    response = client.post(
        "/api/v1/auth/login", json={"email": "nobody@mga-mobile.dev", "password": "whatever"}
    )
    assert response.status_code == 401


def test_me_requires_bearer_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code in (401, 403)


def test_me_returns_current_user(client, db_session):
    create_user(db_session, email="tech@mga-mobile.dev", password="StrongPass123!", role=UserRole.TECHNICIEN)
    headers = auth_headers(client, "tech@mga-mobile.dev", "StrongPass123!")
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["role"] == "TECHNICIEN"


def test_refresh_rotates_token(client, db_session):
    create_user(db_session, email="admin@mga-mobile.dev", password="StrongPass123!")
    login_resp = client.post(
        "/api/v1/auth/login", json={"email": "admin@mga-mobile.dev", "password": "StrongPass123!"}
    )
    old_refresh = login_resp.json()["refresh_token"]

    refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": old_refresh})
    assert refresh_resp.status_code == 200

    # L'ancien refresh token, une fois tourne, ne doit plus etre reutilisable.
    reuse_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": old_refresh})
    assert reuse_resp.status_code == 401


def test_logout_revokes_refresh_token(client, db_session):
    create_user(db_session, email="admin@mga-mobile.dev", password="StrongPass123!")
    login_resp = client.post(
        "/api/v1/auth/login", json={"email": "admin@mga-mobile.dev", "password": "StrongPass123!"}
    )
    refresh_token = login_resp.json()["refresh_token"]

    logout_resp = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert logout_resp.status_code == 204

    refresh_resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 401


def test_technicien_cannot_access_dashboard(client, db_session):
    create_user(db_session, email="tech@mga-mobile.dev", password="StrongPass123!", role=UserRole.TECHNICIEN)
    headers = auth_headers(client, "tech@mga-mobile.dev", "StrongPass123!")
    response = client.get("/api/v1/dashboard/summary", headers=headers)
    assert response.status_code == 403
