"""
SQLAlchemy database models for Tide application.
Implements the domain model entities using SQLAlchemy ORM.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, DateTime, Boolean, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from enum import Enum


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class AuthenticationProvider(str, Enum):
    """OAuth provider identification enum."""

    GOOGLE = "google"
    MICROSOFT = "microsoft"


class User(Base):
    """
    User aggregate root - Core user identity and personalization hub.

    Business Rules from Domain Model:
    - Each user must have exactly one unique email address
    - Each user has exactly one authentication provider
    - User profile must be created automatically after OAuth authentication
    - User deletion cascades to all owned entities
    """

    __tablename__ = "users"

    # Primary Key
    user_id: Mapped[str] = mapped_column(String(50), primary_key=True)

    # Authentication and Identity
    email_address: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    external_user_id: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    authentication_provider: Mapped[AuthenticationProvider] = mapped_column(
        nullable=False
    )

    # Profile Information
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    profile_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    preferred_timezone: Mapped[str] = mapped_column(
        String(50), nullable=False, default="UTC"
    )

    # Timestamps
    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    last_active_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships (one-to-one and one-to-many)
    notification_preferences: Mapped["NotificationPreferences"] = relationship(
        "NotificationPreferences",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    responses: Mapped[list["UserResponse"]] = relationship(
        "UserResponse", back_populates="user", cascade="all, delete-orphan"
    )

    # Unique constraint for external user ID + provider combination
    __table_args__ = (
        UniqueConstraint(
            "external_user_id",
            "authentication_provider",
            name="_user_external_provider_uc",
        ),
    )

    def __repr__(self) -> str:
        return f"<User(user_id='{self.user_id}', email='{self.email_address}', provider='{self.authentication_provider}')>"


class NotificationPreferences(Base):
    """
    User communication settings entity.

    Business Rules:
    - One per User (required)
    - Quiet hours start must be before end
    """

    __tablename__ = "notification_preferences"

    # Primary Key and Foreign Key
    user_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("users.user_id"), primary_key=True
    )

    # Notification Settings
    email_notifications: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    push_notifications: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    preferred_language: Mapped[str] = mapped_column(
        String(10), nullable=False, default="en"
    )

    # Quiet Hours (24-hour format, e.g., "22:00", "08:00")
    quiet_hours_start: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    quiet_hours_end: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)

    # Relationship
    user: Mapped["User"] = relationship(
        "User", back_populates="notification_preferences"
    )

    def __repr__(self) -> str:
        return f"<NotificationPreferences(user_id='{self.user_id}', email={self.email_notifications})>"


class Question(Base):
    """
    Question aggregate root - Individual questions for user personalization.

    Business Rules:
    - Questions can be deprecated (IsActive = false)
    - MCQ questions must have at least two options
    - Display order must be unique among active questions
    """

    __tablename__ = "questions"

    # Primary Key
    question_id: Mapped[str] = mapped_column(String(50), primary_key=True)

    # Question Content
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # MCQ, Numeric, Text
    display_order: Mapped[int] = mapped_column(nullable=False, index=True)

    # Status and Metadata
    is_mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, index=True
    )
    localization_key: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    options: Mapped[list["QuestionOption"]] = relationship(
        "QuestionOption", back_populates="question", cascade="all, delete-orphan"
    )
    responses: Mapped[list["UserResponse"]] = relationship(
        "UserResponse", back_populates="question"
    )

    def __repr__(self) -> str:
        return f"<Question(question_id='{self.question_id}', text='{self.question_text[:50]}...', active={self.is_active})>"


class QuestionOption(Base):
    """
    MCQ answer choices entity.

    Business Rules:
    - Many per Question
    - Display order for proper presentation
    """

    __tablename__ = "question_options"

    # Primary Key
    option_id: Mapped[str] = mapped_column(String(50), primary_key=True)

    # Foreign Key
    question_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("questions.question_id"), nullable=False
    )

    # Option Content
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    display_order: Mapped[int] = mapped_column(nullable=False)
    localization_key: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationship
    question: Mapped["Question"] = relationship("Question", back_populates="options")

    def __repr__(self) -> str:
        return f"<QuestionOption(option_id='{self.option_id}', text='{self.option_text[:30]}...')>"


class UserResponse(Base):
    """
    Individual question answers entity.

    Business Rules:
    - Many per User
    - Cannot be modified after submission
    - Links User and Question domains
    """

    __tablename__ = "user_responses"

    # Primary Key
    response_id: Mapped[str] = mapped_column(String(50), primary_key=True)

    # Foreign Keys
    user_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("users.user_id"), nullable=False, index=True
    )
    question_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("questions.question_id"), nullable=False, index=True
    )

    # Response Data
    response_value: Mapped[str] = mapped_column(Text, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="responses")
    question: Mapped["Question"] = relationship("Question", back_populates="responses")

    # Unique constraint to prevent duplicate responses
    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="_user_question_response_uc"),
    )

    def __repr__(self) -> str:
        return f"<UserResponse(response_id='{self.response_id}', user_id='{self.user_id}', question_id='{self.question_id}')>"
