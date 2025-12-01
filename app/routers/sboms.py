# app/routers/sboms.py
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import parser as sbom_parser

router = APIRouter()


class SBOMListItem(BaseModel):
    """
    Item de la lista de SBOMs expuestos por el dashboard.
    """

    service: str
    filename: str


@router.get("/", response_model=list[SBOMListItem])
def list_sboms() -> list[SBOMListItem]:
    """
    Lista todos los SBOMs disponibles en .evidence/.

    Cada SBOM se identifica por el nombre de servicio inferido del
    nombre de archivo (sbom-<service>.json o sbom.json -> dashboard).
    """
    metadata_items = sbom_parser.list_sboms()

    return [
        SBOMListItem(service=meta.service, filename=meta.path.name)
        for meta in metadata_items
    ]


@router.get("/{service}", response_model=dict)
def get_sbom(service: str) -> dict[str, Any]:
    """
    Devuelve el SBOM completo para un servicio dado.

    - 404 si no existe SBOM para ese servicio.
    - 500 si el archivo existe pero está corrupto o no es JSON válido.
    """
    try:
        sbom_data = sbom_parser.load_sbom_for_service(service)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"SBOM for service '{service}' not found.",
        )
    except sbom_parser.SBOMParseError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    return sbom_data
