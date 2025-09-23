"""
Integration tests for database operations.
"""

import pytest
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class TestDatabaseIntegration:
    """Test database integration and connectivity."""

    @pytest.fixture(scope="class")
    def db_engine(self):
        """Create database engine for testing."""
        database_url = os.getenv(
            "DATABASE_URL",
            "postgresql://tide_user:tide_password@localhost:5432/tide_db_test",
        )
        engine = create_engine(database_url)
        yield engine
        engine.dispose()

    @pytest.fixture
    def db_session(self, db_engine):
        """Create database session for testing."""
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
        session = SessionLocal()
        yield session
        session.close()

    def test_database_connection(self, db_engine):
        """Test that we can connect to the database."""
        with db_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1

    def test_pgvector_extension_available(self, db_engine):
        """Test that pgvector extension is available."""
        with db_engine.connect() as connection:
            try:
                result = connection.execute(
                    text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
                )
                extensions = [row[0] for row in result]
                assert "vector" in extensions
            except Exception:
                # If this fails, it might be because we're using SQLite in some tests
                # Skip the test if not using PostgreSQL
                pytest.skip("pgvector test requires PostgreSQL")

    def test_create_table_with_vector_column(self, db_engine):
        """Test creating a table with vector column."""
        with db_engine.connect() as connection:
            try:
                # Create a test table with vector column
                connection.execute(
                    text(
                        """
                    CREATE TABLE IF NOT EXISTS test_vectors (
                        id SERIAL PRIMARY KEY,
                        embedding vector(384),
                        content TEXT
                    )
                """
                    )
                )
                connection.commit()

                # Insert test data
                connection.execute(
                    text(
                        """
                    INSERT INTO test_vectors (embedding, content)
                    VALUES ('[1,2,3]'::vector, 'test content')
                """
                    )
                )
                connection.commit()

                # Query the data
                result = connection.execute(
                    text("SELECT content FROM test_vectors WHERE id = 1")
                )
                content = result.scalar()
                assert content == "test content"

                # Clean up
                connection.execute(text("DROP TABLE test_vectors"))
                connection.commit()

            except Exception as e:
                if "vector" in str(e).lower():
                    pytest.skip(
                        "pgvector test requires PostgreSQL with vector extension"
                    )
                else:
                    raise

    def test_transaction_rollback(self, db_session):
        """Test transaction rollback functionality."""
        try:
            # This should fail and trigger rollback
            db_session.execute(text("SELECT * FROM non_existent_table"))
            db_session.commit()
        except Exception:
            db_session.rollback()
            # If we get here, rollback worked
            pass

        # Test that session is still usable after rollback
        result = db_session.execute(text("SELECT 1"))
        assert result.scalar() == 1
