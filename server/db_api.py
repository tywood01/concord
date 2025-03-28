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

    def insert_user(username, last_login, online, conn, cursor):
        """Inserts a user into the users table."""
        cursor.execute(
            """
            INSERT INTO users (username, last_login, online) VALUES
                (?, ?, ?)
            """,
            (username, last_login, online),
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

    def insert_message(message_body, message_date, sender, receiver, conn, cursor):
        """Inserts a message into the messages table."""
        cursor.execute(
            """
            INSERT INTO messages (message_body, message_date, sender, receiver)
            VALUES (?, ?, ?, ?)
            """,
            (message_body, message_date, sender, receiver),
        )
        conn.commit()
