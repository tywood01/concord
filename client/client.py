"""
client.py
Authors: Tytus Woodburn

Description:
    This program listens and sends messages to the server
    via socket programming in Python.
"""

# Available Ports: Tytus: 10261 through 10280
import socket
import threading
import json
import os
import sys
import datetime

# Add the root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import HOST, PORT


def send_message():
    """listens for input and sends messages to server"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    try:
        username = input("Enter your username: ")

        while True:
            reciever = input("Enter reciever: ")
            message = input("Enter message: ")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(timestamp)

            data = {
                "username": username,
                "message": message,
                "receiver": reciever,
                "timestamp": timestamp,
            }

            json_data = json.dumps(data)

            print(f"Sending: {data}")
            client_socket.sendall(json_data.encode())

    except KeyboardInterrupt:
        print("Closing client")

    finally:
        client_socket.close()


def recieve_message():
    """listens for messages from server"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    try:
        while True:
            message = client_socket.recv(1024)
            print("from server: ", message.decode())

    except KeyboardInterrupt:
        print("Closing client")

    finally:
        client_socket.close()


def main():
    # Initialize send and recieving threads.
    recieve_thread = threading.Thread(target=recieve_message)
    send_thread = threading.Thread(target=send_message)

    print("Starting Threads")
    recieve_thread.start()
    send_thread.start()


if __name__ == "__main__":
    main()
