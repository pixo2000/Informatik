import pygame
import importlib
from config import maps, host, port

import socket
import threading

class Player(pygame.sprite.Sprite):
    def __init__(self, obstacles, spawn_x, spawn_y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Green player character
        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))
        self.pressed_keys = []

        # Ensure the player does not spawn inside an obstacle
        while pygame.sprite.spritecollideany(self, obstacles):
            self.rect.x += 10  # Adjust the spawn point
            if self.rect.x > 800:  # Reset if out of bounds
                self.rect.x = 0
                self.rect.y += 10
            if self.rect.y > 600:
                self.rect.y = 0

    def update(self, obstacles):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        # Update the list of currently pressed keys
        if keys[pygame.K_a] and pygame.K_a not in self.pressed_keys:
            self.pressed_keys.append(pygame.K_a)
        if keys[pygame.K_d] and pygame.K_d not in self.pressed_keys:
            self.pressed_keys.append(pygame.K_d)
        if keys[pygame.K_w] and pygame.K_w not in self.pressed_keys:
            self.pressed_keys.append(pygame.K_w)
        if keys[pygame.K_s] and pygame.K_s not in self.pressed_keys:
            self.pressed_keys.append(pygame.K_s)

        # Remove keys that are no longer pressed
        if not keys[pygame.K_a] and pygame.K_a in self.pressed_keys:
            self.pressed_keys.remove(pygame.K_a)
        if not keys[pygame.K_d] and pygame.K_d in self.pressed_keys:
            self.pressed_keys.remove(pygame.K_d)
        if not keys[pygame.K_w] and pygame.K_w in self.pressed_keys:
            self.pressed_keys.remove(pygame.K_w)
        if not keys[pygame.K_s] and pygame.K_s in self.pressed_keys:
            self.pressed_keys.remove(pygame.K_s)

        # Determine movement based on the most recent key press
        if self.pressed_keys:
            last_key = self.pressed_keys[-1]
            if last_key == pygame.K_a:
                dx -= 5
            if last_key == pygame.K_d:
                dx += 5
            if last_key == pygame.K_w:
                dy -= 5
            if last_key == pygame.K_s:
                dy += 5

        # Move the player horizontally and check for collisions
        self.rect.x += dx
        if pygame.sprite.spritecollideany(self, obstacles):
            self.rect.x -= dx  # Undo the horizontal move if there's a collision

        # Move the player vertically and check for collisions
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, obstacles):
            self.rect.y -= dy  # Undo the vertical move if there's a collision

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("2D Shooter")
    return screen

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update_game_state(player, obstacles):
    player.update(obstacles)

def render_game(screen, player, all_sprites, obstacles):
    screen.fill((0, 0, 0))

    # Calculate the offset to center the player
    offset_x = screen.get_width() // 2 - player.rect.centerx
    offset_y = screen.get_height() // 2 - player.rect.centery

    # Draw all sprites with the calculated offset
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

    # Draw obstacles with the calculated offset
    for obstacle in obstacles:
        screen.blit(obstacle.image, (obstacle.rect.x + offset_x, obstacle.rect.y + offset_y))

    pygame.display.flip()

def instant_quit(app):
    app.running = False

def receive_data(sock, app):
    while app.running:
        try:
            data = sock.recv(1024)
            if not data:
                break
            # Handle the received data (e.g., update game state)
        except:
            break
    sock.close()

def run_game(selected_map, start_button, app):
    # Initialize the game
    screen = initialize_game()
    clock = pygame.time.Clock()

    # Connect to the server
    server_address = (host, port)  # Replace with your server's address and port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    # Start a thread to receive data from the server
    receive_thread = threading.Thread(target=receive_data, args=(sock, app))
    receive_thread.start()

    # Load the map and initialize the player
    map_config = maps[selected_map]
    map_module = importlib.import_module(f"maps.{map_config['File'].split('.')[0]}")
    game_map = map_module.Map()

    spawn_x = map_config["Spawn"]["X"]
    spawn_y = map_config["Spawn"]["Y"]
    player = Player(game_map.obstacles, spawn_x, spawn_y)
    all_sprites = pygame.sprite.Group(player)

    while app.running:
        if not handle_events():
            break
        update_game_state(player, game_map.obstacles)
        render_game(screen, player, all_sprites, game_map.obstacles)
        clock.tick(60)

        # Send player state to the server
        player_state = f"{player.rect.x},{player.rect.y}"
        sock.sendall(player_state.encode())

        # Check if instant_quit is triggered
        if not app.running:
            pygame.quit()
            break

    pygame.quit()
    start_button.pack(pady=20)  # Add the start button back after the game ends
    app.game_running = False  # Reset the flag when the game ends
    sock.close()