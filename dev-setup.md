# Development Setup Guide

This guide will help you set up the development environment for the Tide DBT AI Assistant.

## Prerequisites

- Python 3.9 or higher
- Git
- uv package manager
- PostgreSQL (for production database)

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

### 4. Database Setup (Optional for initial development)

For local development with PostgreSQL:

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

```bash
# Run the Flet application
uv run flet run

# Or run directly
uv run python src/main.py
```

## Development Commands

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_example.py
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
├── src/                    # Source code
│   ├── main.py            # Main application entry point
│   ├── config.py          # Configuration management
│   └── assets/            # Static assets (images, icons)
├── tests/                 # Test files (to be created)
├── docs/                  # Documentation
│   └── wiki/             # Git submodule for project wiki
├── .env.example          # Example environment variables
├── .env                  # Local environment variables (not in git)
├── pyproject.toml        # Project configuration and dependencies
└── dev-setup.md          # This file
```

## Technology Stack

- **Frontend Framework**: Flet (Python-based cross-platform UI)
- **Database**: PostgreSQL with pgvector extension
- **ORM**: SQLAlchemy
- **AI Integration**: OpenAI API
- **Testing**: pytest with coverage
- **Code Quality**: black (formatting) + ruff (linting)
- **Package Management**: uv

## Development Workflow

1. **Make changes** to source code in `src/`
2. **Run tests** to ensure functionality: `uv run pytest`
3. **Format code**: `uv run black src/`
4. **Check linting**: `uv run ruff check src/`
5. **Test the app**: `uv run flet run`
6. **Commit changes** following project guidelines

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY environment variable is required"**
   - Make sure you've set the `OPENAI_API_KEY` environment variable
   - Check that your `.env` file is properly configured

2. **Database connection errors**
   - Ensure PostgreSQL is running
   - Verify the `DATABASE_URL` in your environment

3. **Import errors**
   - Make sure you're using `uv run` to execute commands
   - Verify all dependencies are installed: `uv sync`

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