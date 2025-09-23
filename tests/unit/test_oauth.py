"""
Unit tests for Google OAuth authentication service.
Tests the OAuth flow logic, security measures, and error handling.
"""

import pytest
import urllib.parse
from unittest.mock import patch

from src.auth.oauth import GoogleOAuthService, AuthenticationError, CSRFError


class TestGoogleOAuthService:
    """Test cases for GoogleOAuthService."""

    def setup_method(self):
        """Set up test fixtures."""
        with patch("src.auth.oauth.GOOGLE_CLIENT_ID", "test_client_id"):
            self.oauth_service = GoogleOAuthService()

    def test_initialization_success(self):
        """Test successful OAuth service initialization."""
        with patch("src.auth.oauth.GOOGLE_CLIENT_ID", "test_client_id"):
            service = GoogleOAuthService()
            assert service is not None

    def test_initialization_missing_client_id(self):
        """Test OAuth service initialization fails without client ID."""
        with patch("src.auth.oauth.GOOGLE_CLIENT_ID", None):
            with pytest.raises(
                ValueError, match="Google OAuth client ID not configured"
            ):
                GoogleOAuthService()

    def test_generate_auth_url_format(self):
        """Test that generated auth URL has correct format and parameters."""
        with patch("src.auth.oauth.GOOGLE_CLIENT_ID", "test_client_id"):
            service = GoogleOAuthService()
            auth_url, state = service.generate_auth_url()

            # Parse URL and query parameters
            parsed_url = urllib.parse.urlparse(auth_url)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            # Verify base URL
            assert parsed_url.scheme == "https"
            assert parsed_url.netloc == "accounts.google.com"
            assert parsed_url.path == "/o/oauth2/v2/auth"

            # Verify required parameters
            assert query_params["client_id"][0] == "test_client_id"
            assert query_params["response_type"][0] == "code"
            assert query_params["state"][0] == state
            assert "openid" in query_params["scope"][0]
            assert "profile" in query_params["scope"][0]
            assert "email" in query_params["scope"][0]

    def test_generate_auth_url_state_uniqueness(self):
        """Test that each call generates a unique state parameter."""
        _, state1 = self.oauth_service.generate_auth_url()
        _, state2 = self.oauth_service.generate_auth_url()

        assert state1 != state2
        assert len(state1) > 0
        assert len(state2) > 0

    def test_validate_state_success(self):
        """Test successful state validation."""
        test_state = "test_state_token"
        assert self.oauth_service.validate_state(test_state, test_state) is True

    def test_validate_state_failure(self):
        """Test state validation failure with different tokens."""
        state1 = "test_state_token_1"
        state2 = "test_state_token_2"
        assert self.oauth_service.validate_state(state1, state2) is False

    def test_validate_state_empty_strings(self):
        """Test state validation with empty strings."""
        assert self.oauth_service.validate_state("", "") is True

    def test_oauth_scopes_are_minimal(self):
        """Test that OAuth scopes are minimal and appropriate."""
        expected_scopes = {"openid", "profile", "email"}
        actual_scopes = set(self.oauth_service.SCOPES)
        assert actual_scopes == expected_scopes

    def test_oauth_urls_are_correct(self):
        """Test that OAuth URLs point to correct Google endpoints."""
        assert (
            self.oauth_service.GOOGLE_AUTH_URL
            == "https://accounts.google.com/o/oauth2/v2/auth"
        )
        assert (
            self.oauth_service.GOOGLE_TOKEN_URL == "https://oauth2.googleapis.com/token"
        )
        assert (
            self.oauth_service.GOOGLE_USERINFO_URL
            == "https://www.googleapis.com/oauth2/v2/userinfo"
        )


class TestAuthenticationErrors:
    """Test cases for authentication error classes."""

    def test_authentication_error_inheritance(self):
        """Test AuthenticationError inherits from Exception."""
        error = AuthenticationError("test message")
        assert isinstance(error, Exception)
        assert str(error) == "test message"

    def test_csrf_error_inheritance(self):
        """Test CSRFError inherits from AuthenticationError."""
        error = CSRFError("csrf test message")
        assert isinstance(error, AuthenticationError)
        assert isinstance(error, Exception)
        assert str(error) == "csrf test message"
