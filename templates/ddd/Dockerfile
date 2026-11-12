# syntax=docker/dockerfile:1
FROM python:3.12-slim

# uv for dependency management (matches the project's uv workflow).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install dependencies first for layer caching, using only the manifests.
# uv.lock is optional here (uv.lock* matches nothing until it exists); commit
# it so images resolve the same versions as local runs.
# --no-install-project: run the app from source (no build backend needed).
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --no-install-project

# App source.
COPY . .

EXPOSE 8000

# --no-sync: use the already-installed venv, don't try to (re)install the project.
CMD ["uv", "run", "--no-dev", "--no-sync", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
