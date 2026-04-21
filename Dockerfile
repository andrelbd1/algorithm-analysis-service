ARG PYTHON_IMAGE=python:3.12.6-alpine3.20
# Pin uv for reproducible builds: https://github.com/astral-sh/uv/pkgs/container/uv
ARG UV_VERSION=0.11.6

# BuildKit does not allow variables in `COPY --from=…` for external images; use a named stage.
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

FROM ${PYTHON_IMAGE} AS base

COPY --from=uv /uv /uvx /usr/local/bin/

# Install packages
RUN apk add --no-cache libcurl

# Needed for pycurl
ENV PYCURL_SSL_LIBRARY=openssl
RUN apk update && apk add --no-cache \
       postgresql-libs \
       curl \
       htop \
       vim \
       curl-dev \
       bash \
       linux-headers
RUN apk upgrade --no-cache

WORKDIR /app

# Use the image Python only (do not download another interpreter during sync).
# Omit UV_SYSTEM_PYTHON so the project venv (`.venv`) stays the install target (matches PATH below).
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_NO_EDITABLE=1 \
    UV_PYTHON_DOWNLOADS=0

# Install locked third-party deps first (better layer cache when only app code changes).
COPY pyproject.toml uv.lock README.md ./

RUN --mount=type=cache,target=/root/.cache/uv \
    apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        postgresql-dev \
    && uv sync --locked --no-install-project \
    && apk del .build-deps

# Application sources and non-editable install of the `src` package (see UV_NO_EDITABLE).
COPY migrations ./migrations
COPY src ./src
COPY alembic.ini ./alembic.ini
COPY main.py ./main.py

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

ENV PATH="/app/.venv/bin:${PATH}"

# CI: `docker build --target test`
FROM base AS test
COPY tests ./tests
RUN uv run pytest --cov=src --cov-report=xml -q tests

# ENTRYPOINT ["python", "main.py"]
# CMD ["server"]