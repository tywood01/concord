"""
web_server.py
CS 341 Computer Networks
Lab 4

"""

# Available Ports: Tytus: 10261 through 10280
import socket
import threading

HOST = "localhost"
PORT = 10263


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


def recieve_messages(server_socket):
    conn, addr = server_socket.accept()
    print("Got connection from", addr)

    with conn:
        print("inside connection")
        while True:
            print("inside while")
            # Receive and decode the request message from the client
            data = conn.recv(1024)
            print("recieved data")
            if not data:
                print("Client disconnected")

                break
            print("from client: ", data.decode())

    conn.close()


def main():
    print("in main")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    # Pass target function and its arguments as a tuple
    recieve_thread = threading.Thread(target=recieve_messages, args=(server_socket,))

    print("Starting Thread")
    recieve_thread.start()


if __name__ == "__main__":
    main()
