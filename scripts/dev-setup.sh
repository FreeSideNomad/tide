#!/bin/bash

# Tide Development Environment Setup Script
# One-command setup for new developers

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}${BOLD}$1${NC}"
    echo -e "${BLUE}$(printf '=%.0s' {1..50})${NC}"
}

print_step() {
    echo -e "\n${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_prerequisites() {
    print_step "Checking prerequisites..."

    # Check Git
    if command -v git &> /dev/null; then
        print_success "Git is installed"
    else
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi

    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION is installed"
    else
        print_error "Python 3 is not installed. Please install Python 3.9+ first."
        exit 1
    fi

    # Check uv
    if command -v uv &> /dev/null; then
        print_success "uv is installed"
    else
        print_warning "uv is not installed. Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
        if command -v uv &> /dev/null; then
            print_success "uv installed successfully"
        else
            print_error "Failed to install uv. Please install manually."
            exit 1
        fi
    fi

    # Check Docker (optional)
    if command -v docker &> /dev/null && docker info &> /dev/null 2>&1; then
        print_success "Docker is available"
        DOCKER_AVAILABLE=true
    else
        print_warning "Docker is not available. Some features will be limited."
        DOCKER_AVAILABLE=false
    fi

    # Check Make
    if command -v make &> /dev/null; then
        print_success "Make is available"
    else
        print_warning "Make is not installed. You'll need to run commands manually."
    fi
}

setup_environment() {
    print_step "Setting up Python environment..."

    # Install dependencies
    uv sync
    print_success "Dependencies installed"

    # Check if .env exists
    if [ ! -f ".env" ]; then
        print_step "Creating .env file..."
        cp .env.example .env
        print_warning "Created .env file from template"
        print_info "Please edit .env and add your OPENAI_API_KEY"
    else
        print_success ".env file already exists"
    fi
}

setup_git_hooks() {
    print_step "Setting up Git hooks..."

    if [ -f "./scripts/setup-hooks.sh" ]; then
        ./scripts/setup-hooks.sh
        print_success "Git hooks configured"
    else
        print_warning "Git hooks setup script not found"
    fi
}

run_initial_validation() {
    print_step "Running initial validation..."

    # Set test API key if not set
    if [ -z "$OPENAI_API_KEY" ]; then
        export OPENAI_API_KEY="test-key"
        print_info "Using test API key for validation"
    fi

    # Run quick check
    if ./scripts/quick-check.sh; then
        print_success "Initial validation passed"
    else
        print_warning "Initial validation failed - this is expected for a fresh setup"
        print_info "You can fix issues later with 'make format' and 'make lint-fix'"
    fi
}

setup_docker() {
    if [ "$DOCKER_AVAILABLE" = true ]; then
        print_step "Testing Docker setup..."

        # Pull required images
        echo "Pulling PostgreSQL with pgvector..."
        docker pull pgvector/pgvector:pg16

        # Test Docker Compose
        if docker-compose config &> /dev/null; then
            print_success "Docker Compose configuration is valid"
        else
            print_warning "Docker Compose configuration has issues"
        fi
    fi
}

show_next_steps() {
    print_header "🎉 Setup Complete!"

    echo -e "${GREEN}Your Tide development environment is ready!${NC}\n"

    print_header "📋 Next Steps"

    echo -e "${YELLOW}1. Configure your API key:${NC}"
    echo "   Edit .env and add your OpenAI API key"
    echo "   Or set environment variable: export OPENAI_API_KEY='your-key'"
    echo ""

    echo -e "${YELLOW}2. Start developing:${NC}"
    echo "   make dev                 # Start development server"
    echo "   make dev-docker          # Start with Docker (full stack)"
    echo ""

    echo -e "${YELLOW}3. Development workflow:${NC}"
    echo "   make quick-check         # Fast validation (run frequently)"
    echo "   make validate            # Full validation (before commits)"
    echo "   make test-unit           # Run unit tests"
    echo ""

    echo -e "${YELLOW}4. Get help:${NC}"
    echo "   make help                # Show all available commands"
    echo "   cat dev-setup.md         # Read detailed setup guide"
    echo "   cat scripts/README.md    # Learn about validation scripts"
    echo ""

    if [ "$DOCKER_AVAILABLE" = false ]; then
        echo -e "${YELLOW}5. Install Docker (recommended):${NC}"
        echo "   Install Docker Desktop for full development experience"
        echo "   This enables integration tests and containerized development"
        echo ""
    fi

    print_header "🚀 Quick Start"
    echo "   make dev                 # Start the application"
    echo "   # Make some changes..."
    echo "   make quick-check         # Validate changes"
    echo "   git add ."
    echo "   git commit -m 'feat: your changes'"
    echo ""

    print_header "📚 Documentation"
    echo "   • dev-setup.md          - Comprehensive setup guide"
    echo "   • scripts/README.md     - Validation scripts documentation"
    echo "   • CLAUDE.md            - Project guidelines and architecture"
    echo "   • docs/wiki/           - Project vision and requirements"
    echo ""

    print_success "Happy coding! 🎯"
}

# Main execution
main() {
    print_header "🌊 Tide Development Environment Setup"

    echo -e "${BLUE}This script will set up your complete development environment.${NC}\n"

    check_prerequisites
    setup_environment
    setup_git_hooks

    if [ "$DOCKER_AVAILABLE" = true ]; then
        setup_docker
    fi

    run_initial_validation
    show_next_steps
}

# Run main function
main "$@"