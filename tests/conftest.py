"""
Pytest configuration and shared fixtures for all test types.
"""

import os
import pytest
import tempfile
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import flet as ft


@pytest.fixture(scope="session")
def test_environment():
    """Set up test environment variables."""
    os.environ["OPENAI_API_KEY"] = "test-key"
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DEBUG"] = "True"
    yield
    # Cleanup not needed as these are environment variables


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing without API calls."""
    with patch("openai.OpenAI") as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        # Mock typical responses
        mock_instance.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="Test response"))]
        )

        yield mock_instance


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    db_url = f"sqlite:///{db_path}"

    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield SessionLocal, engine

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def mock_flet_page():
    """Mock Flet page for UI testing."""
    page = Mock(spec=ft.Page)
    page.add = Mock()
    page.update = Mock()
    page.remove = Mock()
    page.clean = Mock()
    page.go = Mock()
    page.width = 400
    page.height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    return page


@pytest.fixture
def sample_dbt_conversation():
    """Sample conversation data for testing."""
    return {
        "user_id": "test-user-123",
        "conversation_id": "conv-456",
        "messages": [
            {"role": "user", "content": "I'm feeling overwhelmed"},
            {
                "role": "assistant",
                "content": "Let's explore some distress tolerance skills",
            },
        ],
        "skill_category": "distress_tolerance",
        "crisis_indicators": [],
    }


@pytest.fixture
def sample_safety_plan():
    """Sample safety plan data for testing."""
    return {
        "user_id": "test-user-123",
        "warning_signs": ["Feeling hopeless", "Isolation"],
        "coping_strategies": ["Call friend", "Use breathing exercise"],
        "support_contacts": [
            {"name": "Emergency", "phone": "911"},
            {"name": "Crisis Line", "phone": "988"},
        ],
        "professional_contacts": [{"name": "Dr. Smith", "phone": "555-0123"}],
    }
