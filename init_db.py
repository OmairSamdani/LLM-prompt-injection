import sqlite3

connection = sqlite3.connect("chatbot.db")
cursor = connection.cursor()

# -------------------------
# Users
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL
)
""")

# -------------------------
# Sessions
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# -------------------------
# Messages
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,

    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
)
""")

# -------------------------
# Test users
# -------------------------

cursor.execute("""
INSERT OR IGNORE INTO users (username)
VALUES ('Omair')
""")

cursor.execute("""
INSERT OR IGNORE INTO users (username)
VALUES ('Mohammed')
""")

connection.commit()
connection.close()

print("Database initialized successfully.")