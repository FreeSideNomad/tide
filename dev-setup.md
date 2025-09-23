# Development Setup Guide

This guide will help you set up the development environment for the Tide DBT AI Assistant.

## Prerequisites

- Python 3.9 or higher
- Git
- uv package manager
- Docker and Docker Compose (recommended for development)
- PostgreSQL (for production database, or use Docker)

## Initial Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd tide
```

### 2. Install Dependencies

The project uses `uv` for package management. If you don't have `uv` installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install project dependencies:

```bash
uv sync
```

This will:
- Create a virtual environment at `.venv/`
- Install Flet and all required dependencies
- Install development dependencies (black, ruff, pytest)

### 3. Environment Configuration

Set up your environment variables:

```bash
# Copy the example environment file
cp .env.example .env

# Set your OpenAI API key in your environment
export OPENAI_API_KEY="your-api-key-here"

# Or add it to your .env file
echo "OPENAI_API_KEY=your-api-key-here" >> .env
```

**Required Environment Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key for AI functionality

**Optional Environment Variables:**
- `DATABASE_URL`: PostgreSQL connection string (defaults to local development)
- `DEBUG`: Set to "True" for development mode
- `ENVIRONMENT`: Set to "development", "staging", or "production"

### 4. Database Setup

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL with pgvector using Docker Compose
docker-compose up -d postgres

# The database will be available at localhost:5432
# Database: tide_db
# Username: tide_user
# Password: tide_password
```

#### Option B: Local PostgreSQL Installation

```bash
# Install PostgreSQL with pgvector extension
# On macOS with Homebrew:
brew install postgresql pgvector

# Start PostgreSQL service
brew services start postgresql

# Create database
createdb tide_db
```

### 5. Run the Application

#### Option A: Using Docker Compose (Full Stack)

```bash
# Start the entire application stack (PostgreSQL + App)
export OPENAI_API_KEY="your-api-key-here"
docker-compose up

# The application will be available at http://localhost:8080
```

#### Option B: Local Development

```bash
# Run the Flet application locally
uv run flet run

# Run in web mode
uv run flet run --web --port 8080

# Or run directly
uv run python src/main.py
```

## Development Commands

### Local Validation Scripts

The project includes comprehensive validation tools for local development:

```bash
# Quick validation (fast feedback during development)
./scripts/quick-check.sh
make quick-check

# Full validation (comprehensive, run before committing)
./scripts/validate.sh
make validate

# Setup Git hooks for automatic validation
./scripts/setup-hooks.sh
make setup-hooks
```

### Makefile Commands

Use the Makefile for convenient development commands:

```bash
# Show all available commands
make help

# Development workflow
make install          # Install dependencies
make dev             # Start development server
make dev-docker      # Start with Docker Compose

# Code quality (run frequently during development)
make quick-check     # Fast validation
make format          # Format code
make lint            # Check linting
make lint-fix        # Fix linting issues

# Testing
make test            # Run all tests
make test-unit       # Unit tests only
make test-int        # Integration tests only
make coverage        # Test coverage report

# Full validation (before committing)
make validate        # Comprehensive validation
make ci              # Simulate CI pipeline
```

### Running Tests

#### Local Testing

```bash
# Run all tests
uv run pytest

# Run tests by type
uv run pytest tests/unit/          # Unit tests only
uv run pytest tests/integration/   # Integration tests only
uv run pytest tests/e2e/          # End-to-end tests only

# Run with coverage
uv run pytest --cov=src --cov-report=html --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_config.py -v
```

#### Docker Testing

```bash
# Run all tests in Docker environment
docker-compose --profile test run --rm test

# Run specific test types in Docker
docker-compose run --rm test uv run pytest tests/unit/ -v
docker-compose run --rm test uv run pytest tests/integration/ -v
```

#### Browser Testing Setup

For end-to-end tests, install browser drivers:

```bash
# Install Playwright browsers
uv run playwright install

# Install ChromeDriver for Selenium (alternative)
# On macOS with Homebrew:
brew install chromedriver
```

### Code Formatting and Linting

```bash
# Format code with black
uv run black src/ tests/

# Lint with ruff
uv run ruff check src/ tests/

# Fix auto-fixable issues
uv run ruff check --fix src/ tests/
```

### Building for Different Platforms

```bash
# Build for web
uv run flet build web

# Build for desktop
uv run flet build

# Build for mobile (requires additional setup)
uv run flet build apk
uv run flet build ipa
```

## Project Structure

