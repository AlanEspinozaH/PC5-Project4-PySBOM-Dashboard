# app/main.py
from __future__ import annotations
from fastapi import FastAPI
from app.routers import health, sboms, stats  # <--- Importar stats


def create_app() -> FastAPI:
    application = FastAPI(
        title="Python SBOM Dashboard",
        version="0.2.0",  # <--- Bump de versión Sprint 2
        description="Dashboard de Supply Chain Security",
    )

    application.include_router(health.router, tags=["health"])
    application.include_router(sboms.router, prefix="/sboms", tags=["sboms"])
    application.include_router(
        stats.router, prefix="/stats", tags=["stats"]
    )  # <--- Registrar stats

    return application


app: FastAPI = create_app()
