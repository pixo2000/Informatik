import pygame
import Spielfeld
import Spielfigur
from Gegenstaende import platziere_gold, platziere_silber, platziere_platin

# Constants
CELL_SIZE = 80
GRID_COLOR = (200, 200, 200)
PLAYER_COLOR = (255, 0, 0)
SILVER_COLOR = (192, 192, 192)
PLATIN_COLOR = (229, 228, 226)

# Load and resize textures
GOLD_TEXTURE = pygame.image.load('texture/ore/gold.png')
GOLD_TEXTURE = pygame.transform.scale(GOLD_TEXTURE, (CELL_SIZE, CELL_SIZE))
SILVER_TEXTURE = pygame.image.load('texture/ore/silver.png')
SILVER_TEXTURE = pygame.transform.scale(SILVER_TEXTURE, (CELL_SIZE, CELL_SIZE))
PLATINUM_TEXTURE = pygame.image.load('texture/ore/platinum.png')
PLATINUM_TEXTURE = pygame.transform.scale(PLATINUM_TEXTURE, (CELL_SIZE, CELL_SIZE))
PLAYER_TEXTURE = pygame.image.load('texture/player.png')
PLAYER_TEXTURE = pygame.transform.scale(PLAYER_TEXTURE, (CELL_SIZE, CELL_SIZE))

# Load background image
BACKGROUND_IMAGE = pygame.image.load('texture/background.jpeg')

def draw_grid(screen, spielfeld):
    for y, row in enumerate(spielfeld):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if cell == 'X':
                player_rect = PLAYER_TEXTURE.get_rect(center=rect.center)
                screen.blit(PLAYER_TEXTURE, player_rect)
            elif cell == 'G':
                gold_rect = GOLD_TEXTURE.get_rect(center=rect.center)
                screen.blit(GOLD_TEXTURE, gold_rect)
            elif cell == 'S':
                silver_rect = SILVER_TEXTURE.get_rect(center=rect.center)
                screen.blit(SILVER_TEXTURE, silver_rect)
            elif cell == 'P':
                platinum_rect = PLATINUM_TEXTURE.get_rect(center=rect.center)
                screen.blit(PLATINUM_TEXTURE, platinum_rect)

def run_pygame():
    pygame.init()

    # Create the game field
    x, y = 0, 0
    mySpielfeld = Spielfeld.erzeuge(15, 10)
    mySpielfeld = Spielfeld.schreibe(mySpielfeld, x, y, "X")
    mySpielfeld = platziere_gold(mySpielfeld, 5)
    mySpielfeld = platziere_silber(mySpielfeld, 3)
    mySpielfeld = platziere_platin(mySpielfeld, 2)

    # Calculate window size
    field_height = len(mySpielfeld)
    field_width = len(mySpielfeld[0])
    WINDOW_SIZE = (field_width * CELL_SIZE, field_height * CELL_SIZE)

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Informatik Game")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                mySpielfeld, x, y = Spielfigur.bewege(mySpielfeld, x, y, event)
                if mySpielfeld[y][x] in ('G', 'S', 'P'):
                    mySpielfeld[y][x] = 'O'
                if mySpielfeld[y][x] in ('G', 'S', 'P'):
                    mySpielfeld[y][x] = 'O'

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        draw_grid(screen, mySpielfeld)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    run_pygame()