# map.py

import pygame
import math

# Map settings
MAP_WIDTH, MAP_HEIGHT = 800, 600
BLOCK_SIZE = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_speed = 5
slow_speed_factor = 0.5
player_radius = 10

# Initialize pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
pygame.display.set_caption("Labyrinth")

# Define the world border
world_border = pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)

# Define a few blocks
blocks = [
    pygame.Rect(200, 150, BLOCK_SIZE, BLOCK_SIZE),
]

# Define the spawn point
spawn_point = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
player_pos = list(spawn_point)

# List to track the order of pressed keys
key_order = []

# Clock
clock = pygame.time.Clock()

# Function to get angle to the mouse position
def get_angle_to_mouse(player_pos):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - player_pos[0]
    dy = mouse_y - player_pos[1]
    return math.degrees(math.atan2(dy, dx))

# Function to check for collisions
def check_collision(new_pos):
    player_rect = pygame.Rect(new_pos[0] - player_radius, new_pos[1] - player_radius, player_radius * 2, player_radius * 2)
    for block in blocks:
        if player_rect.colliderect(block):
            return True
    return False

# Main loop
running = True
while running:
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

    player_pos[0] = max(player_radius, min(MAP_WIDTH - player_radius, player_pos[0]))
    player_pos[1] = max(player_radius, min(MAP_HEIGHT - player_radius, player_pos[1]))

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, world_border, 5)

    for block in blocks:
        pygame.draw.rect(screen, RED, block)

    angle = get_angle_to_mouse(player_pos)
    pygame.draw.circle(screen, GREEN, player_pos, player_radius)
    stick_length = 50
    end_x = player_pos[0] + stick_length * math.cos(math.radians(angle))
    end_y = player_pos[1] + stick_length * math.sin(math.radians(angle))
    pygame.draw.line(screen, GREEN, player_pos, (end_x, end_y), 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()