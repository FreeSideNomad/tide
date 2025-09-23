# Tide - Safety-First DBT AI Assistant

**Tide** is a Python Flet application targeting mobile and web users. This is a safety-first DBT (Dialectical Behavior Therapy) AI assistant designed to guide individuals through DBT skills development using structured decision-tree architecture.

## 🚀 Quick Start

### 🐳 Docker (Recommended)

The fastest way to get Tide running using our pre-built Docker images:

**📦 Container Registry**: [ghcr.io/freesidenomad/tide](https://github.com/FreeSideNomad/tide/pkgs/container/tide)

#### Quick Start

```bash
# Pull latest image
docker pull ghcr.io/freesidenomad/tide:latest

# Run with required environment variables
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your_openai_key \
  -e GOOGLE_CLIENT_ID=your_google_client_id \
  -e GOOGLE_CLIENT_SECRET=your_google_client_secret \
  ghcr.io/freesidenomad/tide:latest
```

Access the app at: **http://localhost:8080**

#### Available Image Tags

- `ghcr.io/freesidenomad/tide:latest` - Latest stable release
- `ghcr.io/freesidenomad/tide:main` - Latest main branch build
- `ghcr.io/freesidenomad/tide:main-<commit>` - Specific commit builds

#### Multi-Architecture Support

Our Docker images support both:
- `linux/amd64` (Intel/AMD 64-bit)
- `linux/arm64` (Apple Silicon/ARM 64-bit)

#### Production Deployment

For production, use Docker Compose with PostgreSQL:

```bash
# Download production compose file
curl -O https://raw.githubusercontent.com/FreeSideNomad/tide/main/docker-compose.prod.yml

# Set your environment variables
export OPENAI_API_KEY=your_key
export GOOGLE_CLIENT_ID=your_client_id
export GOOGLE_CLIENT_SECRET=your_client_secret

# Deploy with PostgreSQL and Redis
docker compose -f docker-compose.prod.yml up -d
```

**📚 Complete Docker documentation**: [docs/docker.md](docs/docker.md)

### Local Development

#### Using uv (Recommended)

Run as a desktop app:
```bash
uv run flet run
```

Run as a web app:
```bash
uv run flet run --web --port 8080
```

#### Using Poetry

Install dependencies:
```bash
poetry install
```

Run as a desktop app:
```bash
poetry run flet run
```

Run as a web app:
```bash
poetry run flet run --web --port 8080
```

### Environment Variables

Create a `.env` file with:
```bash
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_client_secret
DATABASE_URL=postgresql://user:password@localhost:5432/tide_db  # optional
```

## 🚀 Deployment

### Docker Container Registry

Tide Docker images are automatically built and published to GitHub Container Registry (GHCR):

**📦 Registry**: [ghcr.io/freesidenomad/tide](https://github.com/FreeSideNomad/tide/pkgs/container/tide)

#### Image Versioning Strategy

| Tag Pattern | Description | Use Case |
|-------------|-------------|----------|
| `latest` | Latest stable release from main branch | Production deployments |
| `main` | Latest build from main branch | Staging/preview |
| `main-<sha>` | Specific commit builds | Rollbacks, testing |

#### Health Checks & Monitoring

All Docker images include health check endpoints:

```bash
# Container health check
docker run --health-cmd="curl -f http://localhost:8080/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  ghcr.io/freesidenomad/tide:latest

# Check application health
curl http://localhost:8080/health
```

### Cloud Platform Deployment

#### Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/deploy?template=https://github.com/FreeSideNomad/tide)

#### Deploy to DigitalOcean

```bash
# Create app from Docker image
doctl apps create - <<EOF
name: tide-app
services:
- name: web
  image:
    registry_type: GHCR
    repository: freesidenomad/tide
    tag: latest
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 8080
  envs:
  - key: OPENAI_API_KEY
    value: your_key
    type: SECRET
  - key: GOOGLE_CLIENT_ID
    value: your_client_id
    type: SECRET
  - key: GOOGLE_CLIENT_SECRET
    value: your_client_secret
    type: SECRET
EOF
```

#### Deploy to AWS ECS

```bash
# Create ECS task definition
aws ecs register-task-definition \
  --family tide-app \
  --requires-compatibilities FARGATE \
  --network-mode awsvpc \
  --cpu 256 \
  --memory 512 \
  --container-definitions '[{
    "name": "tide",
    "image": "ghcr.io/freesidenomad/tide:latest",
    "portMappings": [{"containerPort": 8080}],
    "environment": [
      {"name": "OPENAI_API_KEY", "value": "your_key"},
      {"name": "GOOGLE_CLIENT_ID", "value": "your_client_id"},
      {"name": "GOOGLE_CLIENT_SECRET", "value": "your_client_secret"}
    ]
  }]'
```

### Container Orchestration

For production deployments with high availability:

```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tide-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tide
  template:
    metadata:
      labels:
        app: tide
    spec:
      containers:
      - name: tide
        image: ghcr.io/freesidenomad/tide:latest
        ports:
        - containerPort: 8080
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: tide-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**📚 Complete deployment guides**: [docs/docker.md](docs/docker.md)

### Automated CI/CD Pipeline

Docker images are automatically built and published on every push to the main branch:

**🔄 GitHub Actions Workflow**:
- ✅ Code quality checks (formatting, linting)
- ✅ Comprehensive testing (unit, integration, E2E)
- ✅ Security scanning (dependency vulnerabilities, code analysis)
- ✅ Multi-architecture Docker builds (`linux/amd64`, `linux/arm64`)
- ✅ Automated publishing to [GitHub Container Registry](https://github.com/FreeSideNomad/tide/pkgs/container/tide)

**📈 Build Status**: [![CI/CD Pipeline](https://github.com/FreeSideNomad/tide/actions/workflows/ci.yml/badge.svg)](https://github.com/FreeSideNomad/tide/actions/workflows/ci.yml)

## 🔧 Build the app

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).