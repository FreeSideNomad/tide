"""
Tide - Safety-First DBT AI Assistant
Main application entry point with Google OAuth authentication.
"""

import flet as ft
from src.ui.auth_components import AuthenticationPage


def main(page: ft.Page):
    """
    Main application function for Tide.
    Sets up the page and displays the authentication interface.
    """
    # Configure page properties
    page.title = "Tide - DBT AI Assistant"
    page.window.width = 800
    page.window.height = 600
    page.window.center()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # Enable semantic properties for accessibility
    page.accessibility = True

    # Create authentication page
    auth_page = AuthenticationPage()

    # Add page content with proper safe area
    page.add(
        ft.SafeArea(
            content=ft.Container(
                content=auth_page,
                alignment=ft.alignment.center,
                expand=True,
            ),
            expand=True,
        )
    )

    # Update page
    page.update()


if __name__ == "__main__":
    # Run the Flet application
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
