# Evidencias de Seguridad y Cadena de Suministro

Esta carpeta contiene los artefactos inmutables generados automáticamente por nuestros pipelines de CI/CD para auditoría y trazabilidad.

## Contenido de Archivos

### 1. SBOM (Software Bill of Materials)
* **Archivo:** `sbom-dashboard.json` (o similar)
* **Herramienta:** [Syft](https://github.com/anchore/syft)
* **Descripción:** Lista completa de paquetes del sistema operativo y librerías de Python instaladas en el contenedor/entorno.
* **Uso:** Permite detectar si estamos usando versiones vulnerables de alguna librería (ej. `requests`, `fastapi`) sin tener que inspeccionar el código fuente manualmente.

### 2. Reporte de Tests
* **Origen:** GitHub Actions (Job `build-and-test`)
* **Descripción:** Garantiza que la lógica de negocio (como el cálculo de estadísticas en `/stats`) funciona correctamente antes del despliegue.

### 3. Reporte Agregado (Simulado)
* **Archivo:** `aggregated-report.json`
* **Origen:** Pipeline `Dashboard Update`
* **Descripción:** Representa la consolidación de datos de múltiples microservicios para la vista centralizada del dashboard.