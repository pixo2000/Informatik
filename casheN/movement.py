# Camera is NOT attatched to player
# i think only one player is renderd
# no server stuff. only the movement
# player cannot move out of screen
# add map so i can do start_game(mapname)
# check if keys value gets clear so not crash pls

# This is made with basically 0 experience and a tiny bit of Google

# Tip: make player slower and and rezise player etc

import pygame
import math
import time

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
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]  # Initial player position at the center of the screen
player_speed = 5  # Player movement speed
slow_speed_factor = 0.5  # Speed factor when shift is held
player_radius = 40  # Radius of the player circle
gravity = 1 # Gravity
# player_jumpstate = False

# Clock
clock = pygame.time.Clock()  # Clock to control the frame rate

# List to track the order of pressed keys
key_order = []

# Function to get angle to the mouse position
# def get_angle_to_mouse(player_pos):
#    mouse_x, mouse_y = pygame.mouse.get_pos()  # Get current mouse position
#    dx = mouse_x - player_pos[0]  # Difference in x-axis
#    dy = mouse_y - player_pos[1]  # Difference in y-axis
#    return math.degrees(math.atan2(dy, dx))  # Calculate angle in degrees

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


    dy += gravity # Make the player return to his default Y coordinate after jumping

    # Make the player jump when [SPACE] is pressed
    if keys[pygame.K_SPACE]:
        #if player_jumpstate != True:
            #player_jumpstate = True
        dy -= speed
            #player_jumpstate = False

        

    # Handle vertical movement
    #if pygame.K_w in key_order and pygame.K_s in key_order:
        # If both are pressed, prioritize the latest key
        #if key_order.index(pygame.K_w) > key_order.index(pygame.K_s):
            #dy -= speed
        #else:
            #dy += speed
    #elif pygame.K_w in key_order:
        #dy -= speed
    #elif pygame.K_s in key_order:
        #dy += speed

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

    # Keep the player within the screen bounds
    player_pos[0] = max(player_radius, min(SCREEN_WIDTH - player_radius, player_pos[0]))
    player_pos[1] = max(player_radius, min(SCREEN_HEIGHT // 2, player_pos[1]))

    # Draw player
    # angle = get_angle_to_mouse(player_pos)  # Get angle to the mouse position
    pygame.draw.circle(screen, GREEN, player_pos, player_radius)  # Draw the player as a green circle

    # Draw green stick in the direction of the mouse
    #stick_length = 50
    #end_x = player_pos[0] + stick_length * math.cos(math.radians(angle))
    #end_y = player_pos[1] + stick_length * math.sin(math.radians(angle))
    #pygame.draw.line(screen, GREEN, player_pos, (end_x, end_y), 3)  # Draw the stick

    # Update the display
    pygame.display.flip()  # Refresh the screen
    clock.tick(60)  # Maintain 60 frames per second

# Quit pygame
pygame.quit()
