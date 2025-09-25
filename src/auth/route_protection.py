"""
Route Protection Patterns for Flet Authentication

SECURITY REQUIREMENTS (from CLAUDE.md):
- MANDATORY: Follow https://flet.dev/docs/cookbook/authentication/ exactly
- Safety-first architecture prioritizing user wellbeing
- Route protection using Flet's recommended patterns
- Complete audit trail for security monitoring

This module provides route protection and authentication guards.
"""

import logging
from typing import Callable, Optional, List
from functools import wraps
import flet as ft
from .flet_auth_handlers import AuthenticatedApp

# Configure logging for security audit trail
logger = logging.getLogger(__name__)


class RouteProtector:
    """
    Route protection system using Flet's authentication patterns.

    Security Features:
    - Authentication validation before route access
    - Automatic redirection for unauthenticated users
    - Route-based permission checking
    - Security audit logging
    """

    def __init__(self, auth_handler: AuthenticatedApp):
        """
        Initialize route protector.

        Args:
            auth_handler: Authenticated application handler instance
        """
        self.auth_handler = auth_handler
        self.protected_routes: List[str] = []
        self.public_routes: List[str] = ["/", "/auth"]

        logger.info("✅ Route protector initialized")

    def add_protected_route(self, route: str):
        """
        Add route to protection list.

        Args:
            route: Route path to protect

        Security: Logs route protection configuration
        """
        if route not in self.protected_routes:
            self.protected_routes.append(route)
            logger.info(f"🔒 Route protected: {route}")

    def add_public_route(self, route: str):
        """
        Add route to public access list.

        Args:
            route: Route path to allow public access
        """
        if route not in self.public_routes:
            self.public_routes.append(route)
            logger.info(f"🌐 Public route added: {route}")

    def is_route_protected(self, route: str) -> bool:
        """
        Check if route requires authentication.

        Args:
            route: Route path to check

        Returns:
            bool: True if route requires authentication
        """
        return route in self.protected_routes

    def is_route_public(self, route: str) -> bool:
        """
        Check if route allows public access.

        Args:
            route: Route path to check

        Returns:
            bool: True if route allows public access
        """
        return route in self.public_routes

    def check_route_access(self, route: str) -> bool:
        """
        Check if current user can access the specified route.

        Args:
            route: Route path to check access for

        Returns:
            bool: True if access is allowed

        Security: Validates authentication state and logs access attempts
        """
        # Allow access to public routes
        if self.is_route_public(route):
            logger.info(f"✅ Public route access granted: {route}")
            return True

        # Check authentication for protected routes
        if self.is_route_protected(route):
            if self.auth_handler.is_authenticated():
                user = self.auth_handler.get_current_user()
                logger.info(
                    f"✅ Protected route access granted for {user.get('email', 'unknown')}: {route}"
                )
                return True
            else:
                logger.warning(
                    f"❌ Protected route access denied (not authenticated): {route}"
                )
                return False

        # Default: allow access to unspecified routes (fail-open for flexibility)
        logger.info(f"✅ Unspecified route access granted: {route}")
        return True

    def protect_route_navigation(self, target_route: str) -> bool:
        """
        Protect route navigation with automatic redirection.

        Args:
            target_route: Route user is trying to navigate to

        Returns:
            bool: True if navigation should proceed

        Security: Redirects unauthenticated users to auth page
        """
        if self.check_route_access(target_route):
            return True

        # Redirect to authentication page
        logger.info(f"🔄 Redirecting to auth page from protected route: {target_route}")
        self.auth_handler.page.go("/auth")
        return False


