import socket
import threading
from game import Game  # Assuming you have a Game class to manage game state
from config import port  # Import the port from the config

clients = []
game = Game()  # Initialize game state

def handle_client(client_socket, client_id):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            # Process the message and update game state
            game.update_state(message)
            map_name = game.get_map_name_from_message(message)
            broadcast(game.get_state(), map_name, client_id)
        except:
            client = next((c for c in clients if c['id'] == client_id), None)
            if client:
                clients.remove(client)
            client_socket.close()
            break

def broadcast(state, map_name, sender_id):
    for client in clients:
        try:
            if client['map_name'] == map_name and client['id'] != sender_id:
                client['socket'].sendall(state.encode('utf-8'))
        except:
            clients.remove(client)
            client['socket'].close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))  # Bind to all interfaces using the imported port
    server.listen(5)
    print(f'Server started on port {port}')

    client_id_counter = 0

    while True:
        client_socket, addr = server.accept()
        print(f'Connection from {addr}')
        map_name = receive_initial_map_name(client_socket)
        client_id = client_id_counter
        client_id_counter += 1
        clients.append({'id': client_id, 'socket': client_socket, 'map_name': map_name})
        threading.Thread(target=handle_client, args=(client_socket, client_id)).start()

def receive_initial_map_name(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    if data.startswith("initial_map_name:"):
        map_name = data.split(":")[1]
        return map_name
    else:
        raise ValueError("Expected initial map name")

if __name__ == "__main__":
    start_server()