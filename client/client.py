"""
client.py
Authors: Tytus Woodburn

Description:
    This program listens and sends messages to the server
    via socket programming in Python.
"""

import socket
import threading
import json
import os
import sys
import datetime

# Add the root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import HOST, PORT


class RealTimeClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))
        self.username = None

    def main(self):
        self.login()

        print("Login Success!!!")

        # Initialize sending and recieving threads.
        recieve_thread = threading.Thread(target=self.recieve_thread)
        send_thread = threading.Thread(target=self.send_thread)

        print("Starting Threads")
        recieve_thread.start()
        send_thread.start()

    def login(self):
        """Logs in the user to the server"""

        while not self.username:
            self.username = input("Enter your username: ")
            self.client_socket.sendall(self.username.encode())

            ack = self.client_socket.recv(1024)
            if ack.decode() != "ACK":
                print(ack.decode())
                self.username = None

        print(f"Logged in as {self.username}")

    def send_thread(self):
        """listens for input and sends messages to server"""

        try:
            while True:
                ack = ""

                while ack != "ACK":
                    print(ack)
                    reciever = input("Enter reciever: ")
                    self.client_socket.sendall(reciever.encode())
                    ack = self.client_socket.recv(1024).decode()

                history = self.client_socket.recv(1024).decode()

                print(history)

                message = input("Enter message: ")
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                data = {
                    "username": self.username,
                    "message": message,
                    "timestamp": timestamp,
                }

                json_data = json.dumps(data)

                print(f"Sending: {data}")
                self.client_socket.sendall(json_data.encode())
                ack = self.client_socket.recv(1024)
                print(ack.decode())

        except KeyboardInterrupt:
            print("Closing client")
            self.client_socket.close()

    def recieve_thread(self):
        """listens for messages from server"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        try:
            while True:
                message = client_socket.recv(1024)
                print("from server: ", message.decode())

        except KeyboardInterrupt:
            print("Closing client")
            client_socket.close()

    def display_messages(self, db_conn, cursor):
        """Retrieve and display all messages from the database."""

    try:
        # Assuming there is a 'messages' table in the database
        cursor.execute("SELECT sender, receiver, message_body, timestamp FROM messages")
        messages = cursor.fetchall()

        print("Messages exchanged between clients:")
        print("-----------------------------------")
        for message in messages:
            sender, receiver, message_body, timestamp = message
            print(
                f"From: {sender} | To: {receiver} | Message: {message_body} | Timestamp: {timestamp}"
            )
    except Exception as e:
        print(f"Error retrieving messages: {e}")


def main():
    client = RealTimeClient()
    client.main()


if __name__ == "__main__":
    main()