def require_auth(auth_handler: AuthenticatedApp):
    """
    Decorator for functions that require authentication.

    Args:
        auth_handler: Authenticated application handler

    Returns:
        Decorator function for authentication requirement

    Security: Validates authentication before function execution
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not auth_handler.require_authentication():
                logger.warning(
                    f"❌ Authentication required for function: {func.__name__}"
                )
                return None

            user = auth_handler.get_current_user()
            logger.info(
                f"✅ Authenticated function access for {user.get('email', 'unknown')}: {func.__name__}"
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator


class AuthGuard:
    """
    Authentication guard for UI components and actions.

    Security Features:
    - Component-level authentication checks
    - Conditional UI rendering based on auth state
    - Action protection with user feedback
    """

    def __init__(self, auth_handler: AuthenticatedApp):
        """
        Initialize authentication guard.

        Args:
            auth_handler: Authenticated application handler instance
        """
        self.auth_handler = auth_handler

    def create_protected_component(
        self,
        component: ft.Control,
        auth_required_message: str = "Please sign in to access this feature",
        show_auth_prompt: bool = True,
    ) -> ft.Control:
        """
        Create protected UI component that requires authentication.

        Args:
            component: Flet control to protect
            auth_required_message: Message to show when auth required
            show_auth_prompt: Whether to show auth prompt or hide component

        Returns:
            ft.Control: Protected component or auth prompt

        Security: Conditionally renders based on authentication state
        """
        if self.auth_handler.is_authenticated():
            return component

        if show_auth_prompt:
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            name=ft.Icons.LOCK_OUTLINED,
                            size=32,
                            color=ft.Colors.GREY_400,
                        ),
                        ft.Text(
                            auth_required_message,
                            size=14,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.ElevatedButton(
                            text="Sign In",
                            on_click=lambda e: self.auth_handler.page.go("/auth"),
                            icon=ft.Icons.LOGIN,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                padding=ft.Padding(20, 20, 20, 20),
                alignment=ft.alignment.center,
            )
        else:
            # Return empty container if auth not available and prompt disabled
            return ft.Container()

    def create_user_info_display(self) -> Optional[ft.Control]:
        """
        Create user information display for authenticated users.

        Returns:
            Optional[ft.Control]: User info component or None if not authenticated

        Security: Only shows user info when properly authenticated
        """
        if not self.auth_handler.is_authenticated():
            return None

        user = self.auth_handler.get_current_user()
        if not user:
            return None

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=ft.Icons.ACCOUNT_CIRCLE,
                        size=24,
                        color=ft.Colors.BLUE_600,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                user.get("name", "User"),
                                size=14,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                user.get("email", ""),
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        spacing=2,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.LOGOUT,
                        tooltip="Sign Out",
                        on_click=lambda e: self.auth_handler.logout(),
                        icon_color=ft.Colors.GREY_600,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.Padding(8, 4, 8, 4),
            border_radius=ft.BorderRadius(8, 8, 8, 8),
            bgcolor=ft.Colors.GREY_50,
        )

    def protected_action(
        self, action: Callable, auth_required_callback: Optional[Callable] = None
    ) -> Callable:
        """
        Create protected action that requires authentication.

        Args:
            action: Action function to protect
            auth_required_callback: Callback when auth is required

        Returns:
            Callable: Protected action function

        Security: Validates authentication before executing action
        """

        def protected_wrapper(*args, **kwargs):
            if not self.auth_handler.is_authenticated():
                logger.warning(
                    f"❌ Authentication required for action: {action.__name__}"
                )
                if auth_required_callback:
                    auth_required_callback()
                else:
                    # Default: redirect to auth page
                    self.auth_handler.page.go("/auth")
                return None

            user = self.auth_handler.get_current_user()
            logger.info(
                f"✅ Protected action executed for {user.get('email', 'unknown')}: {action.__name__}"
            )
            return action(*args, **kwargs)

        return protected_wrapper


def setup_route_protection(
    page: ft.Page,
    auth_handler: AuthenticatedApp,
    protected_routes: Optional[List[str]] = None,
) -> RouteProtector:
    """
    Set up comprehensive route protection for the application.

    Args:
        page: Flet page instance
        auth_handler: Authenticated application handler
        protected_routes: List of routes to protect (default: common protected routes)

    Returns:
        RouteProtector: Configured route protector instance

    Security: Configures application-wide route protection
    """
    route_protector = RouteProtector(auth_handler)

    # Default protected routes (following CLAUDE.md safety-first principles)
    default_protected_routes = [
        "/dashboard",
        "/profile",
        "/dbt-skills",
        "/safety-plan",
        "/crisis-support",
    ]

    routes_to_protect = protected_routes or default_protected_routes

    # Add protected routes
    for route in routes_to_protect:
        route_protector.add_protected_route(route)

    # Set up route change handler with protection
    original_on_route_change = page.on_route_change

    def protected_route_change(e):
        target_route = e.route if hasattr(e, "route") else page.route

        # Check route protection
        if route_protector.protect_route_navigation(target_route):
            # Call original handler if navigation is allowed
            if original_on_route_change:
                original_on_route_change(e)
        # If navigation is blocked, protection handler already redirected

    page.on_route_change = protected_route_change

    logger.info(
        f"✅ Route protection configured for {len(routes_to_protect)} protected routes"
    )
    return route_protector
