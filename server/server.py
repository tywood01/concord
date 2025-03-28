"""
web_server.py
Authors: Tytus Woodburn

Description:
    This program creates a web server that listens for incoming
    TCP socket connections and messages passed between clients.
"""

import socket
import threading
import sqlite3
import json
import os
import sys

# Add the root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import HOST, PORT, DATABASE


def store_user():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Updates tables with user ids, username, last login date, and current online status
    cursor.execute(
        """
        INSERT INTO users (username, last_login, online) VALUES
            ('client5', '2025-03-26 10:05:00', 1),
            ('client6', '2025-03-26 10:05:00', 1)
        """
    )
    conn.commit()

    # Commit the changes and close the connection
    # Show all the messages in the messages table
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row, flush=True)

    print("Table 'users' has been created successfully in 'database.py'.")


def store_message(data):
    print("inside stor message")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Deserialize JSON string into components
        username = data.get("username")
        message_body = data.get("message_body")
        receiver = data.get("receiver")
        timestamp = data.get("timestamp")

        print(f"Storing message: {data}", flush=True)

        # Insert message into messages table
        cursor.execute(
            """
            INSERT INTO messages (message_body, message_date, sender, receiver)
            VALUES (?, ?, ?, ?)
            """,
            (message_body, timestamp, username, receiver),
        )

        conn.commit()
        print("User tables updated")

        cursor.execute("SELECT * FROM messages;")
        rows = cursor.fetchall()
        for row in rows:
            print(row, flush=True)

    except Exception as e:
        print(f"Error in store_message: {e}", flush=True)

    finally:
        print("closing connection")
        conn.close()


def handler(client_conn, addr):
    """Handles incoming connections and messages from clients"""

    print("Got connection from", addr)
    with client_conn:
        user = client_conn.recv(1024).decode()
        print(f"User {user} connected from {addr}")

        while True:
            data = client_conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected")
                break

            try:
                message = json.loads(data.decode())
                # Deserialize JSON string into components
                sender = message.get("username")
                message_body = message.get("message_body")
                receiver = message.get("receiver")
                timestamp = message.get("timestamp")

                store_message(message)
                # send_message(message)

                print(
                    f"User {sender} from {addr} says: {message_body} to {receiver} at time {timestamp}"
                )

                # Send acknowledgment back to the client
                client_conn.sendall(b"Message received")

            except json.JSONDecodeError:
                print("Received invalid JSON data")
                client_conn.sendall(b"Received invalid JSON data")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")
    store_user()

    while True:
        client_conn, addr = server_socket.accept()
        client_conn.send(b"Welcome to Concord!")
        thread = threading.Thread(target=handler, args=(client_conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
