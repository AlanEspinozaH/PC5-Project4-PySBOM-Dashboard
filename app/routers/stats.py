from __future__ import annotations

from fastapi import APIRouter
from app.services import parser as sbom_parser

router = APIRouter()


@router.get("/")
def get_stats():
    """
    Devuelve estadísticas agregadas de los SBOMs.
    Cumple con el requisito del Sprint 2: conteo de paquetes.
    """
    sboms = sbom_parser.list_sboms()

    total_sboms = len(sboms)
    total_packages = 0
    services_summary = []

    for meta in sboms:
        try:
            data = sbom_parser.load_sbom(meta.path)
            # Syft guarda los paquetes en "artifacts"
            artifacts = data.get("artifacts", [])
            count = len(artifacts)
            total_packages += count
            services_summary.append({"service": meta.service, "packages": count})
        except Exception:
            # Si falla la lectura de uno, no rompemos todo
            continue

    return {
        "total_services_monitored": total_sboms,
        "total_packages_tracked": total_packages,
        "details_by_service": services_summary,
    }