```
tide/
├── src/                           # Source code
│   ├── main.py                   # Main application entry point
│   ├── config.py                 # Configuration management
│   └── assets/                   # Static assets (images, icons)
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   ├── e2e/                      # End-to-end tests
│   │   └── screenshots/          # E2E test screenshots
│   └── conftest.py              # Shared test fixtures
├── .github/
│   └── workflows/               # GitHub Actions CI/CD
│       ├── ci.yml              # Main CI pipeline
│       └── codeql.yml          # Security code scanning
├── docs/                        # Documentation
│   └── wiki/                   # Git submodule for project wiki
├── scripts/                     # Development scripts
│   └── init-db.sql             # Database initialization
├── Dockerfile                   # Container configuration
├── docker-compose.yml          # Local development stack
├── pytest.ini                  # Test configuration
├── .env.example               # Example environment variables
├── .env                       # Local environment variables (not in git)
├── pyproject.toml            # Project configuration and dependencies
└── dev-setup.md             # This file
```

## Technology Stack

- **Frontend Framework**: Flet (Python-based cross-platform UI)
- **Database**: PostgreSQL with pgvector extension
- **ORM**: SQLAlchemy
- **AI Integration**: OpenAI API
- **Testing**: pytest with coverage, Selenium & Playwright for E2E
- **Code Quality**: black (formatting) + ruff (linting)
- **Package Management**: uv
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions with security scanning
- **Browser Automation**: Selenium & Playwright

## Development Workflow

### Recommended Development Process

1. **Setup** (one-time):
   ```bash
   make install        # Install dependencies
   make setup-hooks    # Setup Git hooks
   ```

2. **During development** (frequent):
   ```bash
   make quick-check    # Fast validation (~10 seconds)
   make dev           # Start development server
   ```

3. **Before committing** (thorough):
   ```bash
   make validate      # Full validation (~2-5 minutes)
   git add .
   git commit -m "feat: your changes"  # Hooks run automatically
   ```

4. **Before pushing** (comprehensive):
   ```bash
   make ci            # Simulate CI pipeline
   git push           # Hooks run automatically
   ```

### Manual Development Steps

If you prefer manual commands:

1. **Make changes** to source code in `src/`
2. **Quick validation**: `./scripts/quick-check.sh`
3. **Format code**: `uv run black src/ tests/`
4. **Check linting**: `uv run ruff check --fix src/ tests/`
5. **Test the app**: `uv run flet run` or `docker-compose up`
6. **Run tests**: `uv run pytest tests/unit/`
7. **Full validation**: `./scripts/validate.sh`
8. **Commit changes** following conventional commit format

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

- **Code Quality**: Runs black, ruff, and type checking
- **Unit Tests**: Runs all unit tests with coverage reporting
- **Integration Tests**: Tests database and API integrations
- **E2E Tests**: Browser-based testing of the complete application
- **Security Scanning**: CodeQL analysis and dependency vulnerability checks
- **Docker Build**: Ensures the application builds correctly in containers

All pull requests must pass the CI pipeline before merging.

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY environment variable is required"**
   - Make sure you've set the `OPENAI_API_KEY` environment variable
   - Check that your `.env` file is properly configured

2. **Database connection errors**
   - Ensure PostgreSQL is running: `docker-compose up -d postgres`
   - Verify the `DATABASE_URL` in your environment
   - Check Docker container logs: `docker-compose logs postgres`

3. **Import errors**
   - Make sure you're using `uv run` to execute commands
   - Verify all dependencies are installed: `uv sync`

4. **Docker/Docker Compose issues**
   - Ensure Docker is running: `docker --version`
   - Clean up containers: `docker-compose down --volumes`
   - Rebuild images: `docker-compose build --no-cache`

5. **Test failures**
   - Install browser drivers: `uv run playwright install`
   - Check if application is running: `curl http://localhost:8080`
   - View test screenshots in `tests/e2e/screenshots/` for E2E test debugging

6. **Port conflicts**
   - Stop other services on ports 5432, 8080
   - Use different ports: `docker-compose up -p custom-port`

### Getting Help

- Check the project wiki at `docs/wiki/`
- Review the main project documentation in `CLAUDE.md`
- Create an issue in the project repository for bugs or questions

## Next Steps

After setup is complete:

1. Review the project vision in `docs/wiki/vision.md`
2. Understand the DBT AI assistant requirements
3. Follow the development process outlined in `CLAUDE.md`
4. Start with domain modeling before implementing features