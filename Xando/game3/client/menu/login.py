import pygame
import pygame_gui
import ssl
import socket

# Server settings
HOST = 'localhost'
PORT = 52983

# Initialize pygame
pygame.init()

# Set up the display
pygame.display.set_caption('Login Menu')
window_surface = pygame.display.set_mode((800, 600))

# Set up the background
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

# Set up the UI manager
manager = pygame_gui.UIManager((800, 600))

# Create UI elements
username_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 200), (200, 50)), manager=manager)
password_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 270), (200, 50)), manager=manager)
password_input.set_text_hidden(True)

dropdown_menu = pygame_gui.elements.UIDropDownMenu(options_list=['Register', 'Login'],
                                                   starting_option='Register',
                                                   relative_rect=pygame.Rect((350, 340), (200, 50)),
                                                   manager=manager)

quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 410), (200, 50)),
                                           text='Quit',
                                           manager=manager)

# Main loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == quit_button:
                is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

# Clean up
pygame.quit()