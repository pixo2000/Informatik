ˋˋˋpython
import pygame

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]  # Initial player position at the center of the screen
player_speed = 5  # Player movement speed
slow_speed_factor = 0.5  # Speed factor when shift is held
player_radius = 40  # Radius of the player circle
gravity = 1  # Gravity
jump_strength = 20  # Strength of the jump
on_ground = True  # Track if the player is on the ground

# Clock
clock = pygame.time.Clock()  # Clock to control the frame rate

# List to track the order of pressed keys
key_order = []

# Main game loop
running = True
while running:
    screen.fill(BLACK)  # Fill the screen with black color

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the quit event is triggered
            running = False  # Exit the game loop

        # Key press handling
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                if event.key not in key_order:
                    key_order.append(event.key)

        # Key release handling
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                if event.key in key_order:
                    key_order.remove(event.key)

    # Key handling
    keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
    speed = player_speed
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # If shift key is held
        speed *= slow_speed_factor  # Reduce speed

    # Movement logic to prioritize the latest input in opposite directions
    dx, dy = 0, 0

    # Apply gravity
    dy += gravity

    # Make the player jump when [SPACE] is pressed and the player is on the ground
    if keys[pygame.K_SPACE] and on_ground:
        dy -= jump_strength
        on_ground = False

    # Handle horizontal movement
    if pygame.K_a in key_order and pygame.K_d in key_order:
        # If both are pressed, prioritize the latest key
        if key_order.index(pygame.K_a) > key_order.index(pygame.K_d):
            dx -= speed
        else:
            dx += speed
    elif pygame.K_a in key_order:
        dx -= speed
    elif pygame.K_d in key_order:
        dx += speed

    # Apply movement
    player_pos[0] += dx
    player_pos[1] += dy

    # Check if the player is on the ground
    if player_pos[1] >= SCREEN_HEIGHT // 2:
        player_pos[1] = SCREEN_HEIGHT // 2
        on_ground = True

    # Keep the player within the screen bounds
    player_pos[0] = max(player_radius, min(SCREEN_WIDTH - player_radius, player_pos[0]))

    # Draw player
    pygame.draw.circle(screen, GREEN, player_pos, player_radius)  # Draw the player as a green circle

    # Update the display
    pygame.display.flip()  # Refresh the screen
    clock.tick(60)  # Maintain 60 frames per second

# Quit pygame
pygame.quit()
ˋˋˋ