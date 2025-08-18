CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    user_id INT NOT NULL REFERENCES users(id),
    UNIQUE (title, user_id)   -- 👈 same title allowed for different users
);

-- Example inserts
INSERT INTO users (name) VALUES ('Alice'), ('Bob')
ON CONFLICT DO NOTHING;

INSERT INTO tasks (title, user_id) 
VALUES 
    ('Buy milk', 1),
    ('Clean house', 1),
    ('Buy milk', 2)  -- Allowed because user_id is different
ON CONFLICT DO NOTHING;

