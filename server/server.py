"""
web_server.py
Authors: Tytus Woodburn

Description:

"""

# Available Ports: Tytus: 10261 through 10280
import socket
import threading
import sqlite3
import json
import os
import sys

# Add the root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import HOST, PORT, DATABASE


def store_message(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Deserialize JSON string into components
        username = data.get("username")
        message_body = data.get("message_body")
        receiver = data.get("receiver")

        print(f"Storing message: {data}", flush=True)

        # Insert message into messages table
        cursor.execute(
            """
            INSERT INTO messages (message_body, message_date, sender, receiver)
            VALUES (?, ?, ?, ?)
            """,
            (message_body, "2025-03-26 10:05:00", username, receiver),
        )

        conn.commit()
        print("User tables updated", flush=True)

        cursor.execute("SELECT * FROM messages;")
        rows = cursor.fetchall()
        for row in rows:
            print(row, flush=True)

    except Exception as e:
        print(f"Error in store_message: {e}", flush=True)

    finally:
        conn.close()


def handler(conn, addr):
    """Handles incoming connections and messages from clients"""

    print("Got connection from", addr)
    with conn:
        user = conn.recv(1024).decode()
        print(f"User {user} connected from {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected")
                break

            try:
                message = json.loads(data.decode())
                # Deserialize JSON string into components
                sender = message.get("username")
                message_body = message.get("message_body")
                receiver = message.get("receiver")

                store_message(message)

                print(f"User {sender} from {addr} says: {message_body} to {receiver}")

                # Send acknowledgment back to the client
                conn.sendall(b"Message received")

            except json.JSONDecodeError:
                print("Received invalid JSON data")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        conn.send(b"Welcome to Concord!")
        thread = threading.Thread(target=handler, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
