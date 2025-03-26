"""
web_server.py
CS 341 Computer Networks
Lab 4

"""

# Available Ports: Tytus: 10261 through 10280
import socket
import threading
import sqlite3

HOST = "localhost"
PORT = 10263
DATABASE = "concord.db"



def update_user_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Updates tables with user ids, username, last login date, and current online status
    cursor.execute("INSERT INTO users (user_id, last_logged_on) VALUES (1, '2025-03-25 10:30:00')")   
    # Commit the changes and close the connection

    cursor.execute("SELECT * FROM users")
    conn.commit()
    conn.close()

print("Table 'users' has been created successfully in 'database.py'.")




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
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    create_tables(conn, cursor)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        conn.send(b"Welcome to Concord!")
        thread = threading.Thread(target=handler, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
