# Claude Code Notes

## Project Info

**Tide** is a Python Flet application targeting mobile and web users. This is a safety-first DBT (Dialectical Behavior Therapy) AI assistant designed to guide individuals through DBT skills development using structured decision-tree architecture rather than open-ended chat.

### Technology Stack
- **Python Flet**: Cross-platform framework for mobile and web deployment
- **Target Platforms**: Mobile (iOS/Android) and web browsers prioritizing mobile-first design
- **Architecture**: Safety-constrained decision trees with NLP enhancement for personalization
- **Decision Tree Implementation**: JSON structure with rule engine for crisis detection and skill selection


### Core Features
- **Evidence-based DBT skill delivery** through structured decision pathways (not chat)
- **Four DBT modules**: Mindfulness, Distress Tolerance, Emotion Regulation, Interpersonal Effectiveness
- **Safety-first design** prioritizing user wellbeing over engagement metrics or feature completeness
- **Structured decision trees** with predetermined safe pathways and NLP personalization
- **Crisis survival skills** focus with immediate safety plan activation for 8+ intensity or crisis keywords
- **Human oversight integration** with seamless handoff protocols for flagged situations

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
- `docs/wiki/canadian-mental-health-ai-regulatory-framework.md` - Canadian legal and ethical considerations
- `docs/wiki/dbt-distress-tolerance-tree.md` - Detailed distress tolerance decision tree architecture

### Target Users (from docs/wiki/vision.md)

**Primary Users:**
1. Individuals seeking DBT skills without access to therapy
2. Crisis prevention users needing evidence-based techniques during distress
3. Skill practice users supplementing existing therapy
4. Self-help seekers building emotional regulation and interpersonal skills

**Secondary Users:**
1. Mental health professionals referencing the tool as therapy supplement
2. Human advisors providing oversight and escalation support
3. Crisis counselors receiving escalated cases
4. Researchers studying AI-assisted skill development

### Key Business Requirements (from docs/wiki/vision.md)
- **BR-1**: Safety-First Architecture - Crisis detection with human escalation protocols
- **BR-2**: Evidence-Based DBT Skill Delivery - Structured decision trees only, no open-ended chat
- **BR-3**: Human Oversight Integration - 24/7 advisor availability for critical situations
- **BR-4**: Transparent AI Limitations - Clear disclaimers about therapy replacement boundaries
- **BR-5**: Crisis Detection and Response - Multi-layered safety systems with immediate escalation
- **BR-6**: Structured Decision Architecture - Predetermined pathways within safety constraints

### Safety-First Design Principles (from docs/wiki/dbt-ai-assistant-brainstorm.md)
- **Decision tree primary architecture** with NLP enhancement for personalization only
- **Standalone tool** for users without therapy access
- **Safety plan integration** required during registration before any skill access
- **No direct counseling** - guides to pre-established user resources
- **Crisis survival skills** focus with safety plan activation protocols
- **Maladaptive pattern detection** using keyword matching ("always", "never", "everyone", "no one")
- **Fact vs. perception awareness** - distinguish objective circumstances from emotional interpretations

### Clinical Evidence Base (from docs/wiki/dbt-ai-assistant-brainstorm.md)
- **8 high-quality RCTs** confirm DBT effectiveness
- **Low dropout rate** (27.3%) with moderate effect sizes
- **DBT skills are key mechanism** of change for suicide attempts, NSSI, depression, anger
- **Stand-alone training** growing evidence for transdiagnostic treatment
- **Safety planning reduces** suicidal behavior risk by 45%

### Canadian Regulatory Context (from docs/wiki/canadian-mental-health-ai-regulatory-framework.md)
- **PIPEDA compliance** required for mental health data handling
- **Provincial health information acts** apply across different provinces
- **Bill C-27/AIDA** (proposed) classifies crisis detection as high-impact AI system
- **Health Canada SaMD** classification considerations for crisis features
- **Indigenous data sovereignty** and cultural adaptation requirements
- **Ethical framework alignment** with Canadian AI Ethics Guidelines

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
- **Session Management**: Redis for session state and caching
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

