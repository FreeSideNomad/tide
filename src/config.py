import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://username:password@localhost:5432/tide_db"
)

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback"
)

# Session Configuration
SESSION_SECRET_KEY = os.getenv(
    "SESSION_SECRET_KEY", "your-secret-key-change-in-production"
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Application Configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


class Config:
    """Configuration class for Tide application."""

    # Database Configuration
    DATABASE_URL = DATABASE_URL
    DEBUG_MODE = DEBUG

    # OAuth Configuration
    GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET = GOOGLE_CLIENT_SECRET
    GOOGLE_REDIRECT_URI = GOOGLE_REDIRECT_URI

    # Session Configuration
    SESSION_SECRET_KEY = SESSION_SECRET_KEY
    REDIS_URL = REDIS_URL

    # Application Configuration
    ENVIRONMENT = ENVIRONMENT
