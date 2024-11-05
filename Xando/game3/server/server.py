import socket
import ssl
import threading
from auth import authenticate_user, register_user, delete_user_by_username, change_user_password, reset_user_password

# Server settings
HOST = 'localhost'
PORT = 12345


# Function to handle each client connection
def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            command_parts = data.strip().split()
            command = command_parts[0]

            if command == "register":
                username = command_parts[1]
                password = command_parts[2]
                register_user(username, password)
                client_socket.send("Registration complete!\n".encode())
            elif command == "login":
                username = command_parts[1]
                password = command_parts[2]
                if authenticate_user(username, password):
                    client_socket.send("Login successful!\n".encode())
                else:
                    client_socket.send("Login failed!\n".encode())
            elif command == "change_password":
                username = command_parts[1]
                current_password = command_parts[2]
                new_password = command_parts[3]
                if change_user_password(username, current_password, new_password):
                    client_socket.send("Password changed successfully!\n".encode())
                else:
                    client_socket.send("Failed to change password. Please check your current password.\n".encode())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


# Set up and run the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Set up SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="assets/ssl/certfile.pem", keyfile="assets/ssl/keyfile.pem")

print(f"Server running on {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()
    print(f"New connection from {addr}")
    ssl_client_socket = context.wrap_socket(client_socket, server_side=True)
    client_handler = threading.Thread(target=handle_client, args=(ssl_client_socket,))
    client_handler.start()
