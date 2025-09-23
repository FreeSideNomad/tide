# Docker Publishing & Deployment

Tide uses GitHub Container Registry (ghcr.io) for Docker image publishing with automated CI/CD workflows.

## 📦 Available Images

### Development Images (Main Branch)
- **Latest**: `ghcr.io/freesidenomad/tide:latest`
- **SHA-tagged**: `ghcr.io/freesidenomad/tide:main-<git-sha>`

### Release Images (Tagged Versions)
- **Semantic versions**: `ghcr.io/freesidenomad/tide:v1.0.0`
- **Major.minor**: `ghcr.io/freesidenomad/tide:1.0`
- **Major**: `ghcr.io/freesidenomad/tide:1` (for v1.x.x and above)

## 🚀 Quick Start

### Pull and Run Latest
```bash
# Pull latest development image
docker pull ghcr.io/freesidenomad/tide:latest

# Run with required environment variables
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your_openai_key \
  -e GOOGLE_CLIENT_ID=your_google_client_id \
  -e GOOGLE_CLIENT_SECRET=your_google_client_secret \
  ghcr.io/freesidenomad/tide:latest
```

### Production Deployment
```bash
# Pull specific release version
docker pull ghcr.io/freesidenomad/tide:v1.0.0

# Run in production mode
docker run -d \
  --name tide-app \
  -p 8080:8080 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID \
  -e GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET \
  -e DATABASE_URL=$DATABASE_URL \
  -e ENVIRONMENT=production \
  --restart unless-stopped \
  ghcr.io/freesidenomad/tide:v1.0.0
```

## 🐳 Docker Compose

### Development with Database
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: tide_db
      POSTGRES_USER: tide_user
      POSTGRES_PASSWORD: tide_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    image: ghcr.io/freesidenomad/tide:latest
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://tide_user:tide_password@postgres:5432/tide_db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - ENVIRONMENT=production
    depends_on:
      - postgres

volumes:
  postgres_data:
```

Run with:
```bash
# Create environment file
echo "OPENAI_API_KEY=your_key" > .env
echo "GOOGLE_CLIENT_ID=your_client_id" >> .env
echo "GOOGLE_CLIENT_SECRET=your_client_secret" >> .env

# Start services
docker compose -f docker-compose.prod.yml up -d
```

## 🏗️ Publishing Workflow

### Automatic Publishing

1. **Development Images**: Published automatically on every push to `main`
   - Triggers after all tests pass
   - Tagged as `latest` and `main-<sha>`
   - Multi-architecture builds (AMD64, ARM64)

2. **Release Images**: Published on git tags
   - Trigger: Push tags like `v1.0.0`, `v1.2.3-beta`
   - Creates semantic version tags
   - Generates GitHub release with deployment instructions

### Manual Release Process

```bash
# Create and push a release tag
git tag v1.0.0
git push origin v1.0.0

# This triggers:
# 1. Full test validation
# 2. Docker image build and push
# 3. GitHub release creation
```

## 🔧 Image Features

### Multi-Architecture Support
- **linux/amd64**: Intel/AMD x64 systems
- **linux/arm64**: Apple Silicon, ARM servers

### Optimizations
- **Layer caching**: GitHub Actions cache for faster builds
- **Minimal size**: Python 3.13 slim base image
- **Security**: Non-root user, minimal dependencies
- **Health checks**: Built-in application health monitoring

### Included Tools
- **uv**: Fast Python package manager
- **PostgreSQL client**: Database connectivity tools
- **Git**: Version control (for development)

## 📋 Environment Variables

### Required
- `OPENAI_API_KEY`: OpenAI API authentication
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret

### Optional
- `DATABASE_URL`: PostgreSQL connection (default: embedded SQLite)
- `DEBUG`: Enable debug mode (default: False)
- `ENVIRONMENT`: deployment environment (development/production)
- `FLET_WEB_PORT`: Web server port (default: 8080)

## 🔒 Security & Authentication

### Registry Access
- **Public images**: Available without authentication
- **GitHub Container Registry**: Uses GitHub authentication for pushing
- **GITHUB_TOKEN**: Automatically provided in GitHub Actions

### Image Security
- **Vulnerability scanning**: Automated security scans in CI
- **Dependency checks**: Safety and Bandit security linting
- **Minimal attack surface**: Only necessary packages included

## 📊 Monitoring & Logs

### Container Logs
```bash
# View application logs
docker logs -f tide-app

# Follow logs from compose
docker compose -f docker-compose.prod.yml logs -f app
```

### Health Checks
```bash
# Check if application is healthy
curl http://localhost:8080/health

# Container health status
docker ps --filter name=tide-app --format "table {{.Names}}\t{{.Status}}"
```

## 🚨 Troubleshooting

### Common Issues

1. **Missing environment variables**
   ```bash
   # Check container environment
   docker exec tide-app env | grep -E "(OPENAI|GOOGLE)"
   ```

2. **Database connection issues**
   ```bash
   # Test database connectivity
   docker exec tide-app pg_isready -h postgres -p 5432
   ```

3. **Port conflicts**
   ```bash
   # Use different port
   docker run -p 3000:8080 ghcr.io/freesidenomad/tide:latest
   ```

### Performance Optimization

```bash
# Allocate more memory for large workloads
docker run --memory=2g --cpus=2 \
  -p 8080:8080 \
  ghcr.io/freesidenomad/tide:latest
```

## 🔄 Updates & Rollbacks

### Update to Latest
```bash
# Pull new image
docker pull ghcr.io/freesidenomad/tide:latest

# Recreate container
docker compose -f docker-compose.prod.yml up -d --force-recreate app
```

### Rollback to Previous Version
```bash
# Use specific version
docker pull ghcr.io/freesidenomad/tide:v1.0.0
docker run -d --name tide-app-rollback ghcr.io/freesidenomad/tide:v1.0.0

# Update compose file to use specific version
```