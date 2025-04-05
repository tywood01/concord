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
                        client_conn.sendall(
                            b"User does not exist would you like to create it? (y/n)"
                        )
                        response = client_conn.recv(1024).decode()
                        if response == "y":
                            self.DB.insert_user(user, db_conn, cursor)
                        else:
                            user = None

                client_conn.sendall(b"ACK")
                print(f"User {user} connected from {addr}")

                # User is online, insert a user session record
                self.DB.insert_session(user, db_conn, cursor)

                # TODO (We probably don't have to do this, this is harder) Retrieve all recived read messages for user & all sent messages (both sorted by date intertwined)

                # TODO (We should do this) Retrieve all unread messages for user (sorted by date)

                # Marks all unread messages as read for receiver
                # self.DB.read_messages(user, db_conn, cursor)

                # Message handling loop
                while True:
                    recipient = None
                    while recipient is None:
                        recipient = client_conn.recv(1024).decode()

                        recipient = self.DB.get_user(recipient, db_conn, cursor)

                        if recipient is None:
                            client_conn.sendall(
                                b"User does not exist, please specify a different user"
                            )
                            print(f"User {recipient} does not exist")

                    ack = "ACK"
                    client_conn.sendall(ack.encode())

                    history = self.DB.get_history(user, recipient, db_conn, cursor)

                    print(history)
                    client_conn.sendall(json.dumps(history).encode())

                    data = client_conn.recv(1024)

                    if not data:
                        # Client disconnected & remove user session record
                        self.DB.delete_session(user, db_conn, cursor)
                        print(f"Client {addr} disconnected")
                        break

                    try:
                        data = json.loads(data.decode())
                        # Deserialize JSON string into components
                        receiver = data.get("receiver")

                        message = data.get("message")
                        timestamp = data.get("timestamp")

                        # TODO Send message to reciever
                        # send_message(message)

                        # Stores messages to the database
                        if self.DB.get_user(receiver, db_conn, cursor):
                            receiver_online_status = self.DB.get_user_online_status(
                                receiver, db_conn, cursor
                            )
                            # If user is online mark as read, otherwise if user is offline mark as unread
                            if receiver_online_status == True:
                                self.DB.insert_message(
                                    message,
                                    timestamp,
                                    user,
                                    receiver,
                                    receiver_online_status,
                                    db_conn,
                                    cursor,
                                )
                            else:
                                self.DB.insert_message(
                                    message,
                                    timestamp,
                                    user,
                                    receiver,
                                    receiver_online_status,
                                    db_conn,
                                    cursor,
                                )

                        # receiver user does not exist, message is not stored to database
                        else:
                            print(f"User {receiver} does not exist")

                        print(
                            f"User {user} from {addr} says: {message} to {receiver} at time {timestamp}"
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
