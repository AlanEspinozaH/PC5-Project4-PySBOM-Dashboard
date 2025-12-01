# app/routers/health.py
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """
    Endpoint de liveness.

    Permite que Docker/K8s y herramientas de monitoreo verifiquen
    que el microservicio está respondiendo.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
