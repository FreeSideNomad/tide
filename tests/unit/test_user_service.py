"""
Unit tests for UserService and database integration.
Tests user creation from OAuth data and database operations.
"""

import pytest
from unittest.mock import Mock

from src.services.user_service import UserService
from src.database.models import User, AuthenticationProvider
from src.database.repositories import UserRepository


class TestUserService:
    """Test suite for UserService operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_repository = Mock(spec=UserRepository)
        self.user_service = UserService(user_repository=self.mock_repository)

    def test_create_user_from_oauth_success(self):
        """Test successful user creation from OAuth data."""
        # Arrange
        oauth_data = {
            "id": "google_user_123",
            "email": "test@example.com",
            "name": "Test User",
            "picture": "https://example.com/photo.jpg",
        }

        mock_user = User(
            user_id="test_user_id",
            email_address="test@example.com",
            external_user_id="google_user_123",
            authentication_provider=AuthenticationProvider.GOOGLE,
            display_name="Test User",
            profile_image_url="https://example.com/photo.jpg",
        )

        self.mock_repository.find_by_external_user_id.return_value = None
        self.mock_repository.find_by_email.return_value = None
        self.mock_repository.create_from_oauth_profile.return_value = mock_user

        # Act
        result = self.user_service.create_user_from_oauth(
            oauth_data, AuthenticationProvider.GOOGLE
        )

        # Assert
        assert result == mock_user
        self.mock_repository.find_by_external_user_id.assert_called_once_with(
            "google_user_123", AuthenticationProvider.GOOGLE
        )
        self.mock_repository.find_by_email.assert_called_once_with("test@example.com")
        self.mock_repository.create_from_oauth_profile.assert_called_once_with(
            oauth_data, AuthenticationProvider.GOOGLE
        )

    def test_create_user_from_oauth_missing_email(self):
        """Test user creation fails with missing email."""
        # Arrange
        oauth_data = {
            "id": "google_user_123",
            "name": "Test User",
            # Missing email
        }

        # Act & Assert
        with pytest.raises(ValueError, match="OAuth data must include email address"):
            self.user_service.create_user_from_oauth(
                oauth_data, AuthenticationProvider.GOOGLE
            )

    def test_create_user_from_oauth_missing_user_id(self):
        """Test user creation fails with missing user ID."""
        # Arrange
        oauth_data = {
            "email": "test@example.com",
            "name": "Test User",
            # Missing id/sub
        }

        # Act & Assert
        with pytest.raises(ValueError, match="OAuth data must include user ID"):
            self.user_service.create_user_from_oauth(
                oauth_data, AuthenticationProvider.GOOGLE
            )

    def test_create_user_from_oauth_user_already_exists(self):
        """Test user creation fails when user already exists."""
        # Arrange
        oauth_data = {
            "id": "google_user_123",
            "email": "test@example.com",
            "name": "Test User",
        }

        existing_user = User(user_id="existing_id", external_user_id="google_user_123")
        self.mock_repository.find_by_external_user_id.return_value = existing_user

        # Act & Assert
        with pytest.raises(ValueError, match="User already exists with external ID"):
            self.user_service.create_user_from_oauth(
                oauth_data, AuthenticationProvider.GOOGLE
            )

    def test_create_user_from_oauth_email_already_registered(self):
        """Test user creation fails when email is already registered with different provider."""
        # Arrange
        oauth_data = {
            "id": "google_user_123",
            "email": "test@example.com",
            "name": "Test User",
        }

        existing_user = User(
            user_id="existing_id",
            email_address="test@example.com",
            authentication_provider=AuthenticationProvider.MICROSOFT,
        )

        self.mock_repository.find_by_external_user_id.return_value = None
        self.mock_repository.find_by_email.return_value = existing_user

        # Act & Assert
        with pytest.raises(ValueError, match="Email .* is already registered with"):
            self.user_service.create_user_from_oauth(
                oauth_data, AuthenticationProvider.GOOGLE
            )

    def test_get_or_create_user_existing_user(self):
        """Test getting existing user by external ID."""
        # Arrange
        oauth_data = {
            "id": "google_user_123",
            "email": "test@example.com",
            "name": "Test User",
        }

        existing_user = User(
            user_id="existing_id",
            external_user_id="google_user_123",
            authentication_provider=AuthenticationProvider.GOOGLE,
        )

        self.mock_repository.find_by_external_user_id.return_value = existing_user

        # Act
        result_user, is_new = self.user_service.get_or_create_user_from_oauth(
            oauth_data, AuthenticationProvider.GOOGLE
        )

        # Assert
        assert result_user == existing_user
        assert is_new is False
        self.mock_repository.update_last_active.assert_called_once_with("existing_id")

    def test_get_or_create_user_new_user(self):
        """Test creating new user when none exists."""
        # Arrange
        oauth_data = {
            "id": "google_user_123",
            "email": "test@example.com",
            "name": "Test User",
        }

        new_user = User(
            user_id="new_id",
            external_user_id="google_user_123",
            authentication_provider=AuthenticationProvider.GOOGLE,
        )

        self.mock_repository.find_by_external_user_id.return_value = None
        self.mock_repository.find_by_email.return_value = None
        self.mock_repository.create_from_oauth_profile.return_value = new_user

        # Act
        result_user, is_new = self.user_service.get_or_create_user_from_oauth(
            oauth_data, AuthenticationProvider.GOOGLE
        )

        # Assert
        assert result_user == new_user
        assert is_new is True
        self.mock_repository.create_from_oauth_profile.assert_called_once_with(
            oauth_data, AuthenticationProvider.GOOGLE
        )

    def test_update_profile_success(self):
        """Test successful profile update."""
        # Arrange
        user_id = "test_user_id"
        existing_user = User(
            user_id=user_id, display_name="Old Name", preferred_timezone="UTC"
        )

        self.mock_repository.find_by_id.return_value = existing_user
        self.mock_repository.save.return_value = existing_user

        profile_updates = {
            "display_name": "New Name",
            "preferred_timezone": "America/New_York",
        }

        # Act
        result = self.user_service.update_profile(user_id, profile_updates)

        # Assert
        assert result == existing_user
        assert existing_user.display_name == "New Name"
        assert existing_user.preferred_timezone == "America/New_York"
        self.mock_repository.save.assert_called_once_with(existing_user)

    def test_update_profile_user_not_found(self):
        """Test profile update when user doesn't exist."""
        # Arrange
        self.mock_repository.find_by_id.return_value = None

        # Act
        result = self.user_service.update_profile(
            "nonexistent_id", {"display_name": "New Name"}
        )

        # Assert
        assert result is None
        self.mock_repository.save.assert_not_called()

    def test_deactivate_user_success(self):
        """Test successful user deactivation."""
        # Arrange
        user_id = "test_user_id"
        existing_user = User(user_id=user_id, is_active=True)

        self.mock_repository.find_by_id.return_value = existing_user
        self.mock_repository.save.return_value = existing_user

        # Act
        result = self.user_service.deactivate_user(user_id)

        # Assert
        assert result is True
        assert existing_user.is_active is False
        self.mock_repository.save.assert_called_once_with(existing_user)

    def test_deactivate_user_not_found(self):
        """Test user deactivation when user doesn't exist."""
        # Arrange
        self.mock_repository.find_by_id.return_value = None

        # Act
        result = self.user_service.deactivate_user("nonexistent_id")

        # Assert
        assert result is False
        self.mock_repository.save.assert_not_called()

    def test_get_user_by_id(self):
        """Test getting user by ID."""
        # Arrange
        user_id = "test_user_id"
        expected_user = User(user_id=user_id)
        self.mock_repository.find_by_id.return_value = expected_user

        # Act
        result = self.user_service.get_user_by_id(user_id)

        # Assert
        assert result == expected_user
        self.mock_repository.find_by_id.assert_called_once_with(user_id)

    def test_get_user_by_email(self):
        """Test getting user by email."""
        # Arrange
        email = "test@example.com"
        expected_user = User(email_address=email)
        self.mock_repository.find_by_email.return_value = expected_user

        # Act
        result = self.user_service.get_user_by_email(email)

        # Assert
        assert result == expected_user
        self.mock_repository.find_by_email.assert_called_once_with(email)
