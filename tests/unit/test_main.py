"""
Unit tests for main application functionality.
"""

import flet as ft
from unittest.mock import patch
from src.main import main, TideApp


class TestMainApp:
    """Test the main Flet application."""

    def test_main_function_exists(self):
        """Test that main function is defined."""
        assert callable(main)

    def test_main_accepts_page_parameter(self, mock_flet_page):
        """Test that main function accepts a page parameter."""
        # Should not raise an exception
        main(mock_flet_page)

    def test_main_creates_tide_app(self, mock_flet_page):
        """Test that main function creates TideApp instance."""
        with patch("src.main.TideApp") as mock_tide_app:
            main(mock_flet_page)

            # Verify TideApp was instantiated with the page
            mock_tide_app.assert_called_once_with(mock_flet_page)


class TestTideApp:
    """Test the TideApp class initialization and basic functionality."""

    def test_tide_app_initializes_with_page(self, mock_flet_page):
        """Test TideApp initialization with page setup."""
        app = TideApp(mock_flet_page)

        assert app.page == mock_flet_page
        # Verify page configuration was called
        assert mock_flet_page.title == "Tide - DBT AI Assistant"
        assert mock_flet_page.window.width == 800
        assert mock_flet_page.window.height == 600
        assert mock_flet_page.theme_mode == ft.ThemeMode.LIGHT
        assert mock_flet_page.padding == 20
        assert mock_flet_page.accessibility is True

    def test_main_centers_window(self, mock_flet_page):
        """Test that TideApp centers the window."""
        TideApp(mock_flet_page)

        # Verify window.center was called
        mock_flet_page.window.center.assert_called()

    def test_main_shows_content(self, mock_flet_page):
        """Test that TideApp shows main page content."""
        TideApp(mock_flet_page)

        # Verify content was added to page
        mock_flet_page.add.assert_called_once()
