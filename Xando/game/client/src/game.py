import pygame
import importlib
from config import maps
from gui import create_gui

class Player(pygame.sprite.Sprite):
    def __init__(self, obstacles, spawn_x, spawn_y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Green player character
        self.rect = self.image.get_rect(center=(spawn_x, spawn_y))

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
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # Check for collisions with obstacles
        if pygame.sprite.spritecollideany(self, obstacles):
            if keys[pygame.K_LEFT]:
                self.rect.x += 5
            if keys[pygame.K_RIGHT]:
                self.rect.x -= 5
            if keys[pygame.K_UP]:
                self.rect.y += 5
            if keys[pygame.K_DOWN]:
                self.rect.y -= 5

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

def render_game(screen, all_sprites, obstacles):
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    obstacles.draw(screen)
    pygame.display.flip()

def run_game(selected_map):
    screen = initialize_game()
    clock = pygame.time.Clock()

    map_config = maps[selected_map]
    map_module = importlib.import_module(f"maps.{map_config['File'].split('.')[0]}")
    game_map = map_module.Map()

    spawn_x = map_config["Spawn"]["X"]
    spawn_y = map_config["Spawn"]["Y"]
    player = Player(game_map.obstacles, spawn_x, spawn_y)
    all_sprites = pygame.sprite.Group(player)

    running = True
    while running:
        running = handle_events()
        update_game_state(player, game_map.obstacles)
        render_game(screen, all_sprites, game_map.obstacles)
        clock.tick(60)

    pygame.quit()
    create_gui(run_game)  # Return to GUI after quitting the game