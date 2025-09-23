"""
User domain service for Tide application.
Implements user lifecycle management and business operations.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

from src.database.models import User, AuthenticationProvider, Question
from src.database.repositories import UserRepository


class UserService:
    """
    Complete user lifecycle management service.

    Implements domain model UserService operations.
    """

    def __init__(self, user_repository: UserRepository = None):
        """
        Initialize user service.

        Args:
            user_repository: Optional UserRepository for dependency injection
        """
        self.user_repository = user_repository or UserRepository()

    def create_user_from_oauth(
        self, oauth_data: Dict[str, Any], provider: AuthenticationProvider
    ) -> User:
        """
        Create new user from OAuth provider data.

        Args:
            oauth_data: OAuth user profile data
            provider: Authentication provider (Google, Microsoft)

        Returns:
            Created User entity

        Raises:
            ValueError: If user already exists or invalid data
        """
        # Validate required OAuth data
        email = oauth_data.get("email")
        if not email:
            raise ValueError("OAuth data must include email address")

        external_user_id = oauth_data.get("id") or oauth_data.get("sub")
        if not external_user_id:
            raise ValueError("OAuth data must include user ID")

        # Check if user already exists
        existing_user = self.user_repository.find_by_external_user_id(
            external_user_id, provider
        )
        if existing_user:
            raise ValueError(f"User already exists with external ID {external_user_id}")

        # Check if email is already registered with different provider
        existing_email_user = self.user_repository.find_by_email(email)
        if existing_email_user:
            raise ValueError(
                f"Email {email} is already registered with {existing_email_user.authentication_provider}"
            )

        try:
            # Create user with default notification preferences
            user = self.user_repository.create_from_oauth_profile(oauth_data, provider)
            return user
        except IntegrityError as e:
            raise ValueError(f"Failed to create user: {str(e)}")

    def get_or_create_user_from_oauth(
        self, oauth_data: Dict[str, Any], provider: AuthenticationProvider
    ) -> tuple[User, bool]:
        """
        Get existing user or create new one from OAuth data.

        Args:
            oauth_data: OAuth user profile data
            provider: Authentication provider

        Returns:
            Tuple of (User entity, is_new_user: bool)

        Raises:
            ValueError: If invalid OAuth data provided
        """
        # Validate required OAuth data
        email = oauth_data.get("email")
        if not email:
            raise ValueError("OAuth data must include email address")

        external_user_id = oauth_data.get("id") or oauth_data.get("sub")
        if not external_user_id:
            raise ValueError("OAuth data must include user ID")

        # Try to find existing user by external ID and provider
        existing_user = self.user_repository.find_by_external_user_id(
            external_user_id, provider
        )
        if existing_user:
            # Update last active date
            self.user_repository.update_last_active(existing_user.user_id)
            return existing_user, False

        # Try to find by email (for account linking scenarios)
        existing_email_user = self.user_repository.find_by_email(email)
        if existing_email_user:
            # Email exists with different provider - this is a business decision
            # For now, we'll treat this as an error to prevent account confusion
            raise ValueError(
                f"Email {email} is already registered with {existing_email_user.authentication_provider}"
            )

        # Create new user
        try:
            new_user = self.user_repository.create_from_oauth_profile(
                oauth_data, provider
            )
            return new_user, True
        except IntegrityError as e:
            raise ValueError(f"Failed to create user: {str(e)}")

    def update_profile(
        self, user_id: str, profile_updates: Dict[str, Any]
    ) -> Optional[User]:
        """
        Update user profile information.

        Args:
            user_id: User ID to update
            profile_updates: Dictionary of fields to update

        Returns:
            Updated User entity if found, None otherwise

        Raises:
            ValueError: If invalid update data provided
        """
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return None

        # Update allowed fields
        allowed_fields = {"display_name", "preferred_timezone", "profile_image_url"}
        updated = False

        for field, value in profile_updates.items():
            if field in allowed_fields and hasattr(user, field):
                setattr(user, field, value)
                updated = True

        if updated:
            user.last_active_date = datetime.now(timezone.utc)
            self.user_repository.save(user)

        return user

    def get_pending_questions(self, user_id: str) -> List[Question]:
        """
        Get questions that user hasn't answered yet.

        Args:
            user_id: User ID

        Returns:
            List of unanswered Question entities
        """
        return self.user_repository.find_unanswered_questions(user_id)

    def validate_responses(self, user_id: str, responses: List[Dict[str, Any]]) -> bool:
        """
        Validate user responses before submission.

        Args:
            user_id: User ID
            responses: List of response dictionaries

        Returns:
            True if all responses are valid

        Raises:
            ValueError: If any response is invalid
        """
        # Basic validation
        if not responses:
            raise ValueError("No responses provided")

        # Validate each response has required fields
        for response in responses:
            if "question_id" not in response or "response_value" not in response:
                raise ValueError(
                    "Each response must have question_id and response_value"
                )

            # Additional validation could be added here
            # - Check if question exists and is active
            # - Validate response format based on question type
            # - Check if user already answered this question

        return True

    def submit_responses(self, user_id: str, responses: List[Dict[str, Any]]) -> List:
        """
        Submit user responses to questions.

        Args:
            user_id: User ID
            responses: List of response dictionaries

        Returns:
            List of created UserResponse entities

        Raises:
            ValueError: If validation fails
        """
        # Validate responses first
        self.validate_responses(user_id, responses)

        created_responses = []
        for response_data in responses:
            response = self.user_repository.record_response(
                user_id=user_id,
                question_id=response_data["question_id"],
                response_value=response_data["response_value"],
            )
            created_responses.append(response)

        # Update user's last active date
        self.user_repository.update_last_active(user_id)

        return created_responses

    def deactivate_user(self, user_id: str) -> bool:
        """
        Deactivate user account (soft delete).

        Args:
            user_id: User ID to deactivate

        Returns:
            True if user was deactivated, False if not found
        """
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return False

        user.is_active = False
        user.last_active_date = datetime.now(timezone.utc)
        self.user_repository.save(user)
        return True

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User ID to find

        Returns:
            User entity if found, None otherwise
        """
        return self.user_repository.find_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.

        Args:
            email: Email address to find

        Returns:
            User entity if found, None otherwise
        """
        return self.user_repository.find_by_email(email)
