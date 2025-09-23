# Claude Code Notes

## Project Info

**Tide** is a Python Flet application targeting mobile and web users. This is a safety-first DBT (Dialectical Behavior Therapy) AI assistant designed to guide individuals through DBT skills development using structured decision-tree architecture rather than open-ended chat.

### Technology Stack
- **Python Flet**: Cross-platform framework for mobile and web deployment
- **Target Platforms**: Mobile (iOS/Android) and web browsers
- **Architecture**: Safety-constrained decision trees with NLP enhancement for personalization

### Core Features
- Evidence-based DBT skill delivery through structured pathways
- Crisis detection with safety plan integration
- Four DBT modules: Mindfulness, Distress Tolerance, Emotion Regulation, Interpersonal Effectiveness
- Safety-first design prioritizing user wellbeing over engagement metrics

## Wiki Documentation

The project wiki is integrated as a git submodule at `docs/wiki/`. This provides direct access to all wiki content within the repository.

### Updating Wiki Content

To pull the latest wiki changes:
```bash
git submodule update --remote docs/wiki
```

### Wiki Files

Wiki content is directly accessible in the `docs/wiki/` directory:
- `docs/wiki/vision.md` - Complete project vision and business requirements
- `docs/wiki/dbt-ai-assistant-brainstorm.md` - Design decisions and technical brainstorming

### Key Business Requirements (from docs/wiki/vision.md)
- **BR-1**: Safety-First Architecture - Crisis detection with human escalation
- **BR-2**: Evidence-Based DBT Skill Delivery - Structured decision trees only
- **BR-3**: Human Oversight Integration - 24/7 advisor availability
- **BR-4**: Transparent AI Limitations - Clear disclaimers and boundaries
- **BR-5**: Crisis Detection and Response - Multi-layered safety systems

### Design Principles (from docs/wiki/dbt-ai-assistant-brainstorm.md)
- Decision tree primary architecture with NLP enhancement
- Standalone tool for users without therapy access
- Safety plan integration required during registration
- No direct counseling - guides to pre-established resources
- Maladaptive pattern detection using keyword matching

The wiki repository URL: https://github.com/FreeSideNomad/tide/wiki

## Critical Development Process

**🚨 MANDATORY: NO CODE WITHOUT EXPLICIT STAKEHOLDER APPROVAL**

### 4-Phase Development Workflow

**Phase 1: Planning & Collaboration**
1. Collaborate on .md files (documentation and requirements)
2. Stakeholder review and feedback on .md files
3. **Wait for explicit approval** before proceeding

**Phase 2: Issue Creation**
4. Create GitHub Issues (Epic, Feature, User Story) based on approved .md files
5. Issue-driven development approach

**Phase 3: Implementation Cycle (Per User Story)**
6. **Get explicit approval** for each user story before starting
7. Create feature branch for specific user story
8. Implement & test until all tests pass
9. Commit & merge to remote main, fix build issues

**Phase 4: Validation & Iteration**
10. Stakeholder manual testing
11. Create GitHub issues for problems found
12. Fix & merge code
13. Repeat until user story complete
14. Move to next user story only after completion

### Essential Rules
- ✅ Collaborate on .md files freely
- ❌ Never implement code without explicit stakeholder approval
- ❌ Never create GitHub issues without approved requirements
- ❌ Never merge code without passing tests and build validation

## Technology Stack

### Approved Technologies
- **Frontend**: Python Flet for cross-platform mobile and web deployment
- **Database**: PostgreSQL with pgvector for RAG storage
- **ORM**: SQLAlchemy for maintainability and type safety
- **AI Integration**: OpenAI API with cost management
- **Authentication**: Google OAuth or Microsoft OAuth
- **Package Management**: uv for fast Python dependency management
- **Testing**: Pytest with comprehensive test suite (unit, integration, E2E)
- **Code Quality**: Black (formatting), Ruff (linting), Safety (security), Bandit (security)
- **Browser Testing**: Selenium and Playwright for E2E automation
- **Containerization**: Docker and Docker Compose for development and testing
- **CI/CD**: GitHub Actions with comprehensive pipeline
- **Development Automation**: Makefile and shell scripts for workflow automation
- **Git Integration**: Pre-commit hooks for quality gates
- **Deployment**: GitHub Actions + cloud provider

### Technology Guidelines
1. **Simplicity over sophistication** - choose boring, proven technologies
2. **GitHub integration** - prioritize tools that work well with GitHub
3. **User experience** - optimize for end-user productivity
4. **Testing support** - ensure technologies support automated testing
5. **AI integration** - consider how well tools work with LLM APIs

## Architecture Principles

### 1. Domain-First Architecture
- Core business domain comes first
- Supporting domains (auth, user management) come later
- Start with business entity modeling
- Define core use cases before technical infrastructure
- Defer authentication until business logic is validated

