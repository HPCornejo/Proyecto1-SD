# Base del contenedor
FROM python:3.12-slim-bullseye

#Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

#Copiar archivos de la api al contenedor
COPY . /app

#Moverse a la carpeta app
WORKDIR /app

#Instalar las dependencias de python
RUN uv sync --frozen --no-cache

# Ejecutarl la api
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80"]