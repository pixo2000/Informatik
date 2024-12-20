import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")

# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Button dimensions
button_width = 200
button_height = 50

# Button positions
start_button_pos = (screen_width // 2 - button_width // 2, screen_height // 2 - button_height // 2 - 60)
quit_button_pos = (screen_width // 2 - button_width // 2, screen_height // 2 - button_height // 2 + 60)

def draw_button(text, position):
    button_rect = pygame.Rect(position[0], position[1], button_width, button_height)
    pygame.draw.rect(screen, gray, button_rect)
    text_surface = button_font.render(text, True, black)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def main_menu():
    while True:
        screen.fill(white)

        # Draw buttons
        start_button = draw_button("Start", start_button_pos)
        quit_button = draw_button("Quit", quit_button_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    print("Start button clicked")
                    # Add code to start the game
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()