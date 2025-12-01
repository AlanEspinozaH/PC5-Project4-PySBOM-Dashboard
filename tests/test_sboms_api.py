# tests/test_sboms_api.py
from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import EVIDENCE_DIR
from app.main import app

client = TestClient(app)


def _create_sample_sbom(service: str) -> Path:
    """
    Crea un SBOM JSON mínimo en .evidence/ para pruebas.
    """
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    path = EVIDENCE_DIR / f"sbom-{service}.json"

    sample = {
        "artifacts": [
            {"name": "example-package", "version": "1.0.0"},
        ]
    }
    path.write_text(json.dumps(sample), encoding="utf-8")
    return path


def test_list_and_get_sbom_roundtrip() -> None:
    # Arrange: crear un SBOM de ejemplo
    path = _create_sample_sbom("demo")

    try:
        # /sboms debe listar el SBOM recién creado
        resp_list = client.get("/sboms")
        assert resp_list.status_code == 200
        items = resp_list.json()
        assert any(
            item["service"] == "demo" and item["filename"] == path.name
            for item in items
        )

        # /sboms/demo debe devolver el contenido del SBOM
        resp_detail = client.get("/sboms/demo")
        assert resp_detail.status_code == 200
        data = resp_detail.json()
        assert "artifacts" in data
        assert len(data["artifacts"]) == 1
        assert data["artifacts"][0]["name"] == "example-package"
    finally:
        # Limpieza para no dejar archivos basura en .evidence/
        path.unlink(missing_ok=True)
