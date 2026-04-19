FROM python:3.13.2-slim

COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /uvx /bin/

WORKDIR  /app

COPY pyproject.toml uv.lock /app/

ARG ENV

ENV UV_PROJECT_ENVIRONMENT=/opt/venv

RUN if [ "$ENV" = "only_main" ]; then \
      uv sync --no-dev --no-cache --compile-bytecode --frozen; \
    else \
      uv sync --all-groups --no-cache --compile-bytecode --frozen; \
    fi


COPY . /app

ENV PATH="/opt/venv/bin:$PATH"
