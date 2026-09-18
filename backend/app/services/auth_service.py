from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.user import RefreshToken, User
from app.schemas.auth import TokenPair
from app.security.jwt import create_access_token, create_refresh_token, decode_token
from app.security.password import verify_password


class InvalidCredentialsError(Exception):
    pass


class InvalidRefreshTokenError(Exception):
    pass


class AuthService:
    def __init__(self, db: Session):
        self._db = db
        self._settings = get_settings()

    def authenticate(self, email: str, password: str) -> TokenPair:
        user = self._db.query(User).filter(User.email == email.lower()).first()
        if user is None or not user.is_active or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Email ou mot de passe invalide.")
        return self._issue_tokens(user)

    def refresh(self, refresh_token: str) -> TokenPair:
        try:
            payload = decode_token(refresh_token)
        except JWTError as exc:
            raise InvalidRefreshTokenError("Refresh token invalide.") from exc

        if payload.get("type") != "refresh":
            raise InvalidRefreshTokenError("Type de token invalide.")

        jti = payload.get("jti")
        try:
            user_uuid = uuid.UUID(payload.get("sub", ""))
        except ValueError as exc:
            raise InvalidRefreshTokenError("Refresh token invalide.") from exc

        stored = (
            self._db.query(RefreshToken)
            .filter(RefreshToken.token_jti == jti, RefreshToken.user_id == user_uuid)
            .first()
        )
        if stored is None or not stored.is_valid:
            raise InvalidRefreshTokenError("Refresh token revoque ou expire.")

        user = self._db.get(User, user_uuid)
        if user is None or not user.is_active:
            raise InvalidRefreshTokenError("Utilisateur introuvable ou inactif.")

        # Rotation : on revoque l'ancien refresh token avant d'en emettre un nouveau.
        stored.revoked_at = datetime.now(timezone.utc)
        self._db.add(stored)
        return self._issue_tokens(user)

    def logout(self, refresh_token: str) -> None:
        try:
            payload = decode_token(refresh_token)
        except JWTError:
            return
        jti = payload.get("jti")
        stored = self._db.query(RefreshToken).filter(RefreshToken.token_jti == jti).first()
        if stored is not None and stored.revoked_at is None:
            stored.revoked_at = datetime.now(timezone.utc)
            self._db.add(stored)
            self._db.commit()

    def _issue_tokens(self, user: User) -> TokenPair:
        access_token = create_access_token(str(user.id), user.role.value)
        refresh_token = create_refresh_token(str(user.id), user.role.value)
        payload = decode_token(refresh_token)

        record = RefreshToken(
            user_id=user.id,
            token_jti=payload["jti"],
            expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
        )
        self._db.add(record)
        self._db.commit()

        return TokenPair(access_token=access_token, refresh_token=refresh_token)
