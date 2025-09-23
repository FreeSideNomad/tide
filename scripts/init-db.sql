-- Initialize PostgreSQL with pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create user and database if they don't exist
-- Note: These are already created by the postgres image environment variables
-- This file is for any additional initialization needed

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE tide_db TO tide_user;