"""
Database connection configuration for Tide application.
Provides SQLAlchemy engine and session management.
"""

from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from src.config import Config
from src.database.models import Base


class DatabaseConnection:
    """Manages database connection and session lifecycle."""

    def __init__(self, database_url: str = None):
        """
        Initialize database connection.

        Args:
            database_url: Optional database URL override for testing
        """
        self.database_url = database_url or Config.DATABASE_URL
        self.engine: Engine = self._create_engine()
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def _create_engine(self) -> Engine:
        """Create SQLAlchemy engine with appropriate configuration."""

        # For testing with in-memory SQLite
        if self.database_url.startswith("sqlite://"):
            return create_engine(
                self.database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=Config.DEBUG_MODE,
            )

        # For PostgreSQL production/development
        return create_engine(
            self.database_url,
            echo=Config.DEBUG_MODE,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=3600,  # Recycle connections after 1 hour
        )

    def create_tables(self) -> None:
        """Create all database tables."""
        Base.metadata.create_all(bind=self.engine)

    def drop_tables(self) -> None:
        """Drop all database tables (for testing)."""
        Base.metadata.drop_all(bind=self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        """
        Get database session with automatic cleanup.

        Yields:
            SQLAlchemy session instance
        """
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def get_session_direct(self) -> Session:
        """
        Get database session for manual management.

        Returns:
            SQLAlchemy session instance (must be closed manually)
        """
        return self.SessionLocal()


# Global database connection instance
_db_connection: DatabaseConnection = None


def get_database() -> DatabaseConnection:
    """
    Get global database connection instance.

    Returns:
        DatabaseConnection instance
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection


def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI to get database session.

    Yields:
        SQLAlchemy session instance
    """
    db = get_database()
    yield from db.get_session()


def initialize_database() -> None:
    """Initialize database tables."""
    db = get_database()
    db.create_tables()


def reset_database() -> None:
    """Reset database (drop and recreate tables) - for testing only."""
    db = get_database()
    db.drop_tables()
    db.create_tables()
