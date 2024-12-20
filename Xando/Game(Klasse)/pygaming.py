import pygame
import Spielfeld
import Spielfigur
from Gegenstaende import platziere_gold, platziere_silber, platziere_platin

# Constants
WINDOW_SIZE = (800, 800)
CELL_SIZE = 80
GRID_COLOR = (200, 200, 200)
PLAYER_COLOR = (255, 0, 0)
GOLD_COLOR = (255, 215, 0)
SILVER_COLOR = (192, 192, 192)
PLATIN_COLOR = (229, 228, 226)

def draw_grid(screen, spielfeld):
    for y, row in enumerate(spielfeld):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if cell == 'X':
                pygame.draw.circle(screen, PLAYER_COLOR, rect.center, CELL_SIZE // 3)
            elif cell == 'G':
                pygame.draw.circle(screen, GOLD_COLOR, rect.center, CELL_SIZE // 3)
            elif cell == 'S':
                pygame.draw.circle(screen, SILVER_COLOR, rect.center, CELL_SIZE // 3)
            elif cell == 'P':
                pygame.draw.circle(screen, PLATIN_COLOR, rect.center, CELL_SIZE // 3)

def run_pygame():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Xando Game")

    x, y = 0, 0
    mySpielfeld = Spielfeld.erzeuge(10, 10)
    mySpielfeld = Spielfeld.schreibe(mySpielfeld, x, y, "X")
    mySpielfeld = platziere_gold(mySpielfeld, 5)
    mySpielfeld = platziere_silber(mySpielfeld, 3)
    mySpielfeld = platziere_platin(mySpielfeld, 2)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                mySpielfeld, x, y = Spielfigur.bewege(mySpielfeld, x, y, event)

        screen.fill((0, 0, 0))
        draw_grid(screen, mySpielfeld)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    run_pygame()