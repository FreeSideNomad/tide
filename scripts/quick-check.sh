#!/bin/bash

# Quick validation script for fast local checks
# Use this for rapid feedback during development

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "\n${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

echo -e "${BLUE}🚀 Quick Code Validation${NC}\n"

# 1. Code formatting
print_step "Checking code formatting..."
if uv run black --check --quiet src/ tests/ 2>/dev/null; then
    print_success "Code formatting OK"
else
    print_warning "Formatting issues found - run 'uv run black src/ tests/' to fix"
fi

# 2. Linting
print_step "Running linter..."
if uv run ruff check src/ tests/ --quiet 2>/dev/null; then
    print_success "Linting OK"
else
    print_warning "Linting issues found - run 'uv run ruff check --fix src/ tests/' to fix"
fi

# 3. Basic imports
print_step "Testing imports..."
if uv run python -c "import src.main; import src.config" 2>/dev/null; then
    print_success "Imports OK"
else
    print_error "Import errors found"
    exit 1
fi

# 4. Quick unit tests
print_step "Running quick tests..."
export OPENAI_API_KEY="test-key"
if uv run pytest tests/test_basic.py -q --tb=no 2>/dev/null; then
    print_success "Basic tests OK"
else
    print_error "Basic tests failed"
    exit 1
fi

# 5. Environment check
print_step "Environment check..."
if [ -z "$OPENAI_API_KEY" ]; then
    print_warning "OPENAI_API_KEY not set"
else
    print_success "Environment OK"
fi

echo -e "\n${GREEN}✅ Quick validation complete!${NC}"
echo -e "${BLUE}Run './scripts/validate.sh' for full validation before committing.${NC}\n"