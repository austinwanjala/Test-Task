import socket
import threading
import time
import ssl
import os
from typing import Tuple

CONFIG_FILE = 'config.txt'
MAX_PAYLOAD_SIZE = 1024
BUFFER_SIZE = 4096
REREAD_ON_QUERY = True  # This can be set to False in the config file
SSL_ENABLED = True  # This can also be set to False in the config file
FILE_PATH = ""

# Load configuration
def load_config():
    global FILE_PATH, REREAD_ON_QUERY, SSL_ENABLED
    with open(CONFIG_FILE, 'r') as file:
        for line in file:
            if line.startswith("linuxpath="):
                FILE_PATH = line.split('=')[1].strip()
            elif line.startswith("REREAD_ON_QUERY="):
                REREAD_ON_QUERY = line.split('=')[1].strip().lower() == 'true'
            elif line.startswith("SSL_ENABLED="):
                SSL_ENABLED = line.split('=')[1].strip().lower() == 'true'

# Search for a string in the file
def search_in_file(query: str) -> str:
    if REREAD_ON_QUERY:
        with open(FILE_PATH, 'r') as file:
            lines = file.readlines()
    else:
        if not hasattr(search_in_file, 'lines'):
            with open(FILE_PATH, 'r') as file:
                search_in_file.lines = file.readlines()
        lines = search_in_file.lines

    if query + '\n' in lines:
        return "STRING EXISTS\n"
    else:
        return "STRING NOT FOUND\n"

# Handle client connections
def handle_client(client_socket: socket.socket, address: Tuple[str, int]):
    start_time = time.time()
    try:
        data = client_socket.recv(MAX_PAYLOAD_SIZE).decode().strip('\x00')
        response = search_in_file(data)
        execution_time = time.time() - start_time
        log_message = f"DEBUG: Query: '{data}', IP: {address}, Execution Time: {execution_time:.6f} seconds\n"
        print(log_message.strip())
        client_socket.send(response.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Start the server
def start_server():
    load_config()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if SSL_ENABLED:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        server_socket = context.wrap_socket(server_socket, server_side=True)

    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(5)
    print("Server listening on port 9999...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
