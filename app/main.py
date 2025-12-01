# app/main.py
from __future__ import annotations

from fastapi import FastAPI

from app.routers import health, sboms


def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.

    En Sprint 1 sólo exponemos /health y /sboms.
    /stats se añadirá en Sprint 2.
    """
    application = FastAPI(
        title="Python SBOM Dashboard",
        version="0.1.0",
        description=(
            "Microservicio interno para exponer SBOMs de servicios Python "
            "y apoyar la visibilidad de la cadena de suministro."
        ),
    )

    # Endpoints básicos
    application.include_router(health.router, tags=["health"])
    application.include_router(sboms.router, prefix="/sboms", tags=["sboms"])

    return application


# Instancia que usará uvicorn y los tests
app: FastAPI = create_app()
