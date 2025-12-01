# scripts/ingest_sboms.py
from __future__ import annotations

import json
from typing import Any

from app.services import parser


def _count_packages(sbom: dict[str, Any]) -> int:
    """
    Cuenta paquetes en un SBOM de Syft.

    Syft suele incluirlos bajo la clave "artifacts".
    Si no existe, devolvemos 0.
    """
    artifacts = sbom.get("artifacts")
    if isinstance(artifacts, list):
        return len(artifacts)
    return 0


def main() -> None:
    """
    Script sencillo para inspeccionar SBOMs en .evidence/.

    Uso:
      python scripts/ingest_sboms.py
    """
    metas = parser.list_sboms()
    if not metas:
        print("No se encontraron SBOMs en .evidence/.")
        return

    print(f"Encontrados {len(metas)} SBOM(s) en .evidence/:")
    summary: list[dict[str, Any]] = []

    for meta in metas:
        sbom = parser.load_sbom(meta.path)
        pkg_count = _count_packages(sbom)
        summary.append(
            {"service": meta.service, "filename": meta.path.name, "packages": pkg_count}
        )
        print(f"  - {meta.service}: {pkg_count} paquetes ({meta.path.name})")

    # Si quieres, puedes dejar un resumen en .evidence/summary.json
    # sin aún meterte con /stats ni aggregated-report.json:
    from app.core.config import EVIDENCE_DIR

    out_path = EVIDENCE_DIR / "summary.json"
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nResumen escrito en {out_path}")


if __name__ == "__main__":
    main()
