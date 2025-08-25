import pygame
import sys
from map import Map
from movement import Player

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platform Jumper")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Camera class to follow the player
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.offset_x = 0
        self.offset_y = 0
    
    def update(self, target_x, target_y, map_width, map_height):
        # Center the camera on the player
        self.offset_x = target_x - self.width // 2
        self.offset_y = target_y - self.height // 2
        
        # Keep camera within map bounds
        self.offset_x = max(0, min(self.offset_x, map_width - self.width))
        self.offset_y = max(0, min(self.offset_y, map_height - self.height))

def start_game(map_name="default"):
    # Create player
    player = Player(50, 400)
    
    # Create and load map
    game_map = Map()
    game_map.load_map(map_name)
    
    # Create camera
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen
        screen.fill(BLACK)
        
        # Update map platforms
        game_map.update()
        
        # Update player
        player.update(game_map)
        
        # Update camera to follow player
        camera.update(player.x + player.width // 2, 
                     player.y + player.height // 2,
                     game_map.width, game_map.height)
        
        # Draw map with camera offset
        game_map.draw(screen, camera.offset_x, camera.offset_y)
        
        # Draw player with camera offset
        player.draw(screen, camera.offset_x, camera.offset_y)
        
        # Check if all coins are collected
        all_collected = all(coin.collected for coin in game_map.coins)
        if all_collected:
            font = pygame.font.SysFont(None, 72)
            win_text = font.render("You collected all coins!", True, WHITE)
            screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, SCREEN_HEIGHT//2 - 36))
            
            continue_text = font.render("Press ESC to return to menu", True, WHITE)
            screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + 36))
            
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    # Main menu
    font = pygame.font.SysFont(None, 48)
    
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        
        title = font.render("Platform Jumper", True, WHITE)
        start_text = font.render("Press SPACE to Start", True, WHITE)
        quit_text = font.render("Press ESC to Quit", True, WHITE)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 200))
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 280))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 340))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_running = False
                    start_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
