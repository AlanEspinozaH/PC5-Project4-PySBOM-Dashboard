# PySBOM-Dash: Supply Chain & SBOM Dashboard

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-005571?logo=fastapi)
![Status](https://img.shields.io/badge/Status-Sprint_1_In_Progress-yellow)

## 📋 Descripción del Proyecto

**PySBOM-Dash** es un microservicio diseñado para proporcionar visibilidad sobre la seguridad de la cadena de suministro de software (Software Supply Chain).

En un entorno moderno de microservicios, conocer exactamente qué librerías y versiones se están ejecutando es crítico. Este proyecto automatiza la ingesta, análisis y visualización de **SBOMs (Software Bill of Materials)** generados por herramientas como **Syft**.

### 🎯 Objetivo (Contexto Real)
Construir una herramienta centralizada para un equipo de plataforma/seguridad que necesita:
1.  Recolectar SBOMs de múltiples microservicios.
2.  Visualizar estadísticas de dependencias (paquetes más usados, riesgos).
3.  Mantener un historial auditable de los componentes de software en `.evidence/`.

---

## 🛠️ Tech Stack & Herramientas

* **Lenguaje:** Python 3.11+
* **Framework Web:** FastAPI (ASGI).
* **Containerización:** Docker & Docker Compose (Imágenes *slim* y *non-root*).
* **Seguridad & SBOM:** Syft (Generación de SBOM), Grype (Escaneo opcional).
* **CI/CD:** GitHub Actions (Linting, Testing, Artifact Management).
* **Gestión de Proyectos:** Tablero Kanban (GitHub Projects).

---

## 🚀 Instalación y Ejecución Local

Este proyecto sigue la política de **"Cero dependencias externas"** para su ejecución local (salvo Docker).

### Prerrequisitos
* Python 3.11+
* Docker & Docker Compose
* Git

### 1. Configuración del Entorno
```bash
# Clonar repositorio
git clone <url-del-repo>
cd PC5-Project4-PySBOM-Dashboard

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt -r requirements-dev.txt
````

### 2\. Ejecución del Servidor (Development)

```bash
# Inicia el servidor con recarga automática
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000/docs`

### 3\. Generación de Datos de Prueba (Simulación)

Como el dashboard necesita leer SBOMs, genera uno localmente:

```bash
# Requiere tener 'syft' instalado o usar el script wrapper (próximamente)
mkdir -p .evidence
syft dir:. -o json > .evidence/sbom-dashboard.json
```

-----

## 🚀 Cómo ejecutarlo (Localmente)

Para facilitar la revisión, el proyecto está configurado para correr con un solo comando usando Docker Compose.

### 1. Clonar y Levantar
```bash
git clone <url-del-repo>
cd PC5-Project4-PySBOM-Dashboard
```

# Levanta la app y monta el volumen de evidencias
docker compose up --build
2. Probar Endpoints
Una vez activo, puedes acceder a:

Documentación Interactiva: http://localhost:8000/docs

Estadísticas de SBOM: http://localhost:8000/stats

Healthcheck: http://localhost:8000/health

## 📅 Roadmap de Sprints (7 Días)

Este proyecto se desarrolla en 3 Sprints de 2 días cada uno, más un día de demo final[cite: 8].

### ✅ Sprint 1: MVP & Ingesta (Días 1-2)

  - [ ] Configuración de FastAPI y estructura del proyecto.
  - [ ] Endpoint `/health` y `/sboms` (lectura básica de archivos).
  - [ ] Integración de **Syft** local para generar `sbom.json`.
  - [ ] Pipeline CI: Linting y Tests básicos.

### ✅ Sprint 2: Análisis & Estadísticas (Días 3-4) 

  - [ ] Endpoint `/stats`: Conteo de paquetes y Top 5 dependencias.
  - [ ] Tests unitarios para lógica de agregación.
  - [ ] Pipeline `dashboard_update.yml`: Consolidación de SBOMs automática.
  - [ ] Dockerización inicial (Dockerfile).

### ✅ Sprint 3: Hardening & Producción (Días 5-6) 

  - [ ] Dockerfile seguro (User non-root, multi-stage).
  - [ ] Despliegue en Docker Compose (o K8s local/Minikube).
  - [ ] Reportes de vulnerabilidades en `.evidence/`.
  - [ ] Documentación final y Video Demo.

-----

## 📂 Estructura de Evidencias (.evidence/)

Cumpliendo con los requisitos de la práctica, la carpeta `.evidence/` es crítica y versionada. Contiene:

  * `sbom-*.json`: Los SBOMs crudos generados por el pipeline.
  * `aggregated-report.json`: El estado consolidado del dashboard.
  * `ci-report.txt` / `scan-report.json`: Salidas de los tests y escaneos de seguridad.

-----

## 🤖 Pipelines de GitHub Actions

1.  **`ci.yml`**: Ejecuta `ruff` (linter), `black` (formato) y `pytest` en cada Pull Request.
2.  **`sbom_ingest.yml`**: Genera el SBOM del propio dashboard y lo sube como *Artifact*.
3.  **`dashboard_update.yml`**: Simula la recolección de SBOMs y actualiza las estadísticas globales.

-----

## 👥 Autor
Alumnos: Alan Espinoza , Rodolfo Estacio, Junior Turpo
Proyecto desarrollado para el curso CC3S2 - Desarrollo de Software del profesor Cesar Lara.
