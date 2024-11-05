# Camera is NOT attatched to player
# i think only one player is renderd
# no server stuff. only the movement
# player cannot move out of screen
# add map so i can do start_game(mapname)


# WICHTIG: noch schräg

import pygame
import math

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

# Player settings
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5
slow_speed_factor = 0.5
player_radius = 10
last_input = None

# Clock
clock = pygame.time.Clock()

# Function to get angle to the mouse position
def get_angle_to_mouse(player_pos):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - player_pos[0]
    dy = mouse_y - player_pos[1]
    return math.degrees(math.atan2(dy, dx))

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()
    speed = player_speed
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        speed *= slow_speed_factor

    # Movement logic with snap-tap-like behavior
    if keys[pygame.K_w]:
        last_input = "w"
    elif keys[pygame.K_a]:
        last_input = "a"
    elif keys[pygame.K_s]:
        last_input = "s"
    elif keys[pygame.K_d]:
        last_input = "d"
    else:
        last_input = None

    if last_input == "w":
        player_pos[1] -= speed
    elif last_input == "a":
        player_pos[0] -= speed
    elif last_input == "s":
        player_pos[1] += speed
    elif last_input == "d":
        player_pos[0] += speed

    # Keep the player within the screen bounds
    player_pos[0] = max(player_radius, min(SCREEN_WIDTH - player_radius, player_pos[0]))
    player_pos[1] = max(player_radius, min(SCREEN_HEIGHT - player_radius, player_pos[1]))

    # Draw player
    angle = get_angle_to_mouse(player_pos)
    pygame.draw.circle(screen, GREEN, player_pos, player_radius)

    # Draw green stick in the direction of the mouse
    stick_length = 50
    end_x = player_pos[0] + stick_length * math.cos(math.radians(angle))
    end_y = player_pos[1] + stick_length * math.sin(math.radians(angle))
    pygame.draw.line(screen, GREEN, player_pos, (end_x, end_y), 3)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit pygame
pygame.quit()