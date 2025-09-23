"""
Repository implementations for Tide application.
Implements domain model repositories using SQLAlchemy.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from src.database.models import (
    User,
    NotificationPreferences,
    Question,
    UserResponse,
    AuthenticationProvider,
)
from src.database.connection import get_database


class UserRepository:
    """
    User persistence and response management repository.

    Implements domain model UserRepository interface.
    """

    def __init__(self, session: Session = None):
        """
        Initialize repository with database session.

        Args:
            session: Optional SQLAlchemy session (for dependency injection)
        """
        self.session = session

    def _get_session(self) -> Session:
        """Get database session (create if not provided)."""
        if self.session:
            return self.session
        return get_database().get_session_direct()

    def save(self, user: User) -> User:
        """
        Save user entity to database.

        Args:
            user: User entity to save

        Returns:
            Saved user entity

        Raises:
            IntegrityError: If email or external_user_id constraints violated
        """
        session = self._get_session()
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            if not self.session:  # Only close if we created the session
                session.close()

    def find_by_email(self, email: str) -> Optional[User]:
        """
        Find user by email address.

        Args:
            email: Email address to search for

        Returns:
            User entity if found, None otherwise
        """
        session = self._get_session()
        try:
            return session.query(User).filter(User.email_address == email).first()
        finally:
            if not self.session:
                session.close()

    def find_by_id(self, user_id: str) -> Optional[User]:
        """
        Find user by user ID.

        Args:
            user_id: User ID to search for

        Returns:
            User entity if found, None otherwise
        """
        session = self._get_session()
        try:
            return session.query(User).filter(User.user_id == user_id).first()
        finally:
            if not self.session:
                session.close()

    def find_by_external_user_id(
        self, external_user_id: str, provider: AuthenticationProvider
    ) -> Optional[User]:
        """
        Find user by external OAuth provider user ID.

        Args:
            external_user_id: External user ID from OAuth provider
            provider: Authentication provider (Google, Microsoft)

        Returns:
            User entity if found, None otherwise
        """
        session = self._get_session()
        try:
            return (
                session.query(User)
                .filter(
                    and_(
                        User.external_user_id == external_user_id,
                        User.authentication_provider == provider,
                    )
                )
                .first()
            )
        finally:
            if not self.session:
                session.close()

    def create_from_oauth_profile(
        self, oauth_data: Dict[str, Any], provider: AuthenticationProvider
    ) -> User:
        """
        Create new user profile from OAuth provider data.

        Args:
            oauth_data: OAuth user data containing email, name, etc.
            provider: Authentication provider

        Returns:
            Created user entity with default notification preferences

        Raises:
            IntegrityError: If user already exists
        """
        session = self._get_session()
        try:
            # Generate unique user ID
            user_id = str(uuid.uuid4())

            # Create user entity
            user = User(
                user_id=user_id,
                email_address=oauth_data.get("email"),
                external_user_id=oauth_data.get("id", oauth_data.get("sub")),
                authentication_provider=provider,
                display_name=oauth_data.get(
                    "name", oauth_data.get("email", "").split("@")[0]
                ),
                profile_image_url=oauth_data.get("picture"),
                preferred_timezone="UTC",  # Default timezone
                registration_date=datetime.now(timezone.utc),
                last_active_date=datetime.now(timezone.utc),
                is_active=True,
            )

            # Create default notification preferences
            notification_prefs = NotificationPreferences(
                user_id=user_id,
                email_notifications=True,
                push_notifications=True,
                preferred_language="en",
                quiet_hours_start=None,  # No quiet hours by default
                quiet_hours_end=None,
            )

            # Add both entities to session
            session.add(user)
            session.add(notification_prefs)
            session.commit()

            # Refresh to get relationships loaded
            session.refresh(user)
            return user

        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            if not self.session:
                session.close()

    def update_last_active(self, user_id: str) -> None:
        """
        Update user's last active timestamp.

        Args:
            user_id: User ID to update
        """
        session = self._get_session()
        try:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.last_active_date = datetime.now(timezone.utc)
                session.commit()
        finally:
            if not self.session:
                session.close()

    def delete(self, user_id: str) -> bool:
        """
        Delete user and all related data.

        Args:
            user_id: User ID to delete

        Returns:
            True if user was deleted, False if not found
        """
        session = self._get_session()
        try:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                session.delete(user)  # Cascade will handle related data
                session.commit()
                return True
            return False
        finally:
            if not self.session:
                session.close()

    def record_response(
        self, user_id: str, question_id: str, response_value: str
    ) -> UserResponse:
        """
        Record user response to a question.

        Args:
            user_id: User ID
            question_id: Question ID
            response_value: User's response

        Returns:
            Created UserResponse entity

        Raises:
            IntegrityError: If duplicate response for same user/question
        """
        session = self._get_session()
        try:
            response = UserResponse(
                response_id=str(uuid.uuid4()),
                user_id=user_id,
                question_id=question_id,
                response_value=response_value,
                submitted_at=datetime.now(timezone.utc),
            )

            session.add(response)
            session.commit()
            session.refresh(response)
            return response

        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            if not self.session:
                session.close()

    def find_unanswered_questions(self, user_id: str) -> List[Question]:
        """
        Find questions that user hasn't answered yet.

        Args:
            user_id: User ID

        Returns:
            List of unanswered Question entities
        """
        session = self._get_session()
        try:
            # Subquery for questions the user has already answered
            answered_question_ids = (
                session.query(UserResponse.question_id)
                .filter(UserResponse.user_id == user_id)
                .subquery()
            )

            # Find active questions not in the answered list
            unanswered_questions = (
                session.query(Question)
                .filter(
                    and_(
                        Question.is_active,
                        ~Question.question_id.in_(answered_question_ids),
                    )
                )
                .order_by(Question.display_order)
                .all()
            )

            return unanswered_questions

        finally:
            if not self.session:
                session.close()

    def get_user_responses(self, user_id: str) -> List[UserResponse]:
        """
        Get all responses for a user.

        Args:
            user_id: User ID

        Returns:
            List of UserResponse entities
        """
        session = self._get_session()
        try:
            return (
                session.query(UserResponse)
                .filter(UserResponse.user_id == user_id)
                .order_by(UserResponse.submitted_at.desc())
                .all()
            )
        finally:
            if not self.session:
                session.close()


class QuestionRepository:
    """
    Question persistence repository.

    Implements domain model QuestionRepository interface.
    """

    def __init__(self, session: Session = None):
        """
        Initialize repository with database session.

        Args:
            session: Optional SQLAlchemy session
        """
        self.session = session

    def _get_session(self) -> Session:
        """Get database session (create if not provided)."""
        if self.session:
            return self.session
        return get_database().get_session_direct()

    def save(self, question: Question) -> Question:
        """
        Save question entity to database.

        Args:
            question: Question entity to save

        Returns:
            Saved question entity
        """
        session = self._get_session()
        try:
            session.add(question)
            session.commit()
            session.refresh(question)
            return question
        finally:
            if not self.session:
                session.close()

    def find_active_questions(self) -> List[Question]:
        """
        Find all active questions ordered by display order.

        Returns:
            List of active Question entities
        """
        session = self._get_session()
        try:
            return (
                session.query(Question)
                .filter(Question.is_active)
                .order_by(Question.display_order)
                .all()
            )
        finally:
            if not self.session:
                session.close()

    def find_by_id(self, question_id: str) -> Optional[Question]:
        """
        Find question by ID.

        Args:
            question_id: Question ID to search for

        Returns:
            Question entity if found, None otherwise
        """
        session = self._get_session()
        try:
            return (
                session.query(Question)
                .filter(Question.question_id == question_id)
                .first()
            )
        finally:
            if not self.session:
                session.close()

    def update_display_order(self, question_id: str, new_order: int) -> bool:
        """
        Update question display order.

        Args:
            question_id: Question ID to update
            new_order: New display order

        Returns:
            True if updated successfully, False if question not found
        """
        session = self._get_session()
        try:
            question = (
                session.query(Question)
                .filter(Question.question_id == question_id)
                .first()
            )
            if question:
                question.display_order = new_order
                session.commit()
                return True
            return False
        finally:
            if not self.session:
                session.close()
