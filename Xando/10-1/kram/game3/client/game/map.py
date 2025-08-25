import pygame

class Map:
    def __init__(self):
        self.width = 1600
        self.height = 1200
        self.blocks = [
            (100, 100, 50, 50),
            (300, 200, 100, 50),
            (500, 500, 200, 100)
        ]
        self.world_border = (0, 0, self.width, self.height)

    def draw(self, screen):
        for block in self.blocks:
            pygame.draw.rect(screen, (255, 0, 0), block)
        pygame.draw.rect(screen, (255, 255, 255), self.world_border, 5)