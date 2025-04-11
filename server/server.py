"""
web_server.py
Authors: Tytus Woodburn

Description:
    This program creates a web server that listens for incoming
    TCP socket connections and messages passed between clients.
"""

import socket
import threading
import json
import os
import sys
import db_api

# Add the root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import HOST, PORT



class RealTimeServer:
    def __init__(self):
        self.DB = db_api.DatabaseApi()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)
        self.online_users = {}
        self.online_users_lock = threading.Lock()

    def add_online(self, user, client_conn):
        """Locking to prevent race conditions"""
        with self.online_users_lock:
            self.online_users[user] = client_conn

    def remove_online(self, user):
        """Locking to prevent race conditions"""
        with self.online_users_lock:
            if user in self.online_users:
                del self.online_users[user]

    def main(self):
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            client_conn, client_addr = self.server_socket.accept()
            thread = threading.Thread(
                target=self.handler, args=(client_conn, client_addr)
            )
            thread.start()

    def login(self, client_conn, db_conn, cursor):
        """Identify or create user"""

        user = None
        while not user:
            user = client_conn.recv(1024).decode()

            if self.DB.get_user(user, db_conn, cursor) is None:
                client_conn.sendall(
                    b"User does not exist would you like to create it? (y/n)"
                )
                response = client_conn.recv(1024).decode()
                if response == "y":
                    self.DB.insert_user(user, db_conn, cursor)
                else:
                    user = None

        client_conn.sendall(b"ACK")

        return user

    def send_history(self, user, client_conn, db_conn, cursor):
        """Send chat history to the client."""
        history = self.DB.get_history(user, db_conn, cursor)

        message_content = {"history": []}
        for message in history:
            message_content["history"].append(
                {"timestamp": message[3], "message": message[2], "sender": message[0]}
            )

        client_conn.sendall(json.dumps(message_content).encode("utf-8"))

    def handler(self, client_conn, addr):
        """Handles incoming connections and messages from clients."""
        db_conn, cursor = self.DB.get_connection()

        try:
            print("Got connection from", addr)
            with client_conn:
                # User is online, insert a user session record
                user = self.login(client_conn, db_conn, cursor)
                self.add_online(user, client_conn)
                self.DB.insert_session(user, addr[0], addr[1], db_conn, cursor)

                # Add user to online users with a lock
                with self.online_users_lock:
                    self.online_users[user] = client_conn
                print(f"User {user} connected from {addr}")

                # Send chat history to the client
                self.send_history(user, client_conn, db_conn, cursor)

                # Message Handler
                while True:
                    data = client_conn.recv(1024)

                    try:
                        # Deserialize JSON string into components
                        data = json.loads(data.decode())
                        message = data.get("message")
                        timestamp = data.get("timestamp")
                        recipient = data.get("recipient")

                        print(f"Recipient: {recipient}")
                        recipient_id = self.DB.get_user(recipient, db_conn, cursor)
                        print(f"Recipient ID: {recipient_id}")

                        if recipient_id:
                            # Check if recipient is online
                            with self.online_users_lock:
                                recipient_conn = self.online_users.get(recipient)
                            if recipient_conn:
                                forward_message = {
                                    "sender": user,
                                    "message": message,
                                    "timestamp": timestamp,
                                }
                                recipient_conn.sendall(
                                    json.dumps(forward_message).encode("utf-8")
                                )
                                print(f"Message forwarded to {recipient}")

                            self.DB.insert_message(
                                message,
                                timestamp,
                                user,
                                recipient,
                                bool(recipient_id),
                                db_conn,
                                cursor,
                            )
                            print("Message stored")

                            client_conn.sendall(b"Message sent")
                        else:
                            print("Invalid recipient")
                            client_conn.sendall(b"Invalid recipient")

                    except json.JSONDecodeError:
                        # Since TCP is stream oriented it might trip this a lot...
                        print("Received invalid JSON data or data too long")
                        # client_conn.sendall(b"Invalid JSON data")

        except (BrokenPipeError, ConnectionResetError):
            print(f"User {user} disconnected")
        finally:
            # Clean up on disconnection
            with self.online_users_lock:
                if user in self.online_users:
                    del self.online_users[user]
            self.DB.delete_session(user, db_conn, cursor)
            self.remove_online(user)


if __name__ == "__main__":
    server = RealTimeServer()
    server.main()
