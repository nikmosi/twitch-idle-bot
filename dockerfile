# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:alpine

ENV TERM xterm-256color

RUN apk add --no-cache ca-certificates openssl gcompat \
  && update-ca-certificates 


ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

WORKDIR /app

# Copy dependency files and install
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

COPY . .

# Default to running the CLI; additional args can be passed at runtime
ENTRYPOINT ["uv", "run", "--no-sync", "src/main.py"]
