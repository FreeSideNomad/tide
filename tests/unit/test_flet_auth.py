"""
Unit tests for Flet authentication components.

Tests secure authentication implementation following Flet cookbook patterns.
"""

import pytest
import os
import json
from unittest.mock import patch, Mock, MagicMock
import flet as ft
from cryptography.fernet import Fernet

# Import authentication components
from src.auth.flet_auth_config import SecureAuthConfig, get_auth_config
from src.auth.flet_auth_handlers import FletAuthHandler, AuthenticatedApp
from src.auth.route_protection import RouteProtector, AuthGuard
from src.auth.flet_auth_ui import GoogleSignInButton, AuthenticationPage


class TestSecureAuthConfig:
    """Test secure authentication configuration."""

    def setup_method(self):
        """Set up test environment."""
        # Mock environment variables
        self.env_vars = {
            "GOOGLE_CLIENT_ID": "test_client_id",
            "GOOGLE_CLIENT_SECRET": "test_client_secret",
            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length",
            "GOOGLE_REDIRECT_URI": "http://localhost:8000/oauth_callback"
        }

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_secure_auth_config_initialization(self):
        """Test secure authentication configuration initialization."""
        config = SecureAuthConfig()

        assert config is not None
        assert hasattr(config, '_encryption_key')
        assert hasattr(config, '_fernet')

    @patch.dict(os.environ, {})
    def test_missing_environment_variables_raises_error(self):
        """Test that missing environment variables raise appropriate error."""
        with pytest.raises(ValueError, match="Missing required environment variables"):
            SecureAuthConfig()

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "short"})
    def test_short_session_secret_raises_error(self):
        """Test that short session secret raises error."""
        with pytest.raises(ValueError, match="SESSION_SECRET_KEY must be at least 32 characters"):
            SecureAuthConfig()

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    @patch('src.auth.flet_auth_config.GoogleOAuthProvider')
    def test_create_google_oauth_provider(self, mock_provider_class):
        """Test Google OAuth provider creation."""
        config = SecureAuthConfig()
        mock_provider = Mock()
        mock_provider_class.return_value = mock_provider

        provider = config.create_google_oauth_provider()

        assert provider == mock_provider
        mock_provider_class.assert_called_once_with(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_url="http://localhost:8000/oauth_callback"
        )

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_token_encryption_decryption(self):
        """Test token encryption and decryption."""
        config = SecureAuthConfig()

        original_token = "test_access_token_12345"
        encrypted_token = config.encrypt_token(original_token)
        decrypted_token = config.decrypt_token(encrypted_token)

        assert encrypted_token != original_token
        assert decrypted_token == original_token

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_invalid_token_decryption_returns_empty(self):
        """Test that invalid token decryption returns empty string."""
        config = SecureAuthConfig()

        result = config.decrypt_token("invalid_encrypted_token")

        assert result == ""

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_storage_key_generation(self):
        """Test storage key generation with proper prefix."""
        config = SecureAuthConfig()

        key = config.get_storage_key("tokens")

        assert key == "tide.auth.tokens"

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_oauth_scopes(self):
        """Test OAuth scopes configuration."""
        config = SecureAuthConfig()

        scopes = config.get_oauth_scopes()

        expected_scopes = ["openid", "profile", "email"]
        assert scopes == expected_scopes


class TestFletAuthHandler:
    """Test Flet authentication handler."""

    def setup_method(self):
        """Set up test environment."""
        self.mock_page = Mock(spec=ft.Page)
        self.mock_page.auth = None
        self.mock_page.client_storage = Mock()

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_auth_handler_initialization(self):
        """Test authentication handler initialization."""
        handler = FletAuthHandler(self.mock_page)

        assert handler.page == self.mock_page
        assert handler.current_user is None
        assert self.mock_page.on_login == handler._handle_login_event
        assert self.mock_page.on_logout == handler._handle_logout_event

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_user_not_authenticated_initially(self):
        """Test that user is not authenticated initially."""
        handler = FletAuthHandler(self.mock_page)

        assert not handler.is_authenticated()
        assert handler.get_current_user() is None

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_login_event_with_error(self):
        """Test login event handling with error."""
        handler = FletAuthHandler(self.mock_page)
        mock_event = Mock()
        mock_event.error = "OAuth error occurred"

        handler._handle_login_event(mock_event)

        assert handler.current_user is None
        assert not handler.is_authenticated()

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_successful_login_event(self):
        """Test successful login event handling."""
        # Set up mock authentication data
        mock_user = Mock()
        mock_user.id = "123"
        mock_user.email = "test@example.com"
        mock_user.name = "Test User"
        mock_user.picture = "https://example.com/picture.jpg"

        mock_token = Mock()
        mock_token.access_token = "access_token_123"
        mock_token.refresh_token = "refresh_token_456"
        mock_token.token_type = "Bearer"
        mock_token.expires_at = None

        self.mock_page.auth = Mock()
        self.mock_page.auth.user = mock_user
        self.mock_page.auth.token = mock_token

        handler = FletAuthHandler(self.mock_page)
        mock_event = Mock()
        mock_event.error = None

        handler._handle_login_event(mock_event)

        assert handler.current_user is not None
        assert handler.is_authenticated()
        assert handler.current_user["email"] == "test@example.com"

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_logout_clears_session(self):
        """Test that logout clears user session."""
        handler = FletAuthHandler(self.mock_page)
        handler.current_user = {"user_id": "123", "email": "test@example.com"}

        mock_event = Mock()
        handler._handle_logout_event(mock_event)

        assert handler.current_user is None
        assert not handler.is_authenticated()


