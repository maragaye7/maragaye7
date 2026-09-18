"""Emission et verification des JWT (access + refresh tokens).

Rappel securite : ne jamais logger le contenu d'un token (access ou
refresh), ni le mot de passe en clair. Seuls les identifiants d'utilisateur
et les codes d'erreur sont journalises.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import uuid4

from jose import JWTError, jwt

from app.config import get_settings

TokenType = Literal["access", "refresh"]


def _create_token(subject: str, role: str, token_type: TokenType, expires_delta: timedelta) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: str, role: str) -> str:
    settings = get_settings()
    return _create_token(
        user_id, role, "access", timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )


def create_refresh_token(user_id: str, role: str) -> str:
    settings = get_settings()
    return _create_token(
        user_id, role, "refresh", timedelta(days=settings.jwt_refresh_token_expire_days)
    )


def decode_token(token: str) -> dict[str, Any]:
    """Decode et verifie un token. Leve `jose.JWTError` si invalide/expire."""
    settings = get_settings()
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise
