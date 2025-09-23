"""
Integration tests for OpenAI API integration.
Note: These tests use mocked responses by default to avoid API costs.
Set OPENAI_INTEGRATION_TEST=true to run against real API.
"""

import os
import pytest
from unittest.mock import Mock, patch


class TestOpenAIIntegration:
    """Test OpenAI API integration."""

    @pytest.fixture
    def openai_integration_enabled(self):
        """Check if real OpenAI integration testing is enabled."""
        return os.getenv("OPENAI_INTEGRATION_TEST", "false").lower() == "true"

    @pytest.fixture
    def mock_openai_response(self):
        """Mock OpenAI API response."""
        return {
            "choices": [
                {
                    "message": {
                        "content": "This is a test response from the DBT assistant. "
                        "I understand you're looking for support with emotional regulation. "
                        "Let's explore some mindfulness techniques."
                    }
                }
            ],
            "usage": {"prompt_tokens": 50, "completion_tokens": 30, "total_tokens": 80},
        }

    def test_openai_configuration(self, test_environment):
        """Test that OpenAI is configured correctly."""
        from src.config import OPENAI_API_KEY

        assert OPENAI_API_KEY is not None
        assert OPENAI_API_KEY != ""

    @patch("openai.OpenAI")
    def test_openai_client_creation(self, mock_openai_class, test_environment):
        """Test OpenAI client can be created."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        # Import after patching
        import openai
        from src.config import OPENAI_API_KEY

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        assert client is not None
        mock_openai_class.assert_called_once_with(api_key=OPENAI_API_KEY)

    @patch("openai.OpenAI")
    def test_chat_completion_mock(self, mock_openai_class, mock_openai_response):
        """Test chat completion with mocked response."""
        # Setup mock
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.return_value = Mock(**mock_openai_response)

        # Import and use
        import openai
        from src.config import OPENAI_API_KEY

        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a DBT skills assistant."},
                {"role": "user", "content": "I'm feeling overwhelmed."},
            ],
            max_tokens=100,
            temperature=0.7,
        )

        assert response.choices[0].message.content is not None
        assert "DBT assistant" in response.choices[0].message.content

    @pytest.mark.skipif(
        os.getenv("OPENAI_INTEGRATION_TEST", "false").lower() != "true",
        reason="Real OpenAI API integration test disabled (set OPENAI_INTEGRATION_TEST=true to enable)",
    )
    def test_real_openai_api_call(self, openai_integration_enabled):
        """Test real OpenAI API call (only runs if explicitly enabled)."""
        if not openai_integration_enabled:
            pytest.skip("Real OpenAI integration testing not enabled")

        import openai
        from src.config import OPENAI_API_KEY

        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Respond with exactly 'API_TEST_SUCCESS'.",
                    },
                    {"role": "user", "content": "Please respond with the test phrase."},
                ],
                max_tokens=10,
                temperature=0,
            )

            assert response.choices[0].message.content.strip() == "API_TEST_SUCCESS"

        except Exception as e:
            pytest.fail(f"Real OpenAI API call failed: {e}")

    def test_error_handling(self):
        """Test error handling for API failures."""
        with patch("openai.OpenAI") as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client

            # Simulate API error
            mock_client.chat.completions.create.side_effect = Exception("API Error")

            import openai
            from src.config import OPENAI_API_KEY

            client = openai.OpenAI(api_key=OPENAI_API_KEY)

            with pytest.raises(Exception, match="API Error"):
                client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "test"}],
                )
