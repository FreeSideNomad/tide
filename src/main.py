"""
Tide - Safety-First DBT AI Assistant
Main application entry point.

SECURITY REQUIREMENTS (from CLAUDE.md):
- MANDATORY: Follow https://flet.dev/docs/cookbook/authentication/ exactly
- Safety-first architecture prioritizing user wellbeing
- Complete audit trail for safety monitoring
- No custom authentication solutions allowed

This module implements secure Google authentication using Flet's official patterns.
"""

import logging
import flet as ft
from src.auth.flet_auth_handlers import AuthenticatedApp
from src.auth.flet_auth_ui import AuthenticationPage
from src.auth.route_protection import setup_route_protection, AuthGuard

# Configure logging for security audit trail
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TideApp:
    """
    Main Tide application with secure Flet authentication.

    Security Features:
    - Google OAuth using Flet's official patterns
    - Token encryption for client storage
    - Route protection with authentication guards
    - Complete audit logging
    - Safety-first design principles
    """

    def __init__(self, page: ft.Page):
        """
        Initialize Tide application with authentication.

        Args:
            page: Flet page instance
        """
        self.page = page
        self.current_user = None

        # Configure page properties
        self._configure_page()

        # Initialize secure authentication
        self._initialize_authentication()

        # Set up route protection
        self._setup_route_protection()

        # Initialize navigation
        self._setup_navigation()

        # Start the application
        self._start_application()

        logger.info("✅ Tide application initialized with secure authentication")

    def _configure_page(self):
        """Configure page properties following security best practices."""
        self.page.title = "Tide - DBT AI Assistant"
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.center()
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.accessibility = True

        # Store reference to auth config for later use
        # Authentication will be set up in _initialize_authentication method

        logger.info("✅ Page configuration completed")

    def _initialize_authentication(self):
        """Initialize secure authentication using Flet patterns."""
        try:
            # Create authenticated app handler
            self.auth_handler = AuthenticatedApp(
                page=self.page,
                on_auth_success=self._handle_auth_success,
                on_auth_failure=self._handle_auth_failure,
                on_logout=self._handle_logout,
            )

            # Create authentication guard for UI components
            self.auth_guard = AuthGuard(self.auth_handler)

            logger.info("✅ Secure authentication initialized")

        except Exception as error:
            logger.error(f"❌ Authentication initialization failed: {error}")
            self._show_error_page(
                "Authentication setup failed. Please check your configuration."
            )

    def _setup_route_protection(self):
        """Set up comprehensive route protection."""
        try:
            # Define protected routes following safety-first principles
            protected_routes = [
                "/dashboard",
                "/profile",
                "/dbt-skills",
                "/safety-plan",
                "/crisis-support",
            ]

            # Configure route protection
            self.route_protector = setup_route_protection(
                page=self.page,
                auth_handler=self.auth_handler,
                protected_routes=protected_routes,
            )

            logger.info("✅ Route protection configured")

        except Exception as error:
            logger.error(f"❌ Route protection setup failed: {error}")

    def _setup_navigation(self):
        """Set up navigation with authentication-aware routing."""
        self.page.on_route_change = self._handle_route_change
        self.page.on_view_pop = self._handle_view_pop

        logger.info("✅ Navigation handlers configured")

    def _start_application(self):
        """Start the application with appropriate initial route."""
        # Check if user is already authenticated
        if self.auth_handler.is_authenticated():
            logger.info("✅ User already authenticated, navigating to dashboard")
            self.page.go("/dashboard")
        else:
            logger.info("ℹ️ User not authenticated, showing authentication page")
            self.page.go("/auth")

    def _handle_route_change(self, e):
        """
        Handle route changes with authentication validation.

        Args:
            e: Route change event

        Security: Validates authentication before allowing route access
        """
        try:
            route = e.route if hasattr(e, "route") else self.page.route
            logger.info(f"🔀 Route change requested: {route}")

            # Clear previous views
            self.page.views.clear()

            # Handle different routes
            if route == "/auth":
                self._show_auth_page()
            elif route == "/dashboard":
                self._show_dashboard_page()
            elif route == "/" or route == "":
                self._show_landing_page()
            else:
                self._show_not_found_page()

            self.page.update()

        except Exception as error:
            logger.error(f"❌ Route change handling failed: {error}")
            self._show_error_page("Navigation error occurred.")

    def _handle_view_pop(self, e):
        """Handle back navigation."""
        try:
            self.page.views.pop()
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        except Exception as error:
            logger.error(f"❌ View pop handling failed: {error}")

    def _show_auth_page(self):
        """Show authentication page with Google Sign-In."""
        auth_page = AuthenticationPage(
            page=self.page,
            on_auth_success=self._handle_auth_success,
        )

        view = ft.View(
            route="/auth",
            controls=[auth_page],
            scroll=ft.ScrollMode.AUTO,
        )

        self.page.views.append(view)
        logger.info("✅ Authentication page displayed")

    def _show_dashboard_page(self):
        """Show dashboard page for authenticated users."""
        # Check authentication before showing dashboard
        if not self.auth_handler.require_authentication():
            return

        user = self.auth_handler.get_current_user()

        # Create dashboard content with user info
        user_info_display = self.auth_guard.create_user_info_display()

        dashboard_content = ft.Column(
            controls=[
                # Header with user info
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                "Tide Dashboard",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                            ),
                            user_info_display,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.Padding(0, 0, 0, 20),
                ),
                # Welcome message with safety-first principles
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"Welcome back, {user.get('name', 'User')}!",
                                size=20,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                "🛡️ Your safety comes first. Access evidence-based DBT skills "
                                "with built-in safety protocols.",
                                size=14,
                                color=ft.Colors.GREY_700,
                            ),
                        ],
                        spacing=8,
                    ),
                    bgcolor=ft.Colors.BLUE_50,
                    border=ft.Border(
                        top=ft.BorderSide(1, ft.Colors.BLUE_200),
                        right=ft.BorderSide(1, ft.Colors.BLUE_200),
                        bottom=ft.BorderSide(1, ft.Colors.BLUE_200),
                        left=ft.BorderSide(1, ft.Colors.BLUE_200),
                    ),
                    border_radius=ft.BorderRadius(8, 8, 8, 8),
                    padding=ft.Padding(16, 12, 16, 12),
                ),
                ft.Container(height=20),
                # Dashboard features (placeholder for future implementation)
                ft.Text(
                    "🚧 Dashboard features coming soon:",
                    size=16,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            "• Safety Plan Setup", size=14, color=ft.Colors.GREY_700
                        ),
                        ft.Text(
                            "• DBT Skills Access", size=14, color=ft.Colors.GREY_700
                        ),
                        ft.Text(
                            "• Crisis Support Resources",
                            size=14,
                            color=ft.Colors.GREY_700,
                        ),
                        ft.Text(
                            "• Progress Tracking", size=14, color=ft.Colors.GREY_700
                        ),
                    ],
                    spacing=4,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=16,
        )

        view = ft.View(
            route="/dashboard",
            controls=[
                ft.Container(
                    content=dashboard_content,
                    padding=ft.Padding(20, 20, 20, 20),
                )
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        self.page.views.append(view)
        logger.info(f"✅ Dashboard displayed for user: {user.get('email', 'unknown')}")

    def _show_landing_page(self):
        """Show landing page with authentication check."""
        # Check if user is authenticated and redirect to dashboard
        if self.auth_handler.is_authenticated():
            self.page.go("/dashboard")
            return

        # Show landing page for non-authenticated users
        landing_content = ft.Column(
            controls=[
                ft.Icon(
                    name=ft.Icons.PSYCHOLOGY,
                    size=64,
                    color=ft.Colors.BLUE_600,
                ),
                ft.Container(height=20),
                ft.Text(
                    "Welcome to Tide",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Your Safety-First DBT AI Assistant",
                    size=18,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),
                ft.Text(
                    "Access personalized DBT skills to improve emotional regulation "
                    "and interpersonal effectiveness.",
                    size=14,
                    color=ft.Colors.GREY_700,
                    text_align=ft.TextAlign.CENTER,
                    width=400,
                ),
                ft.Container(height=40),
                ft.ElevatedButton(
                    text="Get Started",
                    on_click=lambda e: self.page.go("/auth"),
                    icon=ft.Icons.ARROW_FORWARD,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

        view = ft.View(
            route="/",
            controls=[
                ft.Container(
                    content=landing_content,
                    alignment=ft.alignment.center,
                    expand=True,
                )
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        self.page.views.append(view)
        logger.info("✅ Landing page displayed")

    def _show_not_found_page(self):
        """Show 404 not found page."""
        not_found_content = ft.Column(
            controls=[
                ft.Icon(
                    name=ft.Icons.ERROR_OUTLINE,
                    size=64,
                    color=ft.Colors.ORANGE_600,
                ),
                ft.Text(
                    "Page Not Found",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "The page you're looking for doesn't exist.",
                    size=16,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    text="Go Home",
                    on_click=lambda e: self.page.go("/"),
                    icon=ft.Icons.HOME,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        )

        view = ft.View(
            route="/404",
            controls=[
                ft.Container(
                    content=not_found_content,
                    alignment=ft.alignment.center,
                    expand=True,
                )
            ],
        )

        self.page.views.append(view)

    def _show_error_page(self, error_message: str):
        """Show error page with message."""
        error_content = ft.Column(
            controls=[
                ft.Icon(
                    name=ft.Icons.ERROR,
                    size=64,
                    color=ft.Colors.RED_600,
                ),
                ft.Text(
                    "Application Error",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    error_message,
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    text="Retry",
                    on_click=lambda e: self.page.go("/"),
                    icon=ft.Icons.REFRESH,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        )

        view = ft.View(
            route="/error",
            controls=[
                ft.Container(
                    content=error_content,
                    alignment=ft.alignment.center,
                    expand=True,
                )
            ],
        )

        self.page.views.append(view)
        self.page.update()

    def _handle_auth_success(self, user_data: dict):
        """
        Handle successful authentication.

        Args:
            user_data: User information from OAuth provider

        Security: Updates current user and navigates to dashboard
        """
        self.current_user = user_data
        logger.info(
            f"✅ Authentication success handled for: {user_data.get('email', 'unknown')}"
        )

        # Navigate to dashboard
        self.page.go("/dashboard")

    def _handle_auth_failure(self, error_message: str):
        """
        Handle authentication failure.

        Args:
            error_message: Error description

        Security: Logs failure and shows user-friendly message
        """
        logger.error(f"❌ Authentication failure handled: {error_message}")
        # Authentication page will handle showing error to user

    def _handle_logout(self):
        """
        Handle user logout.

        Security: Clears current user and navigates to landing page
        """
        self.current_user = None
        logger.info("✅ Logout handled successfully")

        # Navigate to landing page
        self.page.go("/")


def main(page: ft.Page):
    """
    Main application function for Tide.
    Sets up the application with secure Flet authentication.

    Args:
        page: Flet page instance

    Security: Initializes secure authentication following Flet cookbook patterns
    """
    try:
        TideApp(page)
    except Exception as error:
        logger.error(f"❌ Application initialization failed: {error}")

        # Show basic error page
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            name=ft.Icons.ERROR,
                            size=64,
                            color=ft.Colors.RED_600,
                        ),
                        ft.Text(
                            "Application Startup Error",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Failed to initialize the application. Please check your configuration.",
                            size=16,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )


if __name__ == "__main__":
    # Run the Flet application with secure authentication
    logger.info("🚀 Starting Tide application with secure authentication")
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000)
