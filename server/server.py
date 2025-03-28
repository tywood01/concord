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
import datetime

# Add the root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import HOST, PORT


class RealTimeServer:
    def __init__(self):
        self.DB = db_api.DatabaseApi()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)

    def main(self):
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            client_conn, client_addr = self.server_socket.accept()
            thread = threading.Thread(
                target=self.handler, args=(client_conn, client_addr)
            )
            thread.start()

    def handler(self, client_conn, addr):
        """Handles incoming connections and messages from clients"""

        # Create independant DB connection for each client
        db_conn, cursor = self.DB.get_connection()

        try:
            print("Got connection from", addr)
            with client_conn:
                # Client "Login" process
                user = None
                while not user:
                    user = client_conn.recv(1024).decode()

                    if self.DB.get_user(user, db_conn, cursor) is None:
                        client_conn.sendall(b"User does not exist")
                        user = None

                client_conn.sendall(b"ACK")
                print(f"User {user} connected from {addr}")

                # Retrieve messages for user

                # Message handling loop
                while True:
                    data = client_conn.recv(1024)
                    if not data:
                        print(f"Client {addr} disconnected")
                        break

                    try:
                        message = json.loads(data.decode())
                        # Deserialize JSON string into components
                        message_body = message.get("message_body")
                        receiver = message.get("receiver")
                        timestamp = message.get("timestamp")

                        # store_message(message)
                        # send_message(message)

                        print(
                            f"User {user} from {addr} says: {message_body} to {receiver} at time {timestamp}"
                        )

                        # Send acknowledgment back to the client
                        client_conn.sendall(b"Message received")

                    except json.JSONDecodeError:
                        print("Received invalid JSON data")
                        client_conn.sendall(b"Received invalid JSON data")

        except KeyboardInterrupt:
            print("Closing server")
            client_conn.close()
            db_conn.close()


def main():
    server = RealTimeServer()
    server.main()


if __name__ == "__main__":
    main()
