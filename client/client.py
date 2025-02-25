"""
Client.py
CS 341 Computer Networks
Lab 4
Description:
This program listens and sends messages to the server
via socket programming in Python.
"""

# Available Ports: Tytus: 10261 through 10280
import socket
import threading


HOST = "localhost"
PORT = 10263


def send_message():
    """listens for input and sends messages to server"""

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))

    while True:
        message = input()
        print(message)
        clientsocket.sendall(message.encode())
        print("sent info")

    clientsocket.close()


def recieve_message():
    """listens for messages from server"""

    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        message = client_socket.recv(1024)
        print("from server: ", message.decode())
        client_socket.close()


def main():
    # Initialize send and recieving threads.
    recieve_thread = threading.Thread(target=recieve_message())
    send_thread = threading.Thread(target=send_message())

    print("Starting Threads")
    recieve_thread.start()
    send_thread.start()


if __name__ == "__main__":
    main()
