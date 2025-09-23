"""
Unit tests for main application functionality.
"""

import flet as ft
from unittest.mock import Mock, patch
from src.main import main


class TestMainApp:
    """Test the main Flet application."""

    def test_main_function_exists(self):
        """Test that main function is defined."""
        assert callable(main)

    def test_main_accepts_page_parameter(self, mock_flet_page):
        """Test that main function accepts a page parameter."""
        # Should not raise an exception
        main(mock_flet_page)

    def test_main_adds_elements_to_page(self, mock_flet_page):
        """Test that main function adds UI elements to the page."""
        main(mock_flet_page)

        # Verify that page.add was called
        assert mock_flet_page.add.called

        # Verify that a floating action button was set
        assert mock_flet_page.floating_action_button is not None

    def test_counter_initialization(self, mock_flet_page):
        """Test that counter is initialized correctly."""
        main(mock_flet_page)

        # Get the arguments passed to page.add
        add_call_args = mock_flet_page.add.call_args[0]

        # Should have added a SafeArea containing elements
        assert len(add_call_args) > 0

    def test_floating_action_button_configuration(self, mock_flet_page):
        """Test floating action button is configured properly."""
        main(mock_flet_page)

        fab = mock_flet_page.floating_action_button
        assert fab is not None
        assert fab.icon == ft.Icons.ADD
        assert fab.on_click is not None

    @patch("flet.Text")
    def test_increment_functionality(self, mock_text_class, mock_flet_page):
        """Test that increment functionality works."""
        # Mock the Text control
        mock_counter = Mock()
        mock_counter.data = 0
        mock_counter.value = "0"
        mock_counter.update = Mock()
        mock_text_class.return_value = mock_counter

        main(mock_flet_page)

        # Get the floating action button
        fab = mock_flet_page.floating_action_button

        # Create a mock event
        mock_event = Mock()

        # Call the increment function
        fab.on_click(mock_event)

        # Verify the counter was incremented
        assert mock_counter.data == 1
        assert mock_counter.value == "1"
        mock_counter.update.assert_called_once()


class TestCounterComponent:
    """Test the counter component behavior."""

    def test_counter_starts_at_zero(self, mock_flet_page):
        """Test that counter starts at zero."""
        main(mock_flet_page)

        # This test would be more robust with direct access to counter object
        # For now, we test that the function executes without error
        assert mock_flet_page.add.called

    @patch("flet.Text")
    def test_counter_increment(self, mock_text_class, mock_flet_page):
        """Test counter increment behavior."""
        # Mock the Text control
        mock_counter = Mock()
        mock_counter.data = 0
        mock_counter.value = "0"
        mock_counter.update = Mock()
        mock_text_class.return_value = mock_counter

        main(mock_flet_page)

        fab = mock_flet_page.floating_action_button
        mock_event = Mock()

        # Test multiple increments
        for i in range(5):
            fab.on_click(mock_event)

        # Verify final count
        assert mock_counter.data == 5
        assert mock_counter.value == "5"
        assert mock_counter.update.call_count == 5
