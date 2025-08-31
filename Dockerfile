FROM python:3.13-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/

COPY . /app

WORKDIR /app

RUN uv sync --locked

CMD ["/app/.venv/bin/fastapi", "run", "/app/src/lithic_api/__init__.py", "--port", "80"]