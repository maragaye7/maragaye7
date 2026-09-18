import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import CurrentUser
from app.security.jwt import decode_token

_bearer_scheme = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> CurrentUser:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides ou expires.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        raise credentials_error

    if payload.get("type") != "access":
        raise credentials_error

    user_id = payload.get("sub")
    if not user_id:
        raise credentials_error
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise credentials_error

    user = db.get(User, user_uuid)
    if user is None or not user.is_active:
        raise credentials_error

    return CurrentUser(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        can_see_margins=user.can_see_margins,
    )
