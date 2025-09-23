#!/bin/bash

# Setup Git hooks for automatic validation

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Setting up Git hooks for Tide project${NC}\n"

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Tide pre-commit hook
# Runs quick validation before allowing commits

echo "🔍 Running pre-commit validation..."

# Run quick check
if ./scripts/quick-check.sh; then
    echo "✅ Pre-commit validation passed"
    exit 0
else
    echo "❌ Pre-commit validation failed"
    echo "💡 Fix the issues above before committing"
    echo "💡 Or run './scripts/validate.sh' for detailed checks"
    exit 1
fi
EOF

# Create pre-push hook
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash

# Tide pre-push hook
# Runs full validation before pushing to remote

echo "🚀 Running pre-push validation..."

# Set environment for testing
export OPENAI_API_KEY="test-key"

# Run comprehensive validation (skip E2E by default)
if SKIP_E2E=true ./scripts/validate.sh; then
    echo "✅ Pre-push validation passed"
    exit 0
else
    echo "❌ Pre-push validation failed"
    echo "💡 Fix the issues above before pushing"
    exit 1
fi
EOF

# Create commit-msg hook for conventional commits
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash

# Tide commit message validation
# Ensures commit messages follow conventional commit format

commit_regex='^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ Invalid commit message format"
    echo ""
    echo "Commit messages should follow conventional commit format:"
    echo "  type(scope): description"
    echo ""
    echo "Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert"
    echo "Examples:"
    echo "  feat: add user authentication"
    echo "  fix(ui): resolve button alignment issue"
    echo "  docs: update installation guide"
    echo ""
    exit 1
fi
EOF

# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
chmod +x .git/hooks/commit-msg

echo -e "${GREEN}✅ Git hooks installed successfully!${NC}\n"

echo -e "${BLUE}Hooks installed:${NC}"
echo "  • pre-commit  - Quick validation before commits"
echo "  • pre-push    - Full validation before pushing"
echo "  • commit-msg  - Conventional commit format validation"
echo ""

echo -e "${YELLOW}To skip hooks temporarily:${NC}"
echo "  git commit --no-verify"
echo "  git push --no-verify"
echo ""

echo -e "${BLUE}Test the setup:${NC}"
echo "  ./scripts/quick-check.sh      # Quick validation"
echo "  ./scripts/validate.sh         # Full validation"
echo ""