import pygame
import time

class Platform:
    def __init__(self, x, y, width, height, color=(0, 255, 0), permanent=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.visible = True
        self.touch_time = None
        self.disappear_time = None
        self.permanent = permanent  # Flag to mark platforms that should never disappear
    
    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect)
    
    def handle_collision(self, current_time):
        # Only start the disappear countdown for non-permanent platforms
        if self.visible and not self.permanent and self.touch_time is None:
            self.touch_time = current_time
    
    def update(self, current_time):
        # Permanent platforms never disappear
        if self.permanent:
            return
            
        # Check if platform should disappear
        if self.visible and self.touch_time is not None:
            if current_time - self.touch_time >= 3:  # 3 seconds after touch
                self.visible = False
                self.disappear_time = current_time
                self.touch_time = None
        
        # Check if platform should reappear
        if not self.visible and self.disappear_time is not None:
            if current_time - self.disappear_time >= 10:  # 10 seconds after disappearing
                self.visible = True
                self.disappear_time = None

class Coin:
    def __init__(self, x, y, radius=15):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.collected = False
        self.color = (255, 215, 0)  # Gold color
    
    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Map:
    def __init__(self):
        self.platforms = []
        self.coins = []
        self.score = 0
        self.width = 2400  # Larger map width
        self.height = 800  # Larger map height
    
    def load_map(self, map_name="default"):
        # Clear existing map
        self.platforms.clear()
        self.coins.clear()
        self.score = 0
        
        if map_name == "default":
            # Create floor - mark as permanent so it doesn't disappear
            self.platforms.append(Platform(0, 700, self.width, 20, permanent=True))
            
            # Create some platforms - now spread across a larger area
            self.platforms.append(Platform(100, 600, 200, 20))
            self.platforms.append(Platform(400, 550, 150, 20))
            self.platforms.append(Platform(700, 450, 200, 20))
            self.platforms.append(Platform(1000, 500, 150, 20))
            self.platforms.append(Platform(1300, 400, 200, 20))
            self.platforms.append(Platform(1600, 350, 150, 20))
            self.platforms.append(Platform(1900, 450, 200, 20))
            self.platforms.append(Platform(2200, 550, 150, 20))
            self.platforms.append(Platform(200, 350, 100, 20))
            self.platforms.append(Platform(500, 300, 200, 20))
            self.platforms.append(Platform(900, 250, 150, 20))
            self.platforms.append(Platform(1200, 200, 100, 20))
            self.platforms.append(Platform(1500, 150, 200, 20))
            
            # Add coins spread across the map
            self.coins.append(Coin(200, 570))
            self.coins.append(Coin(450, 520))
            self.coins.append(Coin(800, 420))
            self.coins.append(Coin(1050, 470))
            self.coins.append(Coin(1400, 370))
            self.coins.append(Coin(1650, 320))
            self.coins.append(Coin(2000, 420))
            self.coins.append(Coin(250, 320))
            self.coins.append(Coin(600, 270))
            self.coins.append(Coin(950, 220))
            self.coins.append(Coin(1250, 170))
            self.coins.append(Coin(1600, 120))
    
    def draw(self, screen, camera_offset_x, camera_offset_y):
        # Draw platforms with camera offset
        for platform in self.platforms:
            adjusted_rect = pygame.Rect(
                platform.rect.x - camera_offset_x,
                platform.rect.y - camera_offset_y,
                platform.rect.width,
                platform.rect.height
            )
            if platform.visible:
                pygame.draw.rect(screen, platform.color, adjusted_rect)
        
        # Draw coins with camera offset
        for coin in self.coins:
            if not coin.collected:
                adjusted_pos = (coin.x - camera_offset_x, coin.y - camera_offset_y)
                pygame.draw.circle(screen, coin.color, adjusted_pos, coin.radius)
        
        # Draw score (fixed position on screen, not affected by camera)
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Show remaining coins
        coins_left = sum(1 for coin in self.coins if not coin.collected)
        coins_text = font.render(f"Coins left: {coins_left}", True, (255, 255, 255))
        screen.blit(coins_text, (10, 50))
    
    def check_collision(self, player_rect):
        current_time = time.time()  # Get current time
        
        # Check platform collision
        for platform in self.platforms:
            if player_rect.colliderect(platform.rect) and platform.visible:
                platform.handle_collision(current_time)
                return platform.rect
        return None
    
    def collect_coins(self, player_rect):
        for coin in self.coins:
            if not coin.collected and player_rect.colliderect(coin.rect):
                coin.collected = True
                self.score += 1
                return True
        return False
    
    def update(self):
        current_time = time.time()
        for platform in self.platforms:
            platform.update(current_time)
