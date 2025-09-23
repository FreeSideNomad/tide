FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies
RUN uv sync --no-cache

# Copy source code
COPY . .

# Expose port for Flet web app
EXPOSE 8080

# Set environment variables
ENV PYTHONPATH=/app
ENV FLET_WEB_PORT=8080

# Default command
CMD ["uv", "run", "flet", "run", "--web", "--port", "8080", "--host", "0.0.0.0"]