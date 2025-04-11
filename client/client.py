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
import sys
from datetime import datetime
import pathlib

# Add the root directory to the system path
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from settings import HOST, PORT


class RealTimeClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))
        self.username = None

    def main(self):
        self.login()
        print("Login successful!")

        receive_thread = threading.Thread(target=self.receive_thread)
        send_thread = threading.Thread(target=self.send_thread)

        receive_thread.start()
        send_thread.start()

    def login(self):
        while not self.username:
            self.username = input("Enter your username: ")
            self.client_socket.sendall(self.username.encode())

            ack = self.client_socket.recv(1024).decode()
            if ack != "ACK":
                print(ack)
                self.username = None

    def send_thread(self):
        try:
            while True:
                recipient = input("Enter recipient: \n")
                message = input("Enter message: \n")
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                data = {
                    "message": message,
                    "timestamp": timestamp,
                    "recipient": recipient,
                }

                self.client_socket.sendall(json.dumps(data).encode())
        except KeyboardInterrupt:
            print("Closing client...")
            self.client_socket.close()

    def receive_thread(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode()

                if data:
                    try:
                        response = json.loads(data)
                    except json.JSONDecodeError:
                        print("Received invalid JSON data:", data)
                        continue

                    if "sender" in response:
                        sender = response.get("sender")
                        message = response.get("message")
                        date = response.get("timestamp")
                        print(f"[{date}] {sender}: {message}")

                    elif "history" in response:
                        print("Chat History:")
                        records = response.get("history")
                        for record in records:
                            sender = record["sender"]
                            message = record["message"]
                            date = record["timestamp"]
                            print(f"[{date}] {sender} : {message}")

                    else:
                        print("From server:", data)

        except KeyboardInterrupt:
            print("Closing client...")
            self.client_socket.close()


def main():
    client = RealTimeClient()
    client.main()


if __name__ == "__main__":
    main()
