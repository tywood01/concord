import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("concord.db")
cursor = conn.cursor()

# Sample insert that adds new users to the users table
cursor.execute(
    """
    INSERT INTO users (username, last_login, online) VALUES
        ('client1', '2025-03-26 10:05:00', 1),
        ('client2', '2025-03-26 10:05:00', 1)
    """
)

# Sample query that gets the user_id from the name user
user = "client1"
cursor.execute(
    """
    SELECT userid FROM users WHERE username = ?
    """,
    (user,),
)
sender_id = cursor.fetchone()

# Check that a sender exists in the database
if sender_id is None:
    raise ValueError(f"Sender '{user}' does not exist in the database.")
sender_id = sender_id[0]


# Sample query that gets the user_id from the recipient user
recipient = "client2"
cursor.execute(
    """
    SELECT userid FROM users WHERE username = ?
    """,
    (recipient,),
)

# Check that a reciever exists in the database
recipient_id = cursor.fetchone()
if recipient_id is None:
    raise ValueError(f"Recipient '{recipient}' does not exist in the database.")
recipient_id = recipient_id[0]

# Inserts a new message using the sender_id and recipient_id
cursor.execute(
    """
    INSERT INTO messages (message_body, message_date, sender, receiver) VALUES
        ('hello client1', '2025-03-26 10:05:00', ?, ?)
    """,
    (sender_id, recipient_id),
)

# Write to the database
conn.commit()

# Show all the messages in the messages table
cursor.execute("SELECT * FROM messages;")
rows = cursor.fetchall()
for row in rows:
    print(row, flush=True)
