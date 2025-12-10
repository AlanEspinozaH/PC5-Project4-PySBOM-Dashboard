# app/services/parser.py
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from app.core.config import EVIDENCE_DIR


class SBOMParseError(Exception):
    """Error al parsear un archivo SBOM JSON."""


@dataclass(frozen=True)
class SBOMMetadata:
    """
    Metadatos mínimos de un SBOM detectado en .evidence/.
    """

    service: str
    path: Path


def _service_name_from_path(path: Path) -> str:
    """
    Infere el nombre de servicio a partir del nombre de archivo.

    Convenciones:
    - sbom-<service>.json -> <service>
    - sbom_<service>.json -> <service>
    - sbom.json           -> 'dashboard' (este propio proyecto)
    - cualquier otra cosa -> stem del archivo
    """
    name = path.name

    if name == "sbom.json":
        # Caso típico de la práctica: SBOM de este dashboard
        return "dashboard"

    if name.startswith("sbom-") and name.endswith(".json"):
        return name[len("sbom-") : -len(".json")]

    if name.startswith("sbom_") and name.endswith(".json"):
        return name[len("sbom_") : -len(".json")]

    if name.startswith("sbom") and name.endswith(".json"):
        # "sbom-xyz.json" o "sbomxyz.json" – fallback genérico
        core = name[len("sbom") : -len(".json")].lstrip("-_")
        return core or "dashboard"

    return path.stem


def list_sboms() -> list[SBOMMetadata]:
    """
    Descubre todos los SBOMs en .evidence/ con patrón sbom*.json.
    """
    sbom_paths: Iterable[Path] = sorted(EVIDENCE_DIR.glob("sbom*.json"))
    return [
        SBOMMetadata(service=_service_name_from_path(path), path=path)
        for path in sbom_paths
    ]


def load_sbom(path: Path) -> dict[str, Any]:
    """
    Carga un SBOM desde un archivo JSON.

    Raises:
        SBOMParseError: si el contenido no es JSON válido.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        # Dejamos que lo manejen arriba si llaman directo con un path malo.
        raise exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise SBOMParseError(f"File '{path}' is not valid JSON: {exc}") from exc


def load_sbom_for_service(service: str) -> dict[str, Any]:
    """
    Busca el SBOM correspondiente a un servicio y lo devuelve como dict.

    Estrategia:
      1. Llama a list_sboms().
      2. Busca el primer SBOM cuyo `service` coincida.
      3. Lo carga con load_sbom().
    """
    for meta in list_sboms():
        if meta.service == service:
            return load_sbom(meta.path)

    raise FileNotFoundError(f"No SBOM found for service '{service}' in {EVIDENCE_DIR}")
