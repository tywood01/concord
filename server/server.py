"""
web_server.py
CS 341 Computer Networks
Lab 4

"""

# Available Ports: Tytus: 10261 through 10280
from socket import socket, AF_INET, SOCK_STREAM
import socket

import threading


users = {1: "Tytus", 2: "John", 3: "Jane"}


def send_message(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect the socket to the server's address and port
        client_socket.connect(("localhost", 10261))

        # Send data to the server
        message = "Hello, server1!"
        print(f"Sending: {message}")
        client_socket.send(message.encode())

    finally:
        # Clean up the connection
        client_socket.close()


def recieve_messages():
    pass


def main():
    send_message("hello")


if __name__ == "__main__":
    main()
