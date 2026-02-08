FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Enable bytecode compilation for faster startup
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking (container isolation)
ENV UV_LINK_MODE=copy

# Install dependencies first (cache layer)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy application code
COPY app/ app/

# Sync again to finalize
RUN uv sync --frozen --no-dev

# 默认 8000，可通过环境变量 PORT 覆盖
ENV PORT=8000
EXPOSE 8000

# 使用 shell 形式以支持 $PORT
CMD uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
