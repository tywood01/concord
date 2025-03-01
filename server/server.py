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


def handler(conn, addr):
    print("Got connection from", addr)
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected")
                break
            print(f"from {addr}:", data.decode())
            conn.sendall(b"hello from server")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        conn.send(b"Hello from server")
        thread = threading.Thread(target=handler, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