## Domain Model

The application follows Domain-Driven Design (DDD) principles with a comprehensive domain model that serves as the foundation for all implementation work. The domain model establishes ubiquitous language and bounded contexts used across all epics, features, and user stories.

**Domain Model Location**: `docs/wiki/domain-model.md`

### Domain-Driven Design Approach
- **Bounded Contexts**: User Management, Questionnaire, DBT Skills (future), Safety (future)
- **Aggregate Design**: User aggregate owns responses; Question aggregate manages questionnaire structure
- **Ubiquitous Language**: All team communication uses domain model terminology
- **Domain Events**: Track important business events across aggregate boundaries
- **Repository Pattern**: Encapsulates data access and maintains domain integrity

### Key Domain Principles
- **User-Centric Design**: User aggregate is the primary root containing responses and preferences
- **Flexible Questionnaire**: Single questionnaire with deprecated/active questions rather than versioning
- **Session Separation**: Authentication tokens and temporary state stored in Redis, not domain model
- **Eventual Consistency**: New questions automatically become pending for all existing users

## Architecture Principles

### 1. Safety-First Architecture (Overrides All Other Principles)
- **User safety prioritized** over feature completeness, engagement, or technical elegance
- **Crisis detection algorithms** with immediate human escalation triggers
- **Evidence-based responses only** with clear citations and disclaimers
- **Fail-safe mechanisms** when AI confidence levels are insufficient
- **Complete audit trail** of all user interactions for safety monitoring
- **Multi-layer validation** before any AI-generated content reaches users

### 2. Domain-First Architecture
- **Core DBT business domain** comes first (Distress Tolerance MVP)
- Supporting domains (auth, user management) come later
- Start with **safety plan registration** before any skill access
- Define **crisis survival use cases** before technical infrastructure
- Defer authentication until **core safety features** are validated

### 3. GitHub-Native Development
- Use GitHub as single source of truth for all project artifacts
- Vision and context in GitHub Wiki
- Work tracking through GitHub Issues
- Project management via GitHub Projects
- Code in GitHub repositories
- Automation through GitHub Actions

### 4. User-Centric Validation
- Validate every significant decision with users before implementation
- Present plans as GitHub Issues for review
- Create UI mocks in structured format (Markdown/YAML) before coding
- Implement feedback loops at every stage
- **Prioritize user safety** over user experience preferences

### 5. Essential Use Cases Methodology
- Follow Alistair Cockburn's Essential Use Cases approach
- Start with essential user goals and intentions (crisis survival)
- Avoid technical implementation details initially
- Focus on "what" before "how"
- Progressive refinement through structured formats

### 6. Evidence-Based Content Management
- **All content sourced** from published DBT research and clinical guidelines
- **Version control** for all therapeutic content with clinical review requirements
- **Standardized response templates** based on validated interventions
- **Regular content audits** by qualified mental health professionals
- **Clear attribution** and citation for all therapeutic recommendations

## Database and Session Architecture

### PostgreSQL Setup
- **Primary Database**: PostgreSQL for all persistent domain data
- **Vector Storage**: pgvector extension for RAG capabilities
- **Conversation Storage**: Full conversation logging and context
- **ORM**: SQLAlchemy for database operations
- **Migrations**: Alembic for database schema management

### Redis Session Management
- **Session Storage**: Redis for user session state and authentication tokens
- **Caching Layer**: Application-level caching for frequently accessed data
- **Session Expiration**: Automatic cleanup of expired sessions
- **Scalability**: Horizontal scaling support for session management
- **Performance**: Fast in-memory operations for session data

### Data Storage Strategy
- **Persistent Domain Data**: User profiles, questionnaire responses, preferences in PostgreSQL
- **Session State**: Authentication tokens, temporary user state in Redis
- **Conversational Data**: Full conversation logs in PostgreSQL tables
- **Vector Embeddings**: pgvector for similarity search and RAG capabilities
- **Document Storage**: GitHub wiki with version control, current versions in RAG vectors
- **Cache Strategy**: Frequently accessed data cached in Redis with TTL

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

