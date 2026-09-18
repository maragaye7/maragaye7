import os
from collections.abc import Generator
from unittest.mock import MagicMock

# Doit etre defini avant tout import de `app.*` : le moteur SQLAlchemy de
# l'application est cree une seule fois, au chargement de `app.database.session`.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("DOLIBARR_API_KEY", "test-key")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.dolibarr import DolibarrClient, get_dolibarr_client
from app.main import app
from app.models.user import User, UserRole
from app.security.password import hash_password

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture()
def db_session() -> Generator:
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def mock_dolibarr() -> MagicMock:
    """DolibarrClient entierement mocke : aucun appel reseau reel n'est effectue."""
    return MagicMock(spec=DolibarrClient)


@pytest.fixture()
def client(db_session, mock_dolibarr) -> Generator[TestClient, None, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    app.dependency_overrides[get_dolibarr_client] = lambda: mock_dolibarr

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def create_user(
    db_session,
    *,
    email: str = "user@mga-mobile.dev",
    password: str = "SuperSecret123!",
    role: UserRole = UserRole.ADMIN,
    can_see_margins: bool = False,
) -> User:
    user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name="Test User",
        role=role,
        can_see_margins=can_see_margins,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def auth_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
