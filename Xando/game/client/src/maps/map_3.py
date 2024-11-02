import pygame

class Map:
    def __init__(self):
        self.obstacles = pygame.sprite.Group()
        self.create_world_border()
        self.create_obstacles()

    def create_world_border(self):
        border_thickness = 10
        screen_width, screen_height = 1000, 600
        borders = [
            pygame.Rect(0, 0, screen_width, border_thickness),  # Top border
            pygame.Rect(0, 0, border_thickness, screen_height),  # Left border
            pygame.Rect(0, screen_height - border_thickness, screen_width, border_thickness),  # Bottom border
            pygame.Rect(screen_width - border_thickness, 0, border_thickness, screen_height)  # Right border
        ]
        for border in borders:
            obstacle = pygame.sprite.Sprite()
            obstacle.image = pygame.Surface((border.width, border.height))
            obstacle.image.fill((255, 0, 0))  # Red color for borders
            obstacle.rect = border
            self.obstacles.add(obstacle)

    def create_obstacles(self):
        obstacle_positions = [
            (100, 100, 200, 50),
            (300, 200, 100, 150),
            (500, 350, 150, 50),
            (650, 100, 50, 200)
        ]
        for pos in obstacle_positions:
            obstacle = pygame.sprite.Sprite()
            obstacle.image = pygame.Surface((pos[2], pos[3]))
            obstacle.image.fill((0, 0, 255))  # Blue color for obstacles
            obstacle.rect = pygame.Rect(pos)
            self.obstacles.add(obstacle)