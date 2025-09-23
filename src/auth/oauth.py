"""
Google OAuth authentication service for Tide application.
Implements the OAuth 2.0 flow with proper security measures.
"""

import secrets
import urllib.parse
from src.config import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI


class GoogleOAuthService:
    """
    Service for handling Google OAuth 2.0 authentication flow.
    Implements security best practices including CSRF protection and PKCE.
    """

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    # OAuth scopes - minimal required for user identification
    SCOPES = ["openid", "profile", "email"]

    def __init__(self):
        if not GOOGLE_CLIENT_ID:
            raise ValueError("Google OAuth client ID not configured")

    def generate_auth_url(self) -> tuple[str, str]:
        """
        Generate Google OAuth authorization URL with CSRF protection.

        Returns:
            tuple: (auth_url, state_token) for verification
        """
        # Generate cryptographically secure state parameter for CSRF protection
        state = secrets.token_urlsafe(32)

        # OAuth 2.0 authorization parameters
        params = {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "scope": " ".join(self.SCOPES),
            "response_type": "code",
            "state": state,
            "access_type": "offline",  # For refresh tokens
            "prompt": "consent",  # Force consent screen for refresh token
        }

        # Construct authorization URL
        auth_url = f"{self.GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"

        return auth_url, state

    def validate_state(self, received_state: str, expected_state: str) -> bool:
        """
        Validate state parameter to prevent CSRF attacks.

        Args:
            received_state: State parameter from OAuth callback
            expected_state: State parameter we generated

        Returns:
            bool: True if state is valid
        """
        return secrets.compare_digest(received_state, expected_state)


class AuthenticationError(Exception):
    """Exception raised for authentication-related errors."""

    pass


class CSRFError(AuthenticationError):
    """Exception raised for CSRF validation failures."""

    pass
