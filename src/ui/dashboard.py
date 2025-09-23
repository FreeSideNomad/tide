"""
Dashboard UI components for authenticated users.
Provides the main application interface after successful authentication.
"""

import flet as ft
from typing import Optional, Callable


class DashboardPage(ft.Column):
    """
    Main dashboard page for authenticated users.
    Displays user information and navigation to DBT skills.
    """

    def __init__(
        self,
        user_info: Optional[dict] = None,
        on_sign_out: Optional[Callable] = None,
        **kwargs,
    ):
        """
        Initialize dashboard page.

        Args:
            user_info: Dictionary containing user information from OAuth
            on_sign_out: Callback function for sign out action
        """
        self.user_info = user_info or {}
        self.on_sign_out = on_sign_out

        # Page header with user info
        header = self._create_header()

        # Main content area
        content = self._create_content()

        # Navigation/actions
        actions = self._create_actions()

        super().__init__(
            controls=[
                header,
                ft.Divider(),
                content,
                ft.Container(height=20),  # Spacing
                actions,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            **kwargs,
        )

    def _create_header(self) -> ft.Container:
        """Create the header section with user info and sign out."""
        user_name = self.user_info.get("name", "User")
        user_email = self.user_info.get("email", "")

        # Sign out button
        sign_out_button = ft.IconButton(
            icon=ft.Icons.LOGOUT,
            tooltip="Sign out",
            on_click=self._handle_sign_out,
        )

        header_content = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            f"Welcome, {user_name}",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                        (
                            ft.Text(
                                user_email,
                                size=14,
                                color=ft.Colors.GREY_600,
                            )
                            if user_email
                            else ft.Container()
                        ),
                    ],
                    spacing=5,
                ),
                sign_out_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            content=header_content,
            width=600,
            padding=20,
        )

    def _create_content(self) -> ft.Container:
        """Create the main content area."""
        content = ft.Column(
            controls=[
                ft.Text(
                    "Tide - DBT AI Assistant",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Your safety-first DBT skills companion",
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=30),  # Spacing
                # Feature cards (placeholder for future DBT modules)
                ft.Row(
                    controls=[
                        self._create_feature_card(
                            "Distress Tolerance",
                            "Crisis survival skills and distress management",
                            ft.Icons.CRISIS_ALERT,
                            coming_soon=False,
                        ),
                        self._create_feature_card(
                            "Mindfulness",
                            "Present moment awareness and grounding techniques",
                            ft.Icons.SELF_IMPROVEMENT,
                            coming_soon=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Container(height=20),  # Spacing
                ft.Row(
                    controls=[
                        self._create_feature_card(
                            "Emotion Regulation",
                            "Managing difficult emotions effectively",
                            ft.Icons.FAVORITE,
                            coming_soon=True,
                        ),
                        self._create_feature_card(
                            "Interpersonal Effectiveness",
                            "Building healthy relationships and communication",
                            ft.Icons.PEOPLE,
                            coming_soon=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        return ft.Container(
            content=content,
            width=600,
        )

    def _create_feature_card(
        self, title: str, description: str, icon: str, coming_soon: bool = False
    ) -> ft.Container:
        """Create a feature card for DBT modules."""
        card_content = ft.Column(
            controls=[
                ft.Icon(
                    icon,
                    size=40,
                    color=ft.Colors.BLUE_600 if not coming_soon else ft.Colors.GREY_400,
                ),
                ft.Text(
                    title,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    description,
                    size=12,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=10),  # Spacing
                ft.ElevatedButton(
                    text="Start" if not coming_soon else "Coming Soon",
                    on_click=self._handle_feature_click if not coming_soon else None,
                    disabled=coming_soon,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        return ft.Container(
            content=card_content,
            width=250,
            height=200,
            padding=20,
            border_radius=ft.border_radius.all(12),
            border=ft.border.all(1, ft.Colors.GREY_300),
            bgcolor=ft.Colors.WHITE if not coming_soon else ft.Colors.GREY_50,
        )

    def _create_actions(self) -> ft.Container:
        """Create action buttons."""
        actions = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Safety Plan",
                    icon=ft.Icons.SHIELD,
                    on_click=self._handle_safety_plan,
                    style=ft.ButtonStyle(
                        bgcolor=ft.MaterialState.all(ft.Colors.RED_600),
                        color=ft.MaterialState.all(ft.Colors.WHITE),
                    ),
                ),
                ft.OutlinedButton(
                    text="Profile Settings",
                    icon=ft.Icons.SETTINGS,
                    on_click=self._handle_settings,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        return ft.Container(
            content=actions,
            width=600,
        )

    def _handle_feature_click(self, e):
        """Handle feature card click."""
        # TODO: Navigate to specific DBT module
        if hasattr(self, "page") and self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Distress Tolerance module coming soon!"),
                bgcolor=ft.Colors.BLUE_400,
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _handle_safety_plan(self, e):
        """Handle safety plan button click."""
        # TODO: Navigate to safety plan setup/review
        if hasattr(self, "page") and self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Safety plan setup coming soon!"),
                bgcolor=ft.Colors.ORANGE_400,
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _handle_settings(self, e):
        """Handle settings button click."""
        # TODO: Navigate to profile settings
        if hasattr(self, "page") and self.page:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Profile settings coming soon!"),
                bgcolor=ft.Colors.GREEN_400,
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _handle_sign_out(self, e):
        """Handle sign out button click."""
        if self.on_sign_out:
            self.on_sign_out()
