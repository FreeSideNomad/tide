"""
Integration tests for authentication flow.
Tests the complete OAuth integration including UI components and services.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
import flet as ft

from src.main import main
from src.ui.auth_components import AuthenticationPage, GoogleSignInButton


class TestAuthenticationIntegration:
    """Integration tests for authentication flow."""

    @patch("src.config.GOOGLE_CLIENT_ID", "test_client_id")
    @patch("src.config.GOOGLE_CLIENT_SECRET", "test_client_secret")
    def test_main_app_initialization(self):
        """Test that main app initializes with authentication page."""
        # Create a mock page
        mock_page = MagicMock(spec=ft.Page)
        mock_page.session = MagicMock()
        mock_page.views = MagicMock()

        # Run main function
        main(mock_page)

        # Verify page configuration
        assert mock_page.title == "Tide - DBT AI Assistant"
        assert mock_page.window.width == 800
        assert mock_page.window.height == 600

        # Verify navigation setup and initial route
        assert mock_page.on_route_change is not None
        assert mock_page.on_view_pop is not None
        mock_page.go.assert_called_once_with("/auth")

    @patch("src.ui.auth_components.webbrowser")
    def test_oauth_flow_integration(self, mock_webbrowser):
        """Test complete OAuth flow integration."""
        # Create authentication page with mocked OAuth service
        with patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test-client-id"}):
            # Import after environment variable is set
            from src.ui.auth_components import AuthenticationPage

            auth_page = AuthenticationPage()

        # Mock page and session
        mock_page = MagicMock(spec=ft.Page)
        mock_page.session = MagicMock()
        auth_page.page = mock_page
        auth_page.google_button.page = mock_page

        # Simulate button click
        auth_page.google_button._handle_click(None)

        # Verify OAuth URL was opened in browser
        mock_webbrowser.open.assert_called_once()

        # Verify URL contains expected parameters
        called_url = mock_webbrowser.open.call_args[0][0]
        assert "accounts.google.com" in called_url
        # Verify OAuth parameters are present (don't check specific client ID in integration test)
        assert "client_id=" in called_url
        assert "response_type=code" in called_url
        assert "scope=openid+profile+email" in called_url
        assert "redirect_uri=" in called_url
        assert "state=" in called_url

    def test_error_handling_integration(self):
        """Test error handling across components."""
        with patch("src.auth.oauth.GOOGLE_CLIENT_ID", None):
            # This should raise an error during OAuth service initialization
            with pytest.raises(
                ValueError, match="Google OAuth client ID not configured"
            ):
                GoogleSignInButton()

    @patch("src.config.GOOGLE_CLIENT_ID", "test_client_id")
    def test_accessibility_integration(self):
        """Test accessibility features integration."""
        # Create authentication page
        auth_page = AuthenticationPage()

        # Verify Google button has accessibility features
        button = auth_page.google_button
        assert button.tooltip == "Sign in with your Google account"

        # Verify page layout supports accessibility
        assert isinstance(auth_page, ft.Column)
        assert auth_page.horizontal_alignment == ft.CrossAxisAlignment.CENTER

    @patch("src.ui.auth_components.webbrowser")
    @patch("src.config.GOOGLE_CLIENT_ID", "test_client_id")
    def test_state_management_integration(self, mock_webbrowser):
        """Test OAuth state management integration."""
        # Create authentication page with mock page
        auth_page = AuthenticationPage()
        mock_page = MagicMock(spec=ft.Page)
        mock_page.session = MagicMock()
        auth_page.page = mock_page
        auth_page.google_button.page = mock_page

        # Simulate button click
        auth_page.google_button._handle_click(None)

        # Verify state was stored in session
        mock_page.session.set.assert_called_once()
        call_args = mock_page.session.set.call_args
        assert call_args[0][0] == "oauth_state"
        assert len(call_args[0][1]) > 0  # State should be non-empty

        # Verify state is stored in button for validation
        assert auth_page.google_button.current_state == call_args[0][1]

    def test_loading_state_integration(self):
        """Test loading state management integration."""
        # Create authentication page with mocked environment
        with patch.dict(os.environ, {"GOOGLE_CLIENT_ID": "test-client-id"}):
            from src.ui.auth_components import AuthenticationPage

            auth_page = AuthenticationPage()

        # Mock page setup to avoid Flet page attachment requirement
        mock_page = MagicMock(spec=ft.Page)
        auth_page.page = mock_page
        # Also attach page to the Google button to avoid update errors
        auth_page.google_button.page = mock_page

        # Test auth start callback
        auth_page._on_auth_start()
        assert auth_page.status_text.visible is True
        assert "Opening Google authentication" in auth_page.status_text.value

        # Test error callback
        auth_page._on_auth_error("Test error")
        assert auth_page.status_text.visible is True
        assert "Test error" in auth_page.status_text.value
        assert auth_page.status_text.color == ft.Colors.RED_600

        # Test reset
        auth_page.reset_status()
        assert auth_page.status_text.visible is False
