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
        """Initializes the database connection."""
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

    def __del__(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

    def insert_user(self, username, last_login, online):
        """Inserts a user into the users table."""
        self.cursor.execute(
            """
            INSERT INTO users (username, last_login, online) VALUES
                (?, ?, ?)
            """,
            (username, last_login, online),
        )
        self.conn.commit()

    def get_user(self, username):
        """
        Gets the user from the users table.
        user found return user_id
        no user found return None
        """

        self.cursor.execute(
            """
            SELECT userid FROM users WHERE username = ?
            """,
            (username,),
        )
        user_id = self.cursor.fetchone()

        if user_id is None:
            return None

        return user_id[0]

    def insert_message(self, message_body, message_date, sender, receiver):
        """Inserts a message into the messages table."""
        self.cursor.execute(
            """
            INSERT INTO messages (message_body, message_date, sender, receiver)
            VALUES (?, ?, ?, ?)
            """,
            (message_body, message_date, sender, receiver),
        )
        self.conn.commit()
