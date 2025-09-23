"""
Unit tests for authentication UI components.
Tests the Google Sign In button and authentication page components.
"""

from unittest.mock import patch, MagicMock
import flet as ft

from src.ui.auth_components import GoogleSignInButton, AuthenticationPage


class TestGoogleSignInButton:
    """Test cases for GoogleSignInButton component."""

    def setup_method(self):
        """Set up test fixtures."""
        with patch("src.ui.auth_components.GoogleOAuthService"):
            self.button = GoogleSignInButton()

    def test_initialization(self):
        """Test button initialization with default parameters."""
        with patch("src.ui.auth_components.GoogleOAuthService"):
            button = GoogleSignInButton()

            assert button is not None
            assert button.is_loading is False
            assert button.current_state is None
            assert button.bgcolor == "#FFFFFF"  # Google's light theme background
            assert button.tooltip == "Sign in with your Google account"

    def test_initialization_with_callbacks(self):
        """Test button initialization with custom callbacks."""
        auth_start_mock = MagicMock()
        auth_error_mock = MagicMock()

        with patch("src.ui.auth_components.GoogleOAuthService"):
            button = GoogleSignInButton(
                on_auth_start=auth_start_mock, on_auth_error=auth_error_mock
            )

            assert button.on_auth_start == auth_start_mock
            assert button.on_auth_error == auth_error_mock

    def test_button_content_structure(self):
        """Test that button has correct content structure."""
        with patch("src.ui.auth_components.GoogleOAuthService"):
            button = GoogleSignInButton()

            # Check button content is a Row
            assert isinstance(button.button_content, ft.Row)

            # Check content has Google logo and text
            controls = button.button_content.controls
            assert len(controls) == 2
            assert isinstance(controls[0], ft.Container)  # Google logo container
            assert isinstance(controls[1], ft.Text)
            assert controls[1].value == "Sign in with Google"

    def test_loading_content_structure(self):
        """Test that loading content has correct structure."""
        with patch("src.ui.auth_components.GoogleOAuthService"):
            button = GoogleSignInButton()

            # Check loading content is a Row
            assert isinstance(button.loading_content, ft.Row)

            # Check content has progress ring and text
            controls = button.loading_content.controls
            assert len(controls) == 2
            assert isinstance(controls[0], ft.ProgressRing)
            assert isinstance(controls[1], ft.Text)
            assert controls[1].value == "Signing in..."

    @patch("src.ui.auth_components.webbrowser")
    def test_handle_click_success(self, mock_webbrowser):
        """Test successful button click handling."""
        mock_oauth_service = MagicMock()
        mock_oauth_service.generate_auth_url.return_value = (
            "http://test.com",
            "test_state",
        )

        with patch(
            "src.ui.auth_components.GoogleOAuthService", return_value=mock_oauth_service
        ):
            auth_start_mock = MagicMock()
            button = GoogleSignInButton(on_auth_start=auth_start_mock)
            button.page = MagicMock()
            button.page.session = MagicMock()

            # Simulate click
            button._handle_click(None)

            # Verify OAuth service was called
            mock_oauth_service.generate_auth_url.assert_called_once()

            # Verify browser was opened
            mock_webbrowser.open.assert_called_once_with("http://test.com")

            # Verify callback was called
            auth_start_mock.assert_called_once()

            # Verify state was stored
            button.page.session.set.assert_called_once_with("oauth_state", "test_state")

    def test_handle_click_during_loading(self):
        """Test that click is ignored when button is in loading state."""
        mock_oauth_service = MagicMock()

        with patch(
            "src.ui.auth_components.GoogleOAuthService", return_value=mock_oauth_service
        ):
            button = GoogleSignInButton()
            button.is_loading = True

            # Simulate click
            button._handle_click(None)

            # Verify OAuth service was not called
            mock_oauth_service.generate_auth_url.assert_not_called()

    def test_set_loading_state_true(self):
        """Test setting loading state to true."""
        with patch("src.ui.auth_components.GoogleOAuthService"):
            button = GoogleSignInButton()
            button.update = MagicMock()

            button._set_loading_state(True)

            assert button.is_loading is True
            assert button.content == button.loading_content
            assert button.bgcolor == "#F5F5F5"  # Google's loading state background
            assert button.on_click is None

    def test_set_loading_state_false(self):
        """Test setting loading state to false."""
        with patch("src.ui.auth_components.GoogleOAuthService"):
            button = GoogleSignInButton()
            button.update = MagicMock()

            button._set_loading_state(False)

            assert button.is_loading is False
            assert button.content == button.button_content
            assert button.bgcolor == "#FFFFFF"  # Google's light theme background
            assert button.on_click == button._handle_click

    def test_reset_state(self):
        """Test resetting button state."""
        with patch("src.ui.auth_components.GoogleOAuthService"):
            button = GoogleSignInButton()
            button.update = MagicMock()
            button.is_loading = True
            button.current_state = "test_state"

            button.reset_state()

            assert button.is_loading is False
            assert button.current_state is None


class TestAuthenticationPage:
    """Test cases for AuthenticationPage component."""

    def test_initialization(self):
        """Test authentication page initialization."""
        with patch("src.ui.auth_components.GoogleSignInButton"):
            page = AuthenticationPage()

            assert page is not None
            assert isinstance(page, ft.Column)
            assert page.horizontal_alignment == ft.CrossAxisAlignment.CENTER
            assert page.alignment == ft.MainAxisAlignment.CENTER

    def test_page_structure(self):
        """Test that page has correct component structure."""
        with patch("src.ui.auth_components.GoogleSignInButton") as mock_button:
            page = AuthenticationPage()

            # Check that page has multiple controls
            assert len(page.controls) > 5

            # Check that Google button was created
            mock_button.assert_called_once()

    def test_on_auth_start(self):
        """Test authentication start callback."""
        with patch("src.ui.auth_components.GoogleSignInButton"):
            page = AuthenticationPage()
            page.update = MagicMock()

            page._on_auth_start()

            assert page.status_text.visible is True
            assert "Opening Google authentication" in page.status_text.value

    def test_on_auth_error(self):
        """Test authentication error callback."""
        with patch("src.ui.auth_components.GoogleSignInButton"):
            page = AuthenticationPage()
            page.update = MagicMock()

            page._on_auth_error("Test error message")

            assert page.status_text.visible is True
            assert "Test error message" in page.status_text.value
            assert page.status_text.color == ft.Colors.RED_600

    def test_reset_status(self):
        """Test resetting page status."""
        mock_button = MagicMock()
        with patch(
            "src.ui.auth_components.GoogleSignInButton", return_value=mock_button
        ):
            page = AuthenticationPage()
            page.update = MagicMock()
            page.status_text.visible = True

            page.reset_status()

            assert page.status_text.visible is False
            assert page.status_text.color == ft.Colors.GREY_600
            mock_button.reset_state.assert_called_once()

    def test_accessibility_features(self):
        """Test that page includes accessibility features."""
        with patch("src.ui.auth_components.GoogleSignInButton"):
            page = AuthenticationPage()

            # Find text components and verify they have proper alignment
            text_controls = [c for c in page.controls if isinstance(c, ft.Text)]
            for text_control in text_controls:
                assert text_control.text_align == ft.TextAlign.CENTER
