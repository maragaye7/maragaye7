import httpx
from fastapi import HTTPException
from .config import settings

class DolibarrClient:
    def __init__(self):
        self.base_url = settings.dolibarr_api_url.rstrip("/")
        self.headers = {
            "DOLAPIKEY": settings.dolibarr_api_key,
            "Accept": "application/json",
        }

    async def get(self, endpoint: str, params: dict | None = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url, headers=self.headers, params=params)
            if response.status_code == 401:
                raise HTTPException(502, "Authentification Dolibarr refusée")
            if response.status_code >= 400:
                raise HTTPException(502, f"Erreur Dolibarr ({response.status_code})")
            return response.json()
        except httpx.TimeoutException:
            raise HTTPException(504, "Dolibarr ne répond pas dans le délai prévu")
        except httpx.RequestError:
            raise HTTPException(502, "Connexion à Dolibarr impossible")

dolibarr = DolibarrClient()
