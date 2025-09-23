"""
Unit tests for main application functionality.
"""

import flet as ft
from unittest.mock import patch
from src.main import main


class TestMainApp:
    """Test the main Flet application."""

    def test_main_function_exists(self):
        """Test that main function is defined."""
        assert callable(main)

    @patch("src.ui.auth_components.AuthenticationPage")
    def test_main_accepts_page_parameter(self, mock_auth_page, mock_flet_page):
        """Test that main function accepts a page parameter."""
        # Should not raise an exception
        main(mock_flet_page)

    @patch("src.ui.auth_components.AuthenticationPage")
    def test_main_adds_elements_to_page(self, mock_auth_page, mock_flet_page):
        """Test that main function adds UI elements to the page."""
        main(mock_flet_page)

        # Verify that page.add was called
        assert mock_flet_page.add.called

    @patch("src.ui.auth_components.AuthenticationPage")
    def test_main_sets_page_properties(self, mock_auth_page, mock_flet_page):
        """Test that main function sets correct page properties."""
        main(mock_flet_page)

        # Verify page properties are set
        assert mock_flet_page.title == "Tide - DBT AI Assistant"
        assert mock_flet_page.window.width == 800
        assert mock_flet_page.window.height == 600
        assert mock_flet_page.theme_mode == ft.ThemeMode.LIGHT
        assert mock_flet_page.padding == 20
        assert mock_flet_page.accessibility is True

    @patch("src.main.AuthenticationPage")
    def test_main_creates_auth_page(self, mock_auth_page_class, mock_flet_page):
        """Test that main function creates authentication page."""
        main(mock_flet_page)

        # Verify AuthenticationPage was instantiated
        mock_auth_page_class.assert_called_once()

    @patch("src.ui.auth_components.AuthenticationPage")
    def test_main_updates_page(self, mock_auth_page, mock_flet_page):
        """Test that main function calls page.update()."""
        main(mock_flet_page)

        # Verify page.update was called
        mock_flet_page.update.assert_called()

    @patch("src.ui.auth_components.AuthenticationPage")
    def test_main_centers_window(self, mock_auth_page, mock_flet_page):
        """Test that main function centers the window."""
        main(mock_flet_page)

        # Verify window.center was called
        mock_flet_page.window.center.assert_called()
