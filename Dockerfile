FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal set to reduce build time)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first for better caching
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies first (this layer will be cached)
RUN uv sync --frozen --no-cache

# Copy source code
COPY . .

# Expose port for Flet web app
EXPOSE 8080

# Set environment variables
ENV PYTHONPATH=/app
ENV FLET_WEB_PORT=8080

# Default command
CMD ["uv", "run", "flet", "run", "--web", "--port", "8080", "--host", "0.0.0.0"]