class TestRouteProtector:
    """Test route protection functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.mock_page = Mock(spec=ft.Page)
        self.mock_auth_handler = Mock()

    def test_route_protector_initialization(self):
        """Test route protector initialization."""
        protector = RouteProtector(self.mock_auth_handler)

        assert protector.auth_handler == self.mock_auth_handler
        assert "/auth" in protector.public_routes
        assert "/" in protector.public_routes

    def test_add_protected_route(self):
        """Test adding protected route."""
        protector = RouteProtector(self.mock_auth_handler)

        protector.add_protected_route("/dashboard")

        assert "/dashboard" in protector.protected_routes
        assert protector.is_route_protected("/dashboard")

    def test_add_public_route(self):
        """Test adding public route."""
        protector = RouteProtector(self.mock_auth_handler)

        protector.add_public_route("/public")

        assert "/public" in protector.public_routes
        assert protector.is_route_public("/public")

    def test_public_route_access_allowed(self):
        """Test that public routes allow access."""
        protector = RouteProtector(self.mock_auth_handler)

        result = protector.check_route_access("/auth")

        assert result is True

    def test_protected_route_access_with_authentication(self):
        """Test protected route access when authenticated."""
        self.mock_auth_handler.is_authenticated.return_value = True
        self.mock_auth_handler.get_current_user.return_value = {"email": "test@example.com"}

        protector = RouteProtector(self.mock_auth_handler)
        protector.add_protected_route("/dashboard")

        result = protector.check_route_access("/dashboard")

        assert result is True

    def test_protected_route_access_without_authentication(self):
        """Test protected route access when not authenticated."""
        self.mock_auth_handler.is_authenticated.return_value = False

        protector = RouteProtector(self.mock_auth_handler)
        protector.add_protected_route("/dashboard")

        result = protector.check_route_access("/dashboard")

        assert result is False

    def test_protect_route_navigation_with_redirect(self):
        """Test route navigation protection with redirect."""
        self.mock_auth_handler.is_authenticated.return_value = False
        self.mock_auth_handler.page = self.mock_page

        protector = RouteProtector(self.mock_auth_handler)
        protector.add_protected_route("/dashboard")

        result = protector.protect_route_navigation("/dashboard")

        assert result is False
        self.mock_page.go.assert_called_once_with("/auth")


class TestGoogleSignInButton:
    """Test Google Sign-In button component."""

    def setup_method(self):
        """Set up test environment."""
        self.mock_callback = Mock()

    def test_google_signin_button_initialization(self):
        """Test Google Sign-In button initialization."""
        button = GoogleSignInButton(on_click=self.mock_callback)

        assert button.on_click_callback == self.mock_callback
        assert not button.is_loading
        assert button.button_text.value == "Sign in with Google"

    def test_set_loading_state_true(self):
        """Test setting loading state to true."""
        button = GoogleSignInButton()

        button.set_loading_state(True)

        assert button.is_loading
        assert button.button_text.value == "Signing in..."
        assert not button.google_icon.visible
        assert button.loading_spinner.visible

    def test_set_loading_state_false(self):
        """Test setting loading state to false."""
        button = GoogleSignInButton()
        button.set_loading_state(True)  # First set to true

        button.set_loading_state(False)

        assert not button.is_loading
        assert button.button_text.value == "Sign in with Google"
        assert button.google_icon.visible
        assert not button.loading_spinner.visible

    def test_handle_click_during_loading_ignored(self):
        """Test that button clicks are ignored during loading."""
        button = GoogleSignInButton(on_click=self.mock_callback)
        button.set_loading_state(True)

        button._handle_click(Mock())

        self.mock_callback.assert_not_called()

    def test_handle_auth_success(self):
        """Test handling authentication success."""
        mock_success_callback = Mock()
        button = GoogleSignInButton(on_auth_success=mock_success_callback)
        button.set_loading_state(True)  # Set loading first

        user_info = {"email": "test@example.com", "name": "Test User"}
        button.handle_auth_success(user_info)

        assert not button.is_loading
        mock_success_callback.assert_called_once_with(user_info)

    def test_handle_auth_error(self):
        """Test handling authentication error."""
        mock_error_callback = Mock()
        button = GoogleSignInButton(on_auth_error=mock_error_callback)
        button.set_loading_state(True)  # Set loading first

        error_message = "Authentication failed"
        button.handle_auth_error(error_message)

        assert not button.is_loading
        mock_error_callback.assert_called_once_with(error_message)


class TestAuthenticationPage:
    """Test authentication page component."""

    def setup_method(self):
        """Set up test environment."""
        self.mock_page = Mock(spec=ft.Page)
        self.mock_success_callback = Mock()

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_authentication_page_initialization(self):
        """Test authentication page initialization."""
        auth_page = AuthenticationPage(
            page=self.mock_page,
            on_auth_success=self.mock_success_callback
        )

        assert auth_page.page == self.mock_page
        assert auth_page.on_auth_success_callback == self.mock_success_callback
        assert hasattr(auth_page, 'google_signin_button')
        assert hasattr(auth_page, 'error_message')

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_show_error_message(self):
        """Test showing error message."""
        auth_page = AuthenticationPage(self.mock_page)

        auth_page._show_error_message("Test error")

        assert auth_page.error_message.visible
        assert auth_page.error_message.content.value == "Test error"

    @patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test_client_id",
                            "GOOGLE_CLIENT_SECRET": "test_client_secret",
                            "SESSION_SECRET_KEY": "test_session_secret_key_32_characters_minimum_length"})
    def test_hide_error_message(self):
        """Test hiding error message."""
        auth_page = AuthenticationPage(self.mock_page)
        auth_page._show_error_message("Test error")  # First show error

        auth_page._hide_error_message()

        assert not auth_page.error_message.visible


class TestAuthGuard:
    """Test authentication guard functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.mock_auth_handler = Mock()

    def test_auth_guard_initialization(self):
        """Test authentication guard initialization."""
        guard = AuthGuard(self.mock_auth_handler)

        assert guard.auth_handler == self.mock_auth_handler

    def test_create_user_info_display_when_authenticated(self):
        """Test creating user info display when authenticated."""
        self.mock_auth_handler.is_authenticated.return_value = True
        self.mock_auth_handler.get_current_user.return_value = {
            "name": "Test User",
            "email": "test@example.com"
        }

        guard = AuthGuard(self.mock_auth_handler)
        result = guard.create_user_info_display()

        assert result is not None
        assert isinstance(result, ft.Container)

    def test_create_user_info_display_when_not_authenticated(self):
        """Test creating user info display when not authenticated."""
        self.mock_auth_handler.is_authenticated.return_value = False

        guard = AuthGuard(self.mock_auth_handler)
        result = guard.create_user_info_display()

        assert result is None

    def test_protected_component_when_authenticated(self):
        """Test protected component when authenticated."""
        self.mock_auth_handler.is_authenticated.return_value = True
        mock_component = Mock()

        guard = AuthGuard(self.mock_auth_handler)
        result = guard.create_protected_component(mock_component)

        assert result == mock_component

    def test_protected_component_when_not_authenticated_with_prompt(self):
        """Test protected component when not authenticated with auth prompt."""
        self.mock_auth_handler.is_authenticated.return_value = False
        mock_component = Mock()

        guard = AuthGuard(self.mock_auth_handler)
        result = guard.create_protected_component(mock_component, show_auth_prompt=True)

        assert result != mock_component
        assert isinstance(result, ft.Container)

    def test_protected_component_when_not_authenticated_without_prompt(self):
        """Test protected component when not authenticated without auth prompt."""
        self.mock_auth_handler.is_authenticated.return_value = False
        mock_component = Mock()

        guard = AuthGuard(self.mock_auth_handler)
        result = guard.create_protected_component(mock_component, show_auth_prompt=False)

        assert result != mock_component
        assert isinstance(result, ft.Container)

    def test_protected_action_when_authenticated(self):
        """Test protected action when authenticated."""
        self.mock_auth_handler.is_authenticated.return_value = True
        self.mock_auth_handler.get_current_user.return_value = {"email": "test@example.com"}

        mock_action = Mock(return_value="action_result")
        mock_action.__name__ = "test_action"  # Add function name attribute
        guard = AuthGuard(self.mock_auth_handler)

        protected_action = guard.protected_action(mock_action)
        result = protected_action("arg1", kwarg1="value1")

        assert result == "action_result"
        mock_action.assert_called_once_with("arg1", kwarg1="value1")

    def test_protected_action_when_not_authenticated(self):
        """Test protected action when not authenticated."""
        self.mock_auth_handler.is_authenticated.return_value = False
        self.mock_auth_handler.page = Mock()

        mock_action = Mock()
        mock_action.__name__ = "test_action"  # Add function name attribute
        guard = AuthGuard(self.mock_auth_handler)

        protected_action = guard.protected_action(mock_action)
        result = protected_action("arg1")

        assert result is None
        mock_action.assert_not_called()
        self.mock_auth_handler.page.go.assert_called_once_with("/auth")