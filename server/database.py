import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("concord.db")
cursor = conn.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    last_logged_in TEXT,
    online INTEGER DEFAULT 0
)
""")

# Create the messages table
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_body TEXT NOT NULL,
    message_date TEXT NOT NULL,
    sender INTEGER NOT NULL,
    receiver INTEGER NOT NULL,
    FOREIGN KEY (sender) REFERENCES users(userid),
    FOREIGN KEY (receiver) REFERENCES users(userid)
)
""")

# Commit changes and close the connection
conn.commit()
conn.close()
