"""
Basic test to verify testing framework works.
"""


def test_basic_assertion():
    """Test that basic assertions work."""
    assert 1 + 1 == 2


def test_imports():
    """Test that key imports work."""
    import pytest
    import flet as ft

    assert pytest is not None
    assert ft is not None


def test_environment_setup():
    """Test basic environment setup."""
    import os

    # Check that we can access environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    assert openai_key is not None
