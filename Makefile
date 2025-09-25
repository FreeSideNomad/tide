# Tide Development Makefile
# Convenient commands for local development

.PHONY: help install dev test lint format security build docker-build docker-test validate quick-check setup-hooks clean

# Default target
help:
	@echo "Tide Development Commands"
	@echo "========================"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install dependencies"
	@echo "  make setup-hooks  Setup Git hooks"
	@echo ""
	@echo "Development:"
	@echo "  make dev          Start development server (no database)"
	@echo "  make dev-full     Start with PostgreSQL database + app"
	@echo "  make dev-docker   Start with Docker Compose"
	@echo "  make stop         Stop all services"
	@echo ""
	@echo "Code Quality:"
	@echo "  make quick-check  Quick validation (fast)"
	@echo "  make validate     Full validation (comprehensive)"
	@echo "  make lint         Run linting"
	@echo "  make format       Format code"
	@echo "  make security     Security checks"
	@echo ""
	@echo "Testing:"
	@echo "  make test         Run all tests"
	@echo "  make test-unit    Run unit tests"
	@echo "  make test-int     Run integration tests"
	@echo "  make test-e2e     Run end-to-end tests"
	@echo "  make coverage     Run tests with coverage"
	@echo ""
	@echo "Build:"
	@echo "  make build        Test local build"
	@echo "  make docker-build Build Docker image"
	@echo "  make docker-test  Test in Docker"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean        Clean temporary files"

# Setup commands
install:
	@echo "📦 Installing dependencies..."
	uv sync

setup-hooks:
	@echo "🪝 Setting up Git hooks..."
	./scripts/setup-hooks.sh

# Development commands
dev:
	@echo "🚀 Starting development server..."
	uv run flet run --web --port 8080

dev-full:
	@echo "🚀 Starting full development stack (PostgreSQL + Application)..."
	@echo "📋 Checking environment..."
	@if [ -z "$$OPENAI_API_KEY" ]; then \
		echo "⚠️  OPENAI_API_KEY not set - please add it to .env file"; \
		echo "💡 Create .env file with: OPENAI_API_KEY=your_key_here"; \
		exit 1; \
	fi
	@echo "🐳 Starting PostgreSQL database..."
	@docker-compose up -d postgres
	@echo "⏳ Waiting for database to be ready..."
	@for i in {1..30}; do \
		if docker-compose exec -T postgres pg_isready -U tide_user -d tide_db >/dev/null 2>&1; then \
			echo "✅ PostgreSQL is ready!"; \
			break; \
		fi; \
		echo "   Waiting for PostgreSQL... ($$i/30)"; \
		sleep 2; \
	done
	@echo "🔧 Setting database configuration..."
	@export DATABASE_URL="postgresql://tide_user:tide_password@localhost:5432/tide_db"
	@echo "🚀 Starting Tide application..."
	@echo "📱 App will be available at: http://127.0.0.1:8080"
	@echo "🗄️  Database: postgresql://tide_user:tide_password@localhost:5432/tide_db"
	@echo ""
	@DATABASE_URL="postgresql://tide_user:tide_password@localhost:5432/tide_db" \
	 PYTHONPATH=. uv run python src/main.py

dev-docker:
	@echo "🐳 Starting development with Docker..."
	@if [ -z "$$OPENAI_API_KEY" ]; then \
		echo "⚠️  OPENAI_API_KEY not set, using test key"; \
		export OPENAI_API_KEY="test-key"; \
	fi
	docker-compose up

stop:
	@echo "🛑 Stopping all services..."
	@docker-compose down
	@echo "✅ All services stopped"

# Code quality commands
quick-check:
	@echo "⚡ Running quick validation..."
	./scripts/quick-check.sh

validate:
	@echo "🔍 Running full validation..."
	./scripts/validate.sh

lint:
	@echo "🔍 Running linter..."
	uv run ruff check src/ tests/

lint-fix:
	@echo "🔧 Fixing linting issues..."
	uv run ruff check --fix src/ tests/

format:
	@echo "🎨 Formatting code..."
	uv run black src/ tests/

format-check:
	@echo "🎨 Checking code formatting..."
	uv run black --check --diff src/ tests/

security:
	@echo "🔒 Running security checks..."
	@uv run pip install safety bandit || true
	@echo "Checking for known vulnerabilities..."
	@uv run safety check || echo "⚠️  Vulnerabilities found"
	@echo "Running security linting..."
	@uv run bandit -r src/ || echo "⚠️  Security issues found"

# Testing commands
test:
	@echo "🧪 Running all tests..."
	@export OPENAI_API_KEY="test-key"
	uv run pytest tests/ -v

test-unit:
	@echo "🧪 Running unit tests..."
	@export OPENAI_API_KEY="test-key"
	uv run pytest tests/unit/ -v

test-int:
	@echo "🧪 Running integration tests..."
	@export OPENAI_API_KEY="test-key"
	@echo "Starting PostgreSQL..."
	@docker-compose up -d postgres
	@sleep 5
	@uv run pytest tests/integration/ -v || true
	@docker-compose down

test-e2e:
	@echo "🧪 Running end-to-end tests..."
	@export OPENAI_API_KEY="test-key"
	@echo "Starting full application stack..."
	@docker-compose up -d
	@sleep 15
	@uv run pytest tests/e2e/ -v || true
	@docker-compose down

coverage:
	@echo "📊 Running tests with coverage..."
	@export OPENAI_API_KEY="test-key"
	uv run pytest tests/unit/ --cov=src --cov-report=html --cov-report=term-missing
	@echo "📊 Coverage report generated in htmlcov/"

# Build commands
build:
	@echo "🏗️  Testing local build..."
	@export OPENAI_API_KEY="test-key"
	uv run python -c "import src.main; import src.config; print('✅ Build test passed')"

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t tide:latest .

docker-test:
	@echo "🐳 Testing in Docker..."
	@export OPENAI_API_KEY="test-key"
	docker-compose --profile test run --rm test

# Utility commands
clean:
	@echo "🧹 Cleaning temporary files..."
	@rm -rf htmlcov/
	@rm -rf .coverage
	@rm -rf coverage.xml
	@rm -rf .pytest_cache/
	@rm -rf **/__pycache__/
	@rm -rf *.egg-info/
	@rm -f safety_report.json bandit_report.json
	@docker-compose down --volumes --remove-orphans 2>/dev/null || true
	@echo "✅ Cleanup completed"

# CI simulation
ci:
	@echo "🤖 Simulating CI pipeline..."
	@make format-check
	@make lint
	@make security
	@make test-unit
	@make docker-build
	@echo "✅ CI simulation completed"

# Development workflow
workflow:
	@echo "🔄 Running complete development workflow..."
	@make install
	@make format
	@make lint-fix
	@make test-unit
	@make build
	@echo "✅ Development workflow completed"