-- Drop table if it exists (optional for dev/testing)
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert some sample data
INSERT INTO users (username, email, hashed_password, is_active) VALUES
('alice', 'alice@example.com', 'hashed_pw_123', TRUE),
('Ratesh k', 'rk@example.com', 'hashed_pw_456', TRUE);