### 2. GitHub-Native Development
- Use GitHub as single source of truth for all project artifacts
- Vision and context in GitHub Wiki
- Work tracking through GitHub Issues
- Project management via GitHub Projects
- Code in GitHub repositories
- Automation through GitHub Actions

### 3. User-Centric Validation
- Validate every significant decision with users before implementation
- Present plans as GitHub Issues for review
- Create UI mocks in structured format (Markdown/YAML) before coding
- Implement feedback loops at every stage
- Prioritize user experience over technical elegance

### 4. Essential Use Cases Methodology
- Follow Alistair Cockburn's Essential Use Cases approach
- Start with essential user goals and intentions
- Avoid technical implementation details initially
- Focus on "what" before "how"
- Progressive refinement through structured formats

## Database Architecture

### PostgreSQL Setup
- **Primary Database**: PostgreSQL for all structured data
- **Vector Storage**: pgvector extension for RAG capabilities
- **Conversation Storage**: Full conversation logging and context
- **ORM**: SQLAlchemy for database operations
- **Migrations**: Alembic for database schema management

### Data Storage Strategy
- Conversational data in PostgreSQL tables
- Vector embeddings in pgvector for similarity search
- Document storage in GitHub (prefer github wiki) with version control. Current versions of documents also stored in RAG vectors in PostgreSQL

## Quality Standards

### Code Quality
- **Test Coverage**: Minimum 90% for business logic with pytest unit and integration tests, 90% of code lines, branches
- **Code Review**: All changes require review via GitHub PR
- **Documentation**: Every public API documented
- **Performance**: Response times under 2 seconds for user interactions

### Development Quality
- **Linting**: Follow Python black formatting
- **Type Hints**: Use type annotations for better maintainability
- **Error Handling**: Comprehensive error handling and logging
- **Security**: Never expose secrets or API keys

## AI Integration Guidelines

### OpenAI API Usage
- **Cost Management**: Monitor token usage and implement rate limiting
- **Error Handling**: Graceful degradation when API unavailable
- **Context Management**: Efficient prompt engineering for cost control
- **Security**: Secure API key storage and usage patterns

### Conversation Management
- **Logging**: Full conversation audit trail in PostgreSQL
- **Context**: Dynamic context retrieval for relevant responses
- **Privacy**: Secure handling of conversation data
- **Performance**: Optimize for response time and user experience

## Common Pitfalls to Avoid

### Process Violations
1. **Skipping Vision/Requirements Phase**: Never implement without consulting essential use cases
2. **No UI Design Consultation**: Create mockups before any UI implementation
3. **Feature Creep**: Validate business need before adding features
4. **Violating Domain-First Principle**: Start with core business domain, not UI/infrastructure

### Technical Mistakes
1. **Premature Optimization**: Focus on working functionality first
2. **Over-Engineering**: Keep solutions simple and maintainable
3. **Ignoring Test Coverage**: Maintain quality standards from the start
4. **Security Oversights**: Follow security best practices consistently

## Remember

**"Start simple, validate early, iterate based on feedback, and let the business domain drive technical decisions."**

Always prioritize:
1. User needs over technical elegance
2. Working software over perfect documentation
3. Stakeholder feedback over assumptions
4. Domain modeling over technical implementation
5. Security and quality over speed of delivery

## Flet Testing Guidelines

### Testing Strategy for Flet Applications
- **Business Logic Separation**: Extract application logic into separate functions/classes that can be unit tested independently of Flet UI components
- **Unit Testing**: Test individual functions, event handlers, state management, data processing, and validation logic using pytest
- **Integration Testing**: Test component interactions, page navigation, state updates, and data flow between components
- **Test Structure**: Organize tests following pytest conventions with `test_*.py` naming and proper fixture usage

### Pytest Configuration
- Follow pytest conventions for Python test discovery
- Use fixtures for managing test dependencies and state
- Implement parametrization to avoid redundant test code
- Generate test coverage reports for quality assurance
- Integrate with GitHub Actions for continuous integration

### Testing Best Practices
- Separate UI code from business logic for effective testing
- Test event handlers and state management functions independently
- Use mocking for external dependencies
- Maintain high test coverage for core application functionality
- Follow standard Python testing practices adapted for Flet applications

## Development Workflow and Automation

### Local Development Tools

The project includes comprehensive automation tools for consistent development experience:

#### Makefile Commands
Use `make` for all common development tasks:

