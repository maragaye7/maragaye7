"""RBAC applicatif.

Matrice des roles (voir ARCHITECTURE.md section 4) :
  ADMIN       -> acces complet
  DIRECTION   -> dashboard/CA/marges, clients, devis, factures, commandes, projets (lecture)
  COMMERCIAL  -> clients, contacts, produits, devis, commandes (CRUD commercial)
  TECHNICIEN  -> projets, interventions, photos, materiel, rapports

Les prix d'achat et marges sont masques par defaut pour COMMERCIAL et
TECHNICIEN (permission "margins:view").
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.models.user import UserRole
from app.schemas.auth import CurrentUser
from app.security.dependencies import get_current_user

_ROLE_PERMISSIONS: dict[UserRole, set[str]] = {
    UserRole.ADMIN: {
        "dashboard:view",
        "clients:read",
        "clients:write",
        "products:read",
        "products:write",
        "proposals:read",
        "proposals:write",
        "orders:read",
        "orders:write",
        "invoices:read",
        "invoices:write",
        "projects:read",
        "projects:write",
        "margins:view",
    },
    UserRole.DIRECTION: {
        "dashboard:view",
        "clients:read",
        "products:read",
        "proposals:read",
        "orders:read",
        "invoices:read",
        "projects:read",
        "margins:view",
    },
    UserRole.COMMERCIAL: {
        "dashboard:view",
        "clients:read",
        "clients:write",
        "products:read",
        "proposals:read",
        "proposals:write",
        "orders:read",
        "orders:write",
    },
    UserRole.TECHNICIEN: {
        "clients:read",
        "products:read",
        "projects:read",
        "projects:write",
    },
}


def role_has_permission(role: UserRole, permission: str, *, override_margins: bool = False) -> bool:
    if permission == "margins:view" and override_margins:
        return True
    return permission in _ROLE_PERMISSIONS.get(role, set())


def require_role(*allowed_roles: UserRole) -> Callable[..., CurrentUser]:
    def _dependency(current_user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acces refuse pour ce role.",
            )
        return current_user

    return _dependency


def require_permission(permission: str) -> Callable[..., CurrentUser]:
    def _dependency(current_user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        if not role_has_permission(
            current_user.role, permission, override_margins=current_user.can_see_margins
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission manquante: {permission}",
            )
        return current_user

    return _dependency
