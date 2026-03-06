import pygame

class Entity:
    def __init__(self, x, y, size, color):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.size = size
        self.color = color
        self.alive = True
        self.live_points = 1
        
        # --- BLINKING ---
        self.blink_timer = 0.0
        self.is_blinking = False
        
    def get_rect(self):
        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = (self.pos.x, self.pos.y)
        return rect
    
    def update(self, dt):
        self.pos += self.velocity * dt
        self.check_alive()
        
        # --- BLINKING ---
        if self.is_blinking:
            self.blink_timer -= dt
            if self.blink_timer <= 0:
                self.is_blinking = False

    def trigger_blink(self, duration=0.1):
        self.is_blinking = True
        self.blink_timer = duration
        
    def draw(self, screen):
        # --- BLINKING ---
        if self.is_blinking:
            return
            
        pygame.draw.rect(
            screen,
            self.color,
            self.get_rect()
        )
        
    def check_alive(self):
        if self.live_points <= 0:
            self.dead()       
        
    def dead(self):
        self.alive = False