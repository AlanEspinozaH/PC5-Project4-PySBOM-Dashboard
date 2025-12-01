# app/core/config.py
from __future__ import annotations

import os
from pathlib import Path

# Directorio base del proyecto (dos niveles encima de este archivo).
BASE_DIR: Path = Path(__file__).resolve().parents[2]

# Directorio donde se guardan los SBOMs en JSON.
# Puedes sobreescribirlo con la variable de entorno EVIDENCE_DIR si quieres.
EVIDENCE_DIR: Path = Path(
    os.getenv("EVIDENCE_DIR", BASE_DIR / ".evidence")
).resolve()

# Asegura que .evidence exista para evitar errores tontos al escribir.
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
