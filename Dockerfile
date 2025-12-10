# Usa una imagen base oficial y ligera de Python
FROM python:3.11-slim

# Evita que Python escriba archivos .pyc y buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar curl para el healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Crear un usuario no-root para seguridad (Requisito del PDF)
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app app
# Copiar scripts si son necesarios
COPY scripts scripts

# Cambiar la propiedad de los archivos al usuario no-root
RUN chown -R appuser:appuser /app

# Cambiar al usuario no-root (Hardening)
USER appuser

# Exponer el puerto
EXPOSE 8000

# Healthcheck para verificar que la app está viva (Requisito)
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]