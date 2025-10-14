# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

ENV TERM xterm-256color

WORKDIR /app

# Copy dependency files and install
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

COPY . .

# Container health is determined by the heartbeat file produced by the app
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["bash", "-c", "test -f /app/var/heartbeat && (( $(date +%s) - $(cat /app/var/heartbeat) < 30 ))"]

# Default to running the CLI; additional args can be passed at runtime
ENTRYPOINT ["uv", "run", "--no-sync", "src/main.py"]
