from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .config import settings
from .security import create_access_token, current_user
from .dolibarr import dolibarr

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name}

@app.post("/auth/login")
async def login(body: LoginRequest):
    # Bootstrap Sprint 1 uniquement; remplacer par utilisateurs persistants.
    if body.username != settings.mga_admin_username or body.password != settings.mga_admin_password:
        raise HTTPException(401, "Identifiants incorrects")
    return {"access_token": create_access_token(body.username), "token_type": "bearer"}

@app.get("/dashboard")
async def dashboard(user=Depends(current_user)):
    # KPI placeholders; seront alimentés par les endpoints Dolibarr validés.
    return {
        "user": user["sub"],
        "kpis": [
            {"label": "Devis en cours", "value": "—"},
            {"label": "À encaisser", "value": "—"},
            {"label": "Projets actifs", "value": "—"},
            {"label": "CA du mois", "value": "—"},
        ],
    }

@app.get("/clients")
async def clients(q: str | None = None, page: int = 0, limit: int = 20, user=Depends(current_user)):
    params = {"limit": min(limit, 100), "page": page, "sortfield": "t.nom", "sortorder": "ASC"}
    if q:
        # Dolibarr thirdparties API commonly accepts sqlfilters; validate against your explorer.
        safe = q.replace("'", "")
        params["sqlfilters"] = f"(t.nom:like:'%{safe}%')"
    return await dolibarr.get("thirdparties", params)

@app.get("/clients/{client_id}")
async def client(client_id: int, user=Depends(current_user)):
    return await dolibarr.get(f"thirdparties/{client_id}")

@app.get("/products")
async def products(q: str | None = None, page: int = 0, limit: int = 20, user=Depends(current_user)):
    params = {"limit": min(limit, 100), "page": page, "sortfield": "t.ref", "sortorder": "ASC"}
    if q:
        safe = q.replace("'", "")
        params["sqlfilters"] = f"(t.ref:like:'%{safe}%')"
    return await dolibarr.get("products", params)

@app.get("/products/{product_id}")
async def product(product_id: int, user=Depends(current_user)):
    return await dolibarr.get(f"products/{product_id}")