```bash
# Essential workflow commands
make help           # Show all available commands
make install        # Install dependencies with uv
make setup-hooks    # Configure Git hooks (one-time setup)

# Development cycle
make dev            # Start development server (Flet web mode)
make dev-docker     # Start full stack with Docker Compose

# Code quality (run frequently)
make quick-check    # Fast validation (~10 seconds)
make format         # Auto-format code with black
make lint           # Check with ruff linter
make lint-fix       # Auto-fix linting issues

# Testing
make test-unit      # Unit tests only
make test-int       # Integration tests (requires Docker)
make test-e2e       # End-to-end browser tests
make coverage       # Test coverage report

# Comprehensive validation
make validate       # Full validation before commits
make ci             # Simulate CI pipeline
```

#### Validation Scripts

**Quick Check** (`./scripts/quick-check.sh` or `make quick-check`):
- Fast feedback loop for active development (~10 seconds)
- Code formatting, basic linting, imports, essential tests
- Run frequently during development

**Full Validation** (`./scripts/validate.sh` or `make validate`):
- Comprehensive checks before committing (2-5 minutes)
- Code quality, security scanning, all test types, coverage analysis
- Matches CI pipeline requirements

**Environment Setup** (`./scripts/dev-setup.sh`):
- One-command setup for new developers
- Installs uv, configures environment, sets up Git hooks
- Validates setup and provides next steps

### Git Hooks Integration

Automated quality gates prevent issues from reaching the repository:

#### Pre-commit Hook
- **Trigger**: Before each `git commit`
- **Action**: Runs `quick-check.sh` for fast validation
- **Purpose**: Catch basic issues immediately
- **Bypass**: `git commit --no-verify` (use sparingly)

#### Pre-push Hook
- **Trigger**: Before `git push` to remote
- **Action**: Runs full validation (excluding E2E tests)
- **Purpose**: Ensure comprehensive quality before sharing code
- **Bypass**: `git push --no-verify` (use sparingly)

#### Commit Message Hook
- **Trigger**: During commit message creation
- **Action**: Validates conventional commit format
- **Required Format**: `type(scope): description`
- **Examples**:
  - `feat: add user authentication`
  - `fix(ui): resolve button alignment issue`
  - `docs: update installation guide`

### Recommended Development Workflow

#### 1. Initial Setup (One-time)
```bash
./scripts/dev-setup.sh     # Automated setup
# OR manually:
make install
make setup-hooks
cp .env.example .env       # Add your OPENAI_API_KEY
```

#### 2. Daily Development Cycle
```bash
# Start development
make dev                   # Flet development server
# OR
make dev-docker           # Full stack with PostgreSQL

# Make code changes...

# Quick validation (run frequently)
make quick-check          # ~10 seconds feedback

# Continue development...
```

#### 3. Before Committing
```bash
# Comprehensive validation
make validate             # 2-5 minutes, matches CI

# If validation passes:
git add .
git commit -m "feat: implement new feature"  # Hooks run automatically
```

#### 4. Before Pushing
```bash
# Optional: simulate CI pipeline
make ci

# Push (hooks run automatically)
git push origin feature-branch
```

### Docker Integration

All tools automatically detect Docker availability:

**With Docker Available**:
- Full integration tests with PostgreSQL
- E2E tests with browser automation
- Containerized build validation
- Complete CI pipeline simulation

**Without Docker**:
- Graceful degradation with warnings
- Unit tests and code quality checks still run
- Local-only validation mode

### Code Quality Standards

#### Automated Enforcement
- **Black**: Code formatting (zero configuration)
- **Ruff**: Fast Python linter with auto-fix
- **Safety**: Dependency vulnerability scanning
- **Bandit**: Security linting for common issues
- **Pytest**: Test execution with coverage reporting

#### Coverage Requirements
- **Minimum**: 80% line and branch coverage
- **Target**: 90% for business logic
- **Measurement**: Unit tests only (integration tests separate)
- **Reporting**: HTML and XML formats generated

#### Security Scanning
- **Dependency vulnerabilities**: `safety` check against known CVEs
- **Code security**: `bandit` static analysis for security anti-patterns
- **API key protection**: Automated detection of exposed secrets
- **CI integration**: Security scans run on every PR

### Troubleshooting Development Issues

#### Common Commands for Issue Resolution
```bash
# Fix formatting and linting
make format && make lint-fix

# Clean environment and rebuild
make clean && make install

# Test specific components
make test-unit              # Fast unit tests
uv run pytest tests/unit/test_config.py -v  # Specific test file

# Debug failed validation
./scripts/validate.sh --skip-e2e  # Skip slow E2E tests
```

#### Bypass Hooks When Needed
```bash
# Emergency commits (use sparingly)
git commit --no-verify -m "fix: urgent hotfix"
git push --no-verify
```

### Integration with IDE

The validation tools integrate with common IDEs:

- **VS Code**: Works with Python extension, pytest integration
- **PyCharm**: Compatible with built-in test runners and code inspection
- **Command Line**: Full functionality via terminal/shell

All tools use standard Python tooling conventions for maximum compatibility.