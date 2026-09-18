import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import get_settings
from app.database import Base, engine

settings = get_settings()

logging.basicConfig(level=settings.log_level)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if settings.environment == "development":
        # Confort de developpement local uniquement. En staging/production,
        # le schema est gere par Alembic (`alembic upgrade head`), execute
        # explicitement au deploiement (voir DEPLOYMENT.md) : on ne veut
        # jamais qu'un demarrage d'API modifie silencieusement le schema
        # d'une base partagee.
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="MGA API",
    description="Backend intermediaire entre MGA Mobile et Dolibarr (MG Assistance SUARL).",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