## Safety-First Development Principles

**"Safety first, evidence-based, transparent limitations, with seamless human oversight."**

Always prioritize:
1. **User safety** over all other considerations (features, engagement, technical elegance)
2. **Evidence-based DBT content** over innovative but unvalidated approaches
3. **Crisis detection accuracy** over feature completeness
4. **Transparent AI limitations** over user engagement optimization
5. **Human oversight integration** over autonomous AI decision-making
6. **Structured decision pathways** over conversational AI flexibility

## Crisis Detection and Safety Requirements

### Crisis Detection Triggers
- **Intensity Level 8+** (on 1-10 scale) triggers safety plan activation
- **Crisis keywords** (self-harm, suicidal ideation) bypass normal flow
- **Maladaptive language patterns** ("always", "never", "everyone", "no one") flagged
- **System uncertainty** about appropriate skills triggers human escalation

### Safety Plan Integration
- **Required during registration** before accessing any skills
- **Rutgers DBT Adult Crisis Plan** template as foundation
- **Warning signs and coping strategies** required (minimum 1 and 3 respectively)
- **Support contacts** highly recommended but not blocking
- **Crisis activation** bypasses decision tree and goes directly to safety plan

### Clinical Validation Requirements
- Each decision point must reference **DBT literature**
- Skill recommendations must follow **evidence-based protocols**
- Crisis detection must meet **clinical safety standards**
- Coaching content must align with **DBT therapy principles**

## Distress Tolerance Module (MVP Focus)

### Core Skills (Evidence-Based)
- **TIPP**: Temperature, Intense Exercise, Paced Breathing, Paired Muscle Relaxation
- **STOP**: Stop, Take a step back, Observe, Proceed with wise mind
- **Distraction**: Various techniques based on context and preferences
- **Self-Soothing**: Sensory-based coping strategies
- **IMPROVE**: Imagery, Meaning, Prayer, Relaxation, One thing, Vacation, Encouragement

### Decision Tree Structure (from docs/wiki/dbt-distress-tolerance-tree.md)
1. **Crisis check** (intensity 8+ or keywords) → Safety plan
2. **Situation assessment** (impulsive urges, emotional overwhelm, physical crisis, mixed)
3. **Context refinement** (time available, privacy, past successful skills)
4. **Specific skill recommendation** with context-aware coaching
5. **Post-skill assessment** and follow-up guidance

### Skill Personalization
- **DBT experience** assessment
- **Physical limitations** and accessibility needs
- **Environment considerations** (work, home, public)
- **Preference tracking** (movement vs. stillness, duration preferences)
- **Success tracking** for future recommendations

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

## Current CI/CD Status

### ✅ Passing GitHub Actions Jobs (4/4 Active)
- **Code Quality**: Black formatting, Ruff linting ✅
- **Unit Tests**: 14/14 unit tests passing ✅
- **Integration Tests**: Database and OpenAI API integration ✅
- **Security Scanning**: Safety, Bandit, CodeQL ✅

### 🚧 Temporarily Disabled Jobs (For Troubleshooting)
- **End-to-End Tests**: Browser testing with Selenium/Playwright (commented out)
- **Docker Build & Test**: Containerized testing (commented out)

### Issues Under Investigation
1. **Docker Build Timeouts**: Container builds hanging in GitHub Actions environment
2. **E2E Test Timing**: Flet app rendering detection issues with browser automation
3. **Resource Constraints**: GitHub Actions runners struggling with complex Docker operations

### Local Development Status
- **95% test coverage** maintained ✅
- **100% code quality compliance** ✅
- **All core validations working** ✅
- **Git hooks functional** ✅
- **Docker/E2E tests temporarily disabled** for troubleshooting ⚠️

### Validation Tools Status
- ✅ **Local Git Hooks**: Pre-commit and pre-push validation working
- ✅ **Security Scanning**: No vulnerabilities found
- ✅ **Code Quality**: 100% formatting and linting compliance
- ✅ **Unit Test Coverage**: All core functionality tested