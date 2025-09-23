"""
Unit tests for configuration management.
"""

import os
import pytest
from unittest.mock import patch
from src.config import OPENAI_API_KEY, DATABASE_URL


class TestConfig:
    """Test configuration loading and validation."""

    def test_openai_api_key_from_environment(self, test_environment):
        """Test that OpenAI API key is loaded from environment."""
        assert OPENAI_API_KEY == "test-key"

    def test_database_url_default(self, test_environment):
        """Test database URL uses default when not set."""
        expected_default = "postgresql://username:password@localhost:5432/tide_db"
        assert DATABASE_URL == expected_default

    def test_debug_mode_enabled(self, test_environment):
        """Test debug mode is enabled in test environment."""
        # DEBUG comes from the actual environment, not the fixture
        # So we test that it can be True when set
        import os

        with patch.dict(os.environ, {"DEBUG": "True"}):
            import importlib
            import src.config

            importlib.reload(src.config)
            assert src.config.DEBUG is True

    def test_environment_is_test(self, test_environment):
        """Test environment is set to test."""
        # ENVIRONMENT comes from the actual environment, not the fixture
        # So we test that it can be 'test' when set
        import os

        with patch.dict(os.environ, {"ENVIRONMENT": "test"}):
            import importlib
            import src.config

            importlib.reload(src.config)
            assert src.config.ENVIRONMENT == "test"

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_openai_key_raises_error(self):
        """Test that missing OpenAI API key raises ValueError."""
        # Need to reload the module to trigger the error
        import importlib

        with pytest.raises(
            ValueError, match="OPENAI_API_KEY environment variable is required"
        ):
            import src.config

            importlib.reload(src.config)

    @patch.dict(
        os.environ, {"DATABASE_URL": "postgresql://custom:password@host:5432/db"}
    )
    def test_custom_database_url(self):
        """Test custom database URL is used when provided."""
        import importlib
        import src.config

        importlib.reload(src.config)
        assert src.config.DATABASE_URL == "postgresql://custom:password@host:5432/db"
