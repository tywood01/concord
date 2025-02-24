"""
web_server.py
CS 341 Computer Networks
Lab 4

"""

# Available Ports: Tytus: 10261 through 10280
from socket import socket, AF_INET, SOCK_STREAM
import threading

# about what kind of connection you are making.
# What are AF_INET and SOCK_STREAM?
# AF_INET is an address family that can designate the type of
# adresses your socket can communnicate with.
# AF_INET: address format is host and port number
# SOCK_STREAM is a connection-oriented TCP protocol stream.
SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_PORT = 10261

# Bind the socket to server address and server port
SERVER_SOCKET.bind(("localhost", SERVER_PORT))

# Listen to at most 1 connection at a time
SERVER_SOCKET.listen(1)


def send_message():
    """listens for input and sends messages to server"""

    while True:
        message = str(input())
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(("localhost", 10261))
        clientsocket.send(message.encode)


def recieve_messages():
    while True:
        print("Ready to serve...")
        # Set up a new connection from the client
        connection_socket, addr = SERVER_SOCKET.accept()
        print("Got connection from", addr)

        # Receive and decode the request message from the client
        data = connection_socket.recv(1024)
        str_data = data.decode()
        print("from client: ", str_data)
        connection_socket.close()

    # Close the server socket
    SERVER_SOCKET.close()


def main():
    # Create a new thread to listen for messages
    thread = threading.Thread(target=recieve_messages)
    thread.start()

    # Listen for input and send messages
    thread2 = threading.Thread(target=send_message())
    thread2.start()


if __name__ == "__main__":
    main()
