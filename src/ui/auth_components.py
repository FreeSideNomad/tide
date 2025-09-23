"""
Authentication UI components for Tide application.
Implements Google Sign In button following Google's branding guidelines.
"""

import flet as ft
import webbrowser
import threading
import time
import logging
from typing import Callable, Optional, Dict, Any
from src.auth.oauth import GoogleOAuthService, AuthenticationError
from src.auth.server import get_auth_server

# Configure logging
logger = logging.getLogger(__name__)


class GoogleSignInButton(ft.Container):
    """
    Google Sign In button component following Google's branding guidelines.
    Implements accessibility features and proper error handling.
    """

    def __init__(
        self,
        on_auth_start: Optional[Callable] = None,
        on_auth_error: Optional[Callable[[str], None]] = None,
        on_auth_success: Optional[Callable[[Dict[str, Any]], None]] = None,
        **kwargs,
    ):
        """
        Initialize Google Sign In button.

        Args:
            on_auth_start: Callback when authentication starts
            on_auth_error: Callback when authentication error occurs
            on_auth_success: Callback when authentication succeeds with user info
        """
        self.on_auth_start = on_auth_start
        self.on_auth_error = on_auth_error
        self.on_auth_success = on_auth_success
        self.oauth_service = GoogleOAuthService()
        self.auth_server = get_auth_server()
        self.is_loading = False
        self.current_state = None
        self.current_session_id = None
        self.polling_thread = None

        # Create button content
        self.button_content = ft.Row(
            controls=[
                # Google logo (using icon for now, replace with actual logo in production)
                ft.Icon(
                    name=ft.Icons.ACCOUNT_CIRCLE,
                    color=ft.Colors.WHITE,
                    size=20,
                ),
                ft.Text(
                    "Sign in with Google",
                    color=ft.Colors.WHITE,
                    size=16,
                    weight=ft.FontWeight.W_500,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

        self.loading_content = ft.Row(
            controls=[
                ft.ProgressRing(
                    width=20,
                    height=20,
                    stroke_width=2,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    "Signing in...",
                    color=ft.Colors.WHITE,
                    size=16,
                    weight=ft.FontWeight.W_500,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

        # Initialize container with Google's recommended styling
        super().__init__(
            content=self.button_content,
            bgcolor=ft.Colors.BLUE_600,  # Google blue
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.symmetric(horizontal=24, vertical=12),
            ink=True,
            on_click=self._handle_click,
            tooltip="Sign in with your Google account",
            **kwargs,
        )

    def _handle_click(self, e):
        """Handle button click event."""
        if self.is_loading:
            return

        try:
            self._set_loading_state(True)

            # Generate OAuth URL and state
            auth_url, state = self.oauth_service.generate_auth_url()
            self.current_state = state

            # Store state in page session for later validation
            if hasattr(self.page, "session"):
                self.page.session.set("oauth_state", state)

            # Notify callback that auth is starting
            if self.on_auth_start:
                self.on_auth_start()

            # Create auth session in server
            logger.info(f"🔐 Starting OAuth flow with state: {state}")
            session_id = self.auth_server.create_auth_session(auth_url, state)
            self.current_session_id = session_id
            logger.info(f"📝 Created session: {session_id}")

            # Open OAuth URL in browser
            logger.info(f"🌐 Opening OAuth URL: {auth_url}")
            webbrowser.open(auth_url)

            # Start polling for auth completion
            logger.info("🔄 Starting auth polling...")
            self._start_auth_polling()

        except AuthenticationError as e:
            self._handle_error(f"Authentication error: {str(e)}")
        except Exception as e:
            self._handle_error(f"Unexpected error: {str(e)}")

    def _set_loading_state(self, loading: bool):
        """Set button loading state."""
        self.is_loading = loading
        self.content = self.loading_content if loading else self.button_content

        # Update button styling for loading state
        if loading:
            self.bgcolor = ft.Colors.BLUE_400  # Slightly faded
            self.on_click = None  # Disable clicks during loading
        else:
            self.bgcolor = ft.Colors.BLUE_600
            self.on_click = self._handle_click

        if hasattr(self, "update"):
            self.update()

    def _handle_error(self, error_message: str):
        """Handle authentication errors."""
        self._set_loading_state(False)

        if self.on_auth_error:
            self.on_auth_error(error_message)
        else:
            # Default error handling - show snack bar
            if hasattr(self, "page") and self.page:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Sign in failed: {error_message}"),
                    bgcolor=ft.Colors.RED_400,
                )
                self.page.snack_bar.open = True
                self.page.update()

    def _start_auth_polling(self):
        """Start polling for authentication completion."""
        if self.polling_thread and self.polling_thread.is_alive():
            return  # Already polling

        def poll_auth_status():
            """Poll the auth server for completion."""
            max_attempts = 60  # 5 minutes (5 second intervals)
            attempt = 0
            logger.info(f"🔄 Starting polling for session: {self.current_session_id}")

            while attempt < max_attempts and self.current_session_id:
                try:
                    time.sleep(5)  # Poll every 5 seconds
                    attempt += 1

                    if not self.current_session_id:
                        logger.info("⏹️ Session was reset, stopping polling")
                        break  # Session was reset

                    # Check auth status
                    import httpx

                    url = f"http://127.0.0.1:8000/auth/status/{self.current_session_id}"
                    logger.info(f"📞 Polling attempt {attempt}: {url}")

                    response = httpx.get(url)
                    logger.info(f"📡 Response status: {response.status_code}")

                    if response.status_code == 200:
                        result = response.json()
                        logger.info(f"📊 Poll result: {result}")

                        if result.get("success"):
                            # Authentication succeeded
                            user_info = result.get("user_info", {})
                            logger.info(
                                f"✅ Authentication succeeded for: {user_info.get('name', 'Unknown')}"
                            )
                            self._handle_auth_success(user_info)
                            break
                        elif result.get("status") == "not_found":
                            # Session expired or not found
                            logger.error("❌ Session not found")
                            self._handle_error(
                                "Authentication session expired. Please try again."
                            )
                            break
                        else:
                            logger.info(
                                f"⏳ Still pending (attempt {attempt}/{max_attempts})"
                            )
                            # Otherwise, continue polling (status: "pending")
                    else:
                        logger.warning(
                            f"⚠️ Unexpected response status: {response.status_code}"
                        )

                except Exception as e:
                    # Continue polling on error, but limit attempts
                    logger.error(f"❌ Polling error on attempt {attempt}: {str(e)}")
                    if attempt >= max_attempts:
                        self._handle_error(f"Polling error: {str(e)}")

            # Timeout or error
            if attempt >= max_attempts:
                logger.error("⏱️ Authentication polling timed out")
                self._handle_error("Authentication timed out. Please try again.")

        self.polling_thread = threading.Thread(target=poll_auth_status, daemon=True)
        self.polling_thread.start()

    def _handle_auth_success(self, user_info: Dict[str, Any]):
        """Handle successful authentication."""
        self._set_loading_state(False)
        self.current_session_id = None

        if self.on_auth_success:
            self.on_auth_success(user_info)

    def reset_state(self):
        """Reset button to initial state."""
        self._set_loading_state(False)
        self.current_state = None
        self.current_session_id = None


class AuthenticationPage(ft.Column):
    """
    Authentication page component with Google Sign In.
    Implements the landing page UI for user authentication.
    """

    def __init__(
        self,
        on_auth_success: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_auth_error: Optional[Callable[[str], None]] = None,
        **kwargs,
    ):
        """
        Initialize authentication page.

        Args:
            on_auth_success: Callback when authentication succeeds
            on_auth_error: Callback when authentication fails
        """
        self.on_auth_success = on_auth_success
        self.on_auth_error = on_auth_error

        # Page title and description
        title = ft.Text(
            "Welcome to Tide",
            size=32,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        subtitle = ft.Text(
            "Your safety-first DBT AI assistant",
            size=18,
            color=ft.Colors.GREY_600,
            text_align=ft.TextAlign.CENTER,
        )

        description = ft.Text(
            "Sign in to access personalized DBT skills and begin your journey "
            "toward improved emotional regulation and interpersonal effectiveness.",
            size=14,
            color=ft.Colors.GREY_700,
            text_align=ft.TextAlign.CENTER,
            width=400,
        )

        # Create Google Sign In button
        self.google_button = GoogleSignInButton(
            on_auth_start=self._on_auth_start,
            on_auth_error=self._on_auth_error,
            on_auth_success=self._on_auth_success,
        )

        # Status text for feedback
        self.status_text = ft.Text(
            "",
            size=14,
            color=ft.Colors.GREY_600,
            text_align=ft.TextAlign.CENTER,
            visible=False,
        )

        super().__init__(
            controls=[
                # Logo/icon placeholder
                ft.Icon(
                    name=ft.Icons.PSYCHOLOGY,
                    size=64,
                    color=ft.Colors.BLUE_600,
                ),
                ft.Container(height=20),  # Spacing
                title,
                subtitle,
                ft.Container(height=20),  # Spacing
                description,
                ft.Container(height=40),  # Spacing
                self.google_button,
                ft.Container(height=20),  # Spacing
                self.status_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            **kwargs,
        )

    def _on_auth_start(self):
        """Handle authentication start."""
        self.status_text.value = "Opening Google authentication..."
        self.status_text.visible = True
        if hasattr(self, "update"):
            self.update()

    def _on_auth_success(self, user_info: Dict[str, Any]):
        """Handle authentication success."""
        self.status_text.value = "Authentication successful! Loading dashboard..."
        self.status_text.color = ft.Colors.GREEN_600
        self.status_text.visible = True
        if hasattr(self, "update"):
            self.update()

        # Call the parent callback
        if self.on_auth_success:
            self.on_auth_success(user_info)

    def _on_auth_error(self, error_message: str):
        """Handle authentication error."""
        self.status_text.value = f"Authentication failed: {error_message}"
        self.status_text.color = ft.Colors.RED_600
        self.status_text.visible = True
        if hasattr(self, "update"):
            self.update()

        # Call the parent callback
        if self.on_auth_error:
            self.on_auth_error(error_message)

    def reset_status(self):
        """Reset status message."""
        self.status_text.visible = False
        self.status_text.color = ft.Colors.GREY_600
        self.google_button.reset_state()
        if hasattr(self, "update"):
            self.update()
