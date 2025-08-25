import pygame

# Map settings
MAP_WIDTH, MAP_HEIGHT = 800, 600
BLOCK_SIZE = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
pygame.display.set_caption("Map with World Border and Blocks")

# Define the world border
world_border = pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)

# Define a few blocks
blocks = [
    pygame.Rect(200, 150, BLOCK_SIZE, BLOCK_SIZE),
]

# Define the spawn point
spawn_point = (MAP_WIDTH // 2, MAP_HEIGHT // 2)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, world_border, 5)

    for block in blocks:
        pygame.draw.rect(screen, RED, block)

    pygame.display.flip()

pygame.quit()