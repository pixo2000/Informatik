# test.py
# aufgabe: einfach n labyrinth mit einer möglichen lösung generieren lassen

import pygame
import math
import importlib

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player settings
player_speed = 5
slow_speed_factor = 0.5
player_radius = 10

# Clock
clock = pygame.time.Clock()

# List to track the order of pressed keys
key_order = []

# Function to get angle to the mouse position
def get_angle_to_mouse(player_pos):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - player_pos[0]
    dy = mouse_y - player_pos[1]
    return math.degrees(math.atan2(dy, dx))

# Select map
map_name = input("Enter the map name (without .py extension): ")
map_module = importlib.import_module(map_name)

# Use the spawn point from the selected map
player_pos = list(map_module.spawn_point)
blocks = map_module.blocks
world_border = map_module.world_border

# Function to check for collisions
def check_collision(new_pos):
    player_rect = pygame.Rect(new_pos[0] - player_radius, new_pos[1] - player_radius, player_radius * 2, player_radius * 2)
    if not world_border.contains(player_rect):
        return True
    for block in blocks:
        if player_rect.colliderect(block):
            return True
    return False

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                if event.key not in key_order:
                    key_order.append(event.key)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                if event.key in key_order:
                    key_order.remove(event.key)

    keys = pygame.key.get_pressed()
    speed = player_speed
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        speed *= slow_speed_factor

    dx, dy = 0, 0

    if pygame.K_w in key_order and pygame.K_s in key_order:
        if key_order.index(pygame.K_w) > key_order.index(pygame.K_s):
            dy -= speed
        else:
            dy += speed
    elif pygame.K_w in key_order:
        dy -= speed
    elif pygame.K_s in key_order:
        dy += speed

    if pygame.K_a in key_order and pygame.K_d in key_order:
        if key_order.index(pygame.K_a) > key_order.index(pygame.K_d):
            dx -= speed
        else:
            dx += speed
    elif pygame.K_a in key_order:
        dx -= speed
    elif pygame.K_d in key_order:
        dx += speed

    new_pos = [player_pos[0] + dx, player_pos[1] + dy]
    if not check_collision(new_pos):
        player_pos = new_pos

    # Center the camera on the player
    camera_x = player_pos[0] - SCREEN_WIDTH // 2
    camera_y = player_pos[1] - SCREEN_HEIGHT // 2

    # Draw the world border
    pygame.draw.rect(screen, WHITE, world_border.move(-camera_x, -camera_y), 5)

    # Draw the blocks
    for block in blocks:
        pygame.draw.rect(screen, RED, block.move(-camera_x, -camera_y))

    # Draw player
    angle = get_angle_to_mouse(player_pos)
    pygame.draw.circle(screen, GREEN, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), player_radius)
    stick_length = 50
    end_x = SCREEN_WIDTH // 2 + stick_length * math.cos(math.radians(angle))
    end_y = SCREEN_HEIGHT // 2 + stick_length * math.sin(math.radians(angle))
    pygame.draw.line(screen, GREEN, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (end_x, end_y), 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()