import socket
import threading
from game import Game  # Assuming you have a Game class to manage game state
from config import port  # Import the port from the config

clients = []
game = Game()  # Initialize game state

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            # Process the message and update game state
            game.update_state(message)
            broadcast(game.get_state())
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(state):
    for client in clients:
        try:
            client.sendall(state.encode('utf-8'))
        except:
            clients.remove(client)
            client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))  # Bind to all interfaces using the imported port
    server.listen(5)
    print(f'Server started on port {port}')

    while True:
        client_socket, addr = server.accept()
        print(f'Connection from {addr}')
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()