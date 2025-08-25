import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (0, 255, 0)
        self.speed = 5
        self.jump_power = 15
        self.velocity_y = 0
        self.gravity = 0.8
        self.is_jumping = False
        self.on_ground = False
        
        # Key tracking
        self.key_order = []
    
    def update(self, map):
        # Store old position for collision resolution
        old_x = self.x
        old_y = self.y
        
        # Handle keyboard input
        keys = pygame.key.get_pressed()
        
        # Movement
        dx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
        
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = -self.jump_power
            self.is_jumping = True
            self.on_ground = False
        
        # Apply gravity
        self.velocity_y += self.gravity
        
        # Apply movement
        self.x += dx
        self.y += self.velocity_y
        
        # Update rectangle
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Check platform collision
        platform_rect = map.check_collision(self.rect)
        if platform_rect:
            # Landing on top of platform
            if self.velocity_y > 0 and old_y + self.height <= platform_rect.top + 10:
                self.rect.bottom = platform_rect.top
                self.y = self.rect.y
                self.velocity_y = 0
                self.on_ground = True
                self.is_jumping = False
            # Hitting bottom of platform
            elif self.velocity_y < 0 and old_y >= platform_rect.bottom - 10:
                self.rect.top = platform_rect.bottom
                self.y = self.rect.y
                self.velocity_y = 0
            # Side collision
            else:
                self.x = old_x
                self.rect.x = old_x
        else:
            self.on_ground = False
        
        # Map boundaries instead of screen boundaries
        if self.x < 0:
            self.x = 0
            self.rect.x = 0
        if self.x > map.width - self.width:
            self.x = map.width - self.width
            self.rect.x = map.width - self.width
        if self.y > map.height:
            self.y = map.height - self.height
            self.rect.y = map.height - self.height
            self.velocity_y = 0
            self.on_ground = True
        
        # Check coin collection
        map.collect_coins(self.rect)
    
    def draw(self, screen, camera_offset_x, camera_offset_y):
        # Draw player with camera offset
        adjusted_rect = pygame.Rect(
            self.rect.x - camera_offset_x,
            self.rect.y - camera_offset_y,
            self.rect.width,
            self.rect.height
        )
        pygame.draw.rect(screen, self.color, adjusted_rect)
        
        # Draw eyes with camera offset
        eye_radius = 5
        eye_offset_x = 10
        eye_offset_y = 15
        
        pygame.draw.circle(screen, (255, 255, 255), 
                          (self.x + eye_offset_x - camera_offset_x, 
                           self.y + eye_offset_y - camera_offset_y), eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), 
                          (self.x + self.width - eye_offset_x - camera_offset_x, 
                           self.y + eye_offset_y - camera_offset_y), eye_radius)
