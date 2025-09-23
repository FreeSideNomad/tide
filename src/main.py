"""
Tide - Safety-First DBT AI Assistant
Main application entry point with Google OAuth authentication.
"""

import flet as ft
import atexit
from typing import Optional, Dict, Any
from src.ui.auth_components import AuthenticationPage
from src.ui.dashboard import DashboardPage
from src.auth.server import start_auth_server, stop_auth_server


class TideApp:
    """Main Tide application with authentication state management."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.auth_server = None
        self.current_user: Optional[Dict[str, Any]] = None

        # Configure page properties
        self._configure_page()

        # Set up navigation
        self._setup_navigation()

        # Start auth server
        self._start_auth_server()

        # Navigate to initial route
        self.page.go("/auth")

    def _configure_page(self):
        """Configure page properties."""
        self.page.title = "Tide - DBT AI Assistant"
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.center()
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.accessibility = True

    def _setup_navigation(self):
        """Set up navigation and routing."""
        self.page.on_route_change = self._route_change
        self.page.on_view_pop = self._view_pop

    def _route_change(self, route):
        """Handle route changes."""
        # Clear existing views
        self.page.views.clear()

        # Create view based on current route
        if self.page.route == "/auth":
            self._create_auth_view()
        elif self.page.route == "/dashboard":
            self._create_dashboard_view()
        else:
            # Default to auth if route not recognized
            self.page.route = "/auth"
            self._create_auth_view()

        self.page.update()

    def _view_pop(self, view):
        """Handle view pop (back navigation)."""
        # Remove the top view
        if len(self.page.views) > 1:
            self.page.views.pop()
            self.page.update()

    def _create_auth_view(self):
        """Create authentication view."""
        auth_page = AuthenticationPage(
            on_auth_success=self._handle_auth_success,
            on_auth_error=self._handle_auth_error,
        )

        view = ft.View(
            "/auth",
            [
                ft.SafeArea(
                    content=ft.Container(
                        content=auth_page,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                    expand=True,
                )
            ],
        )
        self.page.views.append(view)

    def _create_dashboard_view(self):
        """Create dashboard view."""
        if not self.current_user:
            # Redirect to auth if no user
            self.page.go("/auth")
            return

        dashboard = DashboardPage(
            user_info=self.current_user,
            on_sign_out=self._handle_sign_out,
        )

        view = ft.View(
            "/dashboard",
            [
                ft.SafeArea(
                    content=ft.Container(
                        content=dashboard,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                    expand=True,
                )
            ],
        )
        self.page.views.append(view)

    def _start_auth_server(self):
        """Start the authentication server."""
        try:
            self.auth_server = start_auth_server()
            # Register cleanup on exit
            atexit.register(self._cleanup)
        except Exception as e:
            self._show_error(f"Failed to start authentication server: {str(e)}")

    def _cleanup(self):
        """Clean up resources on exit."""
        if self.auth_server:
            stop_auth_server()

    def _handle_auth_success(self, user_info: Dict[str, Any]):
        """Handle successful authentication."""
        self.current_user = user_info
        # Navigate to dashboard using Flet's routing
        self.page.go("/dashboard")

    def _handle_auth_error(self, error_message: str):
        """Handle authentication error."""
        self._show_error(f"Authentication failed: {error_message}")

    def _handle_sign_out(self):
        """Handle user sign out."""
        self.current_user = None
        # Navigate back to auth using Flet's routing
        self.page.go("/auth")

    def _show_error(self, message: str):
        """Show error message to user."""
        if hasattr(self.page, "snack_bar"):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED_400,
                duration=5000,
            )
            self.page.snack_bar.open = True
            self.page.update()


def main(page: ft.Page):
    """
    Main application function for Tide.
    Sets up the application with authentication and dashboard.
    """
    TideApp(page)


if __name__ == "__main__":
    # Run the Flet application
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
