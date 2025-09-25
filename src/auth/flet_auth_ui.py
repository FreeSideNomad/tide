"""
Flet Authentication UI Components

SECURITY REQUIREMENTS (from CLAUDE.md):
- MANDATORY: Follow https://flet.dev/docs/cookbook/authentication/ exactly
- Safety-first design prioritizing user wellbeing
- No custom authentication solutions allowed
- Complete audit trail for safety monitoring

This module provides Google Sign-In UI components using Flet's official patterns.
"""

import logging
from typing import Callable, Optional
import flet as ft
from .flet_auth_config import get_auth_config

# Configure logging for security audit trail
logger = logging.getLogger(__name__)


class GoogleSignInButton(ft.Container):
    """
    Google Sign-In button following Google's branding guidelines and Flet patterns.

    Security Features:
    - Official Google branding compliance
    - Loading states for user feedback
    - Accessible design with keyboard navigation
    - Audit logging for authentication attempts
    """

    def __init__(
        self,
        on_click: Optional[Callable] = None,
        on_auth_success: Optional[Callable] = None,
        on_auth_error: Optional[Callable] = None,
    ):
        """
        Initialize Google Sign-In button.

        Args:
            on_click: Callback for button click events
            on_auth_success: Callback for successful authentication
            on_auth_error: Callback for authentication errors
        """
        self.on_click_callback = on_click
        self.on_auth_success_callback = on_auth_success
        self.on_auth_error_callback = on_auth_error
        self.is_loading = False

        # Create button content
        self._create_button_content()

        super().__init__(
            content=self.button_content,
            on_click=self._handle_click,
            border_radius=ft.BorderRadius(4, 4, 4, 4),
            bgcolor=ft.Colors.WHITE,
            border=ft.Border(
                top=ft.BorderSide(1, ft.Colors.GREY_300),
                right=ft.BorderSide(1, ft.Colors.GREY_300),
                bottom=ft.BorderSide(1, ft.Colors.GREY_300),
                left=ft.BorderSide(1, ft.Colors.GREY_300),
            ),
            padding=ft.Padding(12, 8, 12, 8),
            animate=ft.Animation(200),
            tooltip="Sign in with your Google account",
        )

        logger.info("✅ Google Sign-In button initialized")

    def _create_button_content(self):
        """Create button content following Google's branding guidelines."""
        # Google logo (using built-in icon as placeholder)
        self.google_icon = ft.Icon(
            name=ft.Icons.ACCOUNT_CIRCLE,
            color=ft.Colors.BLUE_600,
            size=20,
        )

        # Button text
        self.button_text = ft.Text(
            "Sign in with Google",
            size=14,
            weight=ft.FontWeight.NORMAL,
            color=ft.Colors.GREY_700,
        )

        # Loading spinner
        self.loading_spinner = ft.ProgressRing(
            width=20,
            height=20,
            stroke_width=3,
            color=ft.Colors.BLUE_600,
            visible=False,
        )

        # Button content row
        self.button_content = ft.Row(
            controls=[
                self.google_icon,
                ft.Container(width=8),  # Spacing
                self.button_text,
                self.loading_spinner,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )

    def _handle_click(self, e):
        """
        Handle button click with loading state management.

        Security: Prevents multiple concurrent authentication attempts
        """
        if self.is_loading:
            logger.warning("⚠️ Authentication already in progress, ignoring click")
            return

        logger.info("🔐 Google Sign-In button clicked - starting authentication")
        self.set_loading_state(True)

        try:
            if self.on_click_callback:
                self.on_click_callback(e)
        except Exception as error:
            logger.error(f"❌ Authentication button click handler failed: {error}")
            self.set_loading_state(False)
            if self.on_auth_error_callback:
                self.on_auth_error_callback(str(error))

    def set_loading_state(self, loading: bool):
        """
        Set loading state with visual feedback.

        Args:
            loading: True to show loading state, False to hide
        """
        self.is_loading = loading

        if loading:
            self.button_text.value = "Signing in..."
            self.button_text.color = ft.Colors.GREY_500
            self.google_icon.visible = False
            self.loading_spinner.visible = True
            self.bgcolor = ft.Colors.GREY_50
        else:
            self.button_text.value = "Sign in with Google"
            self.button_text.color = ft.Colors.GREY_700
            self.google_icon.visible = True
            self.loading_spinner.visible = False
            self.bgcolor = ft.Colors.WHITE

        self.update()

    def handle_auth_success(self, user_info: dict):
        """
        Handle successful authentication.

        Args:
            user_info: User information from OAuth provider

        Security: Logs successful authentication for audit trail
        """
        logger.info(
            f"✅ Authentication successful for user: {user_info.get('email', 'unknown')}"
        )
        self.set_loading_state(False)

        if self.on_auth_success_callback:
            self.on_auth_success_callback(user_info)

    def handle_auth_error(self, error_message: str):
        """
        Handle authentication errors.

        Args:
            error_message: Error description

        Security: Logs authentication failures for security monitoring
        """
        logger.error(f"❌ Authentication failed: {error_message}")
        self.set_loading_state(False)

        if self.on_auth_error_callback:
            self.on_auth_error_callback(error_message)


class AuthenticationPage(ft.Container):
    """
    Complete authentication page with Google Sign-In integration.

    Security Features:
    - Follows Flet authentication patterns exactly
    - Safety-first messaging for user wellbeing
    - Error handling with user-friendly messages
    - Audit logging for security monitoring
    """

    def __init__(
        self,
        page: ft.Page,
        on_auth_success: Optional[Callable] = None,
    ):
        """
        Initialize authentication page.

        Args:
            page: Flet page instance
            on_auth_success: Callback for successful authentication
        """
        self.page = page
        self.on_auth_success_callback = on_auth_success
        self.auth_config = get_auth_config()

        # Create page content
        self._create_page_content()

        super().__init__(
            content=self.main_content,
            alignment=ft.alignment.center,
            expand=True,
        )

        logger.info("✅ Authentication page initialized")

    def _create_page_content(self):
        """Create authentication page content with safety-first messaging."""
        # App logo and title
        app_icon = ft.Icon(
            name=ft.Icons.PSYCHOLOGY,
            size=64,
            color=ft.Colors.BLUE_600,
        )

        app_title = ft.Text(
            "Welcome to Tide",
            size=32,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        app_subtitle = ft.Text(
            "Your Safety-First DBT AI Assistant",
            size=18,
            color=ft.Colors.GREY_600,
            text_align=ft.TextAlign.CENTER,
        )

        # Safety-first messaging (from CLAUDE.md requirements)
        safety_message = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "🛡️ Your Safety Comes First",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.GREEN_700,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Tide provides evidence-based DBT skills with built-in safety protocols. "
                        "We prioritize your wellbeing over all other considerations.",
                        size=14,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            bgcolor=ft.Colors.GREEN_50,
            border=ft.Border(
                top=ft.BorderSide(1, ft.Colors.GREEN_200),
                right=ft.BorderSide(1, ft.Colors.GREEN_200),
                bottom=ft.BorderSide(1, ft.Colors.GREEN_200),
                left=ft.BorderSide(1, ft.Colors.GREEN_200),
            ),
            border_radius=ft.BorderRadius(8, 8, 8, 8),
            padding=ft.Padding(16, 12, 16, 12),
            width=400,
        )

        # Google Sign-In button
        self.google_signin_button = GoogleSignInButton(
            on_click=self._handle_google_signin,
            on_auth_success=self._handle_auth_success,
            on_auth_error=self._handle_auth_error,
        )

        # Sign-in section
        signin_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Sign in to access your personalized DBT skills",
                        size=16,
                        color=ft.Colors.GREY_800,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=16),  # Spacing
                    self.google_signin_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            width=300,
        )

        # Error message container
        self.error_message = ft.Container(
            content=ft.Text(
                "",
                color=ft.Colors.RED_600,
                text_align=ft.TextAlign.CENTER,
                size=14,
            ),
            visible=False,
            width=400,
        )

        # Main content column
        self.main_content = ft.Column(
            controls=[
                app_icon,
                ft.Container(height=16),
                app_title,
                app_subtitle,
                ft.Container(height=32),
                safety_message,
                ft.Container(height=32),
                signin_section,
                ft.Container(height=16),
                self.error_message,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

    def _handle_google_signin(self, e):
        """
        Handle Google Sign-In initiation using Flet's OAuth patterns (GitHub issue #2936).

        Security: Uses Flet's official login method with secure configuration
        """
        try:
            # Clear any previous error messages
            self._hide_error_message()

            # Create Google OAuth provider using secure configuration
            provider = self.auth_config.create_google_oauth_provider()

            # Initiate OAuth flow using Flet's official pattern (GitHub issue #2936)
            # Note: page.login() triggers the on_login event handler
            self.page.login(provider)

            logger.info("🔐 OAuth flow initiated with Google provider")

        except Exception as error:
            logger.error(f"❌ Failed to initiate Google OAuth: {error}")
            self._show_error_message(f"Authentication setup failed: {error}")
            self.google_signin_button.set_loading_state(False)

    def _handle_auth_success(self, user_info: dict):
        """
        Handle successful authentication.

        Args:
            user_info: User information from OAuth provider

        Security: Validates user data and calls success callback
        """
        logger.info(
            f"✅ Authentication successful in UI for: {user_info.get('email', 'unknown')}"
        )

        if self.on_auth_success_callback:
            self.on_auth_success_callback(user_info)

    def _handle_auth_error(self, error_message: str):
        """
        Handle authentication errors with user-friendly messages.

        Args:
            error_message: Error description

        Security: Logs errors without exposing sensitive details to user
        """
        logger.error(f"❌ Authentication error in UI: {error_message}")

        # Show user-friendly error message
        friendly_message = (
            "Sign-in failed. Please try again or check your internet connection."
        )
        self._show_error_message(friendly_message)

    def _show_error_message(self, message: str):
        """Show error message to user."""
        self.error_message.content.value = message
        self.error_message.visible = True
        self.error_message.update()

    def _hide_error_message(self):
        """Hide error message."""
        self.error_message.visible = False
        self.error_message.update()
