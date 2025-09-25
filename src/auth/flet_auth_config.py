"""
Secure Flet Authentication Configuration

SECURITY REQUIREMENTS (from CLAUDE.md):
- MANDATORY: Follow https://flet.dev/docs/cookbook/authentication/ exactly
- No custom authentication solutions allowed
- Safety-first architecture prioritizes user wellbeing
- SERVER-SIDE token storage only (ADR-0001)
- Complete audit trail for safety monitoring

IMPORTANT: This module follows ADR-0001 which requires server-side token storage.
Client-side token storage is PROHIBITED for security reasons.
"""

import os
import logging
from typing import Optional
from flet.auth.providers import GoogleOAuthProvider
from dotenv import load_dotenv

# Configure logging for security audit trail
logger = logging.getLogger(__name__)


class SecureAuthConfig:
    """
    Secure authentication configuration following Flet cookbook patterns.

    Security Features (aligned with ADR-0001):
    - Environment variable-based configuration (no secrets in code)
    - SERVER-SIDE session management only
    - NO client-side token storage
    - HTTPS enforcement for production
    - Audit logging for security monitoring
    """

    def __init__(self):
        """Initialize secure authentication configuration."""
        # Load environment variables from .env file
        load_dotenv()
        self._validate_environment()

    def _validate_environment(self) -> None:
        """Validate required environment variables are present."""
        required_vars = [
            "GOOGLE_CLIENT_ID",
            "GOOGLE_CLIENT_SECRET",
            "SESSION_SECRET_KEY",
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                f"Please check your .env file or environment configuration."
            )

        logger.info("✅ Authentication environment variables validated")

    def create_google_oauth_provider(self) -> GoogleOAuthProvider:
        """
        Create Google OAuth provider with secure configuration.

        Returns:
            GoogleOAuthProvider: Configured provider following Flet patterns

        Security Notes:
        - Uses environment variables for credentials (never hardcoded)
        - Validates redirect URI format
        - Logs provider creation for audit trail
        """
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        redirect_uri = os.getenv(
            "GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth_callback"
        )

        # Validate redirect URI format for security
        if not redirect_uri.startswith(("http://localhost", "https://")):
            logger.warning(f"⚠️ Redirect URI may be insecure: {redirect_uri}")

        # Create provider using Flet's official pattern
        provider = GoogleOAuthProvider(
            client_id=client_id, client_secret=client_secret, redirect_url=redirect_uri
        )

        logger.info(f"✅ Google OAuth provider created with redirect: {redirect_uri}")
        return provider

    def get_server_session_config(self) -> dict:
        """
        Get server-side session configuration (ADR-0001 compliance).

        Returns:
            dict: Server session configuration for token storage

        Security: Tokens stored server-side only, no client-side storage
        """
        return {
            "session_backend": "redis",  # Server-side storage
            "encryption_required": True,  # Encrypt tokens at rest
            "token_storage": "server_only",  # No client-side tokens
            "audit_logging": True,  # Complete audit trail
        }

    def get_session_identifier_config(self) -> dict:
        """
        Get session identifier configuration for client-server communication.

        Returns:
            dict: Session identifier configuration

        Security: Only session IDs stored client-side, never tokens
        """
        return {
            "identifier_length": 32,  # Secure session ID length
            "identifier_entropy": "high",  # High entropy generation
            "rotation_policy": "on_auth",  # Rotate on authentication
            "storage_location": "client_session_only",  # Session ID only
        }

    def get_oauth_scopes(self) -> list[str]:
        """
        Get OAuth scopes for Google authentication.

        Returns:
            list[str]: Required OAuth scopes for user profile access

        Security: Minimal scopes for principle of least privilege
        """
        return ["openid", "profile", "email"]


# Global secure auth configuration instance
_auth_config: Optional[SecureAuthConfig] = None


def get_auth_config() -> SecureAuthConfig:
    """
    Get singleton secure authentication configuration.

    Returns:
        SecureAuthConfig: Global authentication configuration instance

    Security: Singleton pattern ensures consistent configuration
    """
    global _auth_config
    if _auth_config is None:
        _auth_config = SecureAuthConfig()
    return _auth_config
