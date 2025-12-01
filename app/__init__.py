# app/__init__.py
"""
Paquete principal de la aplicación SBOM Dashboard.

Exponemos `app` para que herramientas como uvicorn puedan
encontrar la instancia de FastAPI usando `app.main:app`.
"""

from .main import app  # noqa: F401
