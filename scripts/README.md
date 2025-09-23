# Development Scripts

This directory contains automation scripts for local development and validation.

## Scripts Overview

### 🔍 `validate.sh`
**Comprehensive validation script** - Run before committing

- ✅ Code formatting (black)
- ✅ Linting (ruff)
- ✅ Type checking (mypy, optional)
- ✅ Security scanning (safety, bandit)
- ✅ Unit tests with coverage
- ✅ Integration tests (with Docker)
- ✅ Build validation
- ✅ Optional E2E tests

**Usage:**
```bash
./scripts/validate.sh                    # Full validation
./scripts/validate.sh --skip-e2e         # Skip E2E tests
./scripts/validate.sh --coverage-threshold 90  # Custom coverage
```

### ⚡ `quick-check.sh`
**Fast validation script** - Run frequently during development

- ✅ Code formatting check
- ✅ Basic linting
- ✅ Import validation
- ✅ Quick unit tests
- ✅ Environment check

**Usage:**
```bash
./scripts/quick-check.sh    # Fast feedback (~10 seconds)
```

### 🪝 `setup-hooks.sh`
**Git hooks setup** - One-time setup for automatic validation

Installs Git hooks:
- **pre-commit**: Runs quick-check before commits
- **pre-push**: Runs full validation before pushing
- **commit-msg**: Validates conventional commit format

**Usage:**
```bash
./scripts/setup-hooks.sh    # One-time setup
```

### 📄 `init-db.sql`
**Database initialization** - PostgreSQL setup for Docker

- Creates pgvector extension
- Sets up initial permissions

## Script Features

### Validation Levels

1. **Quick Check** (~10 seconds)
   - Essential checks for rapid feedback
   - Run frequently during development

2. **Full Validation** (~2-5 minutes)
   - Comprehensive checks before committing
   - Includes security scanning and coverage

3. **CI Simulation**
   - Matches GitHub Actions pipeline
   - Use for final validation

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `OPENAI_API_KEY` | OpenAI API access | `test-key` |
| `SKIP_E2E` | Skip E2E tests | `false` |
| `COVERAGE_THRESHOLD` | Minimum coverage % | `80` |

### Docker Integration

Scripts automatically detect Docker availability:
- **With Docker**: Runs full integration tests
- **Without Docker**: Skips Docker-dependent tests with warnings

### Error Handling

All scripts:
- ✅ Exit on first error (`set -e`)
- ✅ Colored output for clarity
- ✅ Detailed error messages
- ✅ Cleanup on exit

## Examples

### Daily Development
```bash
# Start development
make dev

# Make changes to code
# ...

# Quick validation (run frequently)
make quick-check

# Continue development
```

### Before Committing
```bash
# Full validation
make validate

# If all passes
git add .
git commit -m "feat: implement new feature"
```

### Troubleshooting
```bash
# Fix formatting issues
make format

# Fix linting issues
make lint-fix

# Run specific test types
make test-unit
make test-int

# Clean up temporary files
make clean
```

## Integration with Make

All scripts are integrated with the Makefile for convenience:

```bash
make quick-check    # ./scripts/quick-check.sh
make validate       # ./scripts/validate.sh
make setup-hooks    # ./scripts/setup-hooks.sh
```

See `make help` for all available commands.

## Customization

### Adding New Checks

To add new validation steps:

1. **Quick checks** → Edit `quick-check.sh`
2. **Comprehensive checks** → Edit `validate.sh`
3. **Add Make target** → Edit `Makefile`

### Modifying Thresholds

Edit the configuration section in `validate.sh`:

```bash
COVERAGE_THRESHOLD=80
MAX_COMPLEXITY=10
```

### Custom Hooks

Modify `.git/hooks/` files after running `setup-hooks.sh`:

```bash
# Customize pre-commit hook
vim .git/hooks/pre-commit
```