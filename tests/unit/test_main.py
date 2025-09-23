"""
Unit tests for main application functionality.
"""

import flet as ft
from unittest.mock import patch, Mock
from src.main import main, TideApp


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

    @patch("src.main.start_auth_server")
    @patch("src.ui.auth_components.AuthenticationPage")
    def test_main_sets_up_navigation(self, mock_auth_page, mock_auth_server, mock_flet_page):
        """Test that main function sets up route-based navigation."""
        main(mock_flet_page)

        # Verify that navigation handlers are set
        assert mock_flet_page.on_route_change is not None
        assert mock_flet_page.on_view_pop is not None

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

    @patch("src.main.start_auth_server")
    def test_main_navigates_to_auth(self, mock_auth_server, mock_flet_page):
        """Test that main function navigates to authentication route."""
        main(mock_flet_page)

        # Verify initial navigation to auth route
        mock_flet_page.go.assert_called_with("/auth")

    @patch("src.main.start_auth_server")
    def test_main_creates_tide_app(self, mock_auth_server, mock_flet_page):
        """Test that main function creates TideApp instance."""
        with patch("src.main.TideApp") as mock_tide_app:
            main(mock_flet_page)

            # Verify TideApp was instantiated with the page
            mock_tide_app.assert_called_once_with(mock_flet_page)

    @patch("src.ui.auth_components.AuthenticationPage")
    def test_main_centers_window(self, mock_auth_page, mock_flet_page):
        """Test that main function centers the window."""
        main(mock_flet_page)

        # Verify window.center was called
        mock_flet_page.window.center.assert_called()


class TestTideApp:
    """Test the TideApp class navigation and routing."""

    @patch("src.main.start_auth_server")
    def test_tide_app_initializes_with_page(self, mock_auth_server, mock_flet_page):
        """Test TideApp initialization with page setup."""
        app = TideApp(mock_flet_page)

        assert app.page == mock_flet_page
        assert app.current_user is None
        assert mock_flet_page.on_route_change is not None
        assert mock_flet_page.on_view_pop is not None

    @patch("src.main.start_auth_server")
    @patch("src.ui.auth_components.AuthenticationPage")
    def test_route_change_to_auth(self, mock_auth_page, mock_auth_server, mock_flet_page):
        """Test route change to authentication page."""
        mock_flet_page.route = "/auth"
        app = TideApp(mock_flet_page)

        # Simulate route change
        app._route_change(None)

        # Verify views were cleared and auth view created
        mock_flet_page.views.clear.assert_called()
        mock_flet_page.views.append.assert_called()
        mock_flet_page.update.assert_called()

    @patch("src.main.start_auth_server")
    @patch("src.main.DashboardPage")
    def test_route_change_to_dashboard_with_user(self, mock_dashboard, mock_auth_server, mock_flet_page):
        """Test route change to dashboard when user is authenticated."""
        mock_flet_page.route = "/dashboard"
        app = TideApp(mock_flet_page)
        app.current_user = {"user_id": "test", "name": "Test User"}

        # Simulate route change
        app._route_change(None)

        # Verify dashboard was created
        mock_dashboard.assert_called_once()
        mock_flet_page.views.append.assert_called()

    @patch("src.main.start_auth_server")
    def test_route_change_to_dashboard_without_user_redirects(self, mock_auth_server, mock_flet_page):
        """Test route change to dashboard without user redirects to auth."""
        mock_flet_page.route = "/dashboard"
        app = TideApp(mock_flet_page)
        app.current_user = None

        # Simulate route change
        app._route_change(None)

        # Verify redirect to auth
        mock_flet_page.go.assert_called_with("/auth")

    @patch("src.main.start_auth_server")
    def test_auth_success_navigates_to_dashboard(self, mock_auth_server, mock_flet_page):
        """Test successful authentication navigates to dashboard."""
        app = TideApp(mock_flet_page)
        user_info = {"user_id": "test", "name": "Test User"}

        app._handle_auth_success(user_info)

        assert app.current_user == user_info
        mock_flet_page.go.assert_called_with("/dashboard")

    @patch("src.main.start_auth_server")
    def test_sign_out_navigates_to_auth(self, mock_auth_server, mock_flet_page):
        """Test sign out clears user and navigates to auth."""
        app = TideApp(mock_flet_page)
        app.current_user = {"user_id": "test"}

        app._handle_sign_out()

        assert app.current_user is None
        mock_flet_page.go.assert_called_with("/auth")
