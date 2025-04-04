"""
db_api.py
Authors: Tytus Woodburn

Description:
    This defines a class that is easier to use
    for our db queries and inserts.
"""

import sqlite3
import os
import sys

# Add the root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import DATABASE


class DatabaseApi(object):
    """This class is used to interact with the database."""

    def __init__(self):
        self.db_path = DATABASE

    def get_connection(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return (self.conn, self.cursor)

    def insert_user(self, username, conn, cursor):
        """Inserts a user into the users table."""
        cursor.execute(
            """
            INSERT INTO users (username) VALUES
                (?)
            """,
            (username,),
        )
        conn.commit()

    def get_user(self, username, conn, cursor):
        """
        Gets the user from the users table.
        user found return user_id
        no user found return None
        """

        cursor.execute(
            """
            SELECT userid FROM users WHERE username = ?
            """,
            (username,),
        )
        user_id = cursor.fetchone()

        if user_id is None:
            return None

        return user_id[0]

    def insert_message(
        self, message_body, message_date, sender, receiver, receiver_read, conn, cursor
    ):
        """Inserts a message into the messages table."""
        cursor.execute(
            """
            INSERT INTO messages (message_body, message_date, sender, receiver, receiver_read)
            VALUES (?, ?, ?, ?, ?)
            """,
            (message_body, message_date, sender, receiver, receiver_read),
        )
        conn.commit()

    def read_messages(self, receiver, conn, cursor):
        """Inserts a message into the messages table."""
        cursor.execute(
            """
            UPDATE messages
            SET receiver_read = 1
            WHERE receiver = ?
            """,
            (receiver,),
        )
        conn.commit()

    def insert_session(self, user, conn, cursor):
        """Inserts a session into the session table.
        If session record exists, user is online.
        If session record does not exist, user is offline.
        """
        cursor.execute(
            """
            INSERT INTO sessions (user)
            VALUES (?)
            """,
            (user,),
        )
        conn.commit()

    def delete_session(self, user, conn, cursor):
        """Deletes a session from the session table.
        The user is logging out.
        """
        cursor.execute(
            """
            DELETE FROM sessions WHERE user = ?;
            """,
            (user,),
        )
        conn.commit()

    def get_user_online_status(self, user, conn, cursor):
        """
        Gets the session from the sessions table.
        If there is no session record, then returns False. (user is not online)
        If there is a session record, then returns True. (user is online)
        """

        cursor.execute(
            """
            SELECT user FROM sessions WHERE user = ?
            """,
            (user,),
        )
        user_id = cursor.fetchone()

        if user_id is None:
            return False
        else:
            return True

    def get_history(self, user, recipient, conn, cursor):
        """Get all messages between a sender and reciever from the messages table"""

        cursor.execute(
            """
            SELECT sender, receiver, message_body, message_date 
            FROM messages 
            WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
            ORDER BY message_date
            """,
            (user, recipient, recipient, user),
        )

        history = []
        messages = cursor.fetchall()
        for message in messages:
            history.append(message)

        return history
