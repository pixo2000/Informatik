import socket
import threading
from auth import authenticate_user, register_user, delete_user_by_username, change_user_password, reset_user_password

# Server settings
HOST = 'localhost'
PORT = 12345


# Handle each client connection
def handle_client(client_socket):
    try:
        client_socket.send(
            "Do you want to (1) Register, (2) Login, or (3) Delete your account? Press Enter to submit.\n".encode())
        choice = client_socket.recv(1024).decode().strip()

        if choice == '1':
            client_socket.send("Enter username: ".encode())
            username = client_socket.recv(1024).decode().strip()
            client_socket.send("Enter password: ".encode())
            password = client_socket.recv(1024).decode().strip()
            register_user(username, password)
            client_socket.send("Registration complete!\n".encode())
        elif choice == '2':
            client_socket.send("Enter username: ".encode())
            username = client_socket.recv(1024).decode().strip()
            client_socket.send("Enter password: ".encode())
            password = client_socket.recv(1024).decode().strip()
            if authenticate_user(username, password):
                client_socket.send("Login successful!\n".encode())

                # Allow user to change their password after logging in
                client_socket.send("Do you want to change your password? (yes/no) ".encode())
                change_choice = client_socket.recv(1024).decode().strip()

                if change_choice.lower() == 'yes':
                    client_socket.send("Enter your current password: ".encode())
                    current_password = client_socket.recv(1024).decode().strip()
                    client_socket.send("Enter your new password: ".encode())
                    new_password = client_socket.recv(1024).decode().strip()

                    if change_user_password(username, current_password, new_password):
                        client_socket.send("Password changed successfully!\n".encode())
                    else:
                        client_socket.send("Failed to change password. Please check your current password.\n".encode())
            else:
                client_socket.send("Login failed!\n".encode())
        elif choice == '3':
            client_socket.send("Enter username: ".encode())
            username = client_socket.recv(1024).decode().strip()
            client_socket.send("Enter password: ".encode())
            password = client_socket.recv(1024).decode().strip()
            if delete_user_by_username(username):
                client_socket.send("User deleted successfully!\n".encode())
            else:
                client_socket.send("Failed to delete user. Incorrect credentials.\n".encode())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


# Console-based admin interface
def admin_console():
    while True:
        print("\nAdmin Commands:")
        print("1. Delete a user by username")
        print("2. Reset a user's password")
        print("3. Exit admin console")
        command = input("Enter command number: ").strip()

        if command == '1':
            username = input("Enter the username of the user to delete: ").strip()
            if delete_user_by_username(username):
                print(f"User '{username}' deleted successfully.")
            else:
                print(f"User '{username}' not found.")
        elif command == '2':
            username = input("Enter the username of the user to reset password: ").strip()
            new_password = input("Enter the new password: ").strip()
            if reset_user_password(username, new_password):
                print(f"Password for user '{username}' reset successfully.")
            else:
                print(f"User '{username}' not found.")
        elif command == '3':
            print("Exiting admin console.")
            break
        else:
            print("Invalid command. Please try again.")


# Set up and run the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server running on {HOST}:{PORT}")
# Run the admin console in a separate thread
admin_thread = threading.Thread(target=admin_console, daemon=True)
admin_thread.start()

while True:
    client_socket, addr = server.accept()
    print(f"New connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
