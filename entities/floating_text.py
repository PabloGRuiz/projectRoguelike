import pygame

class FloatingText:
    def __init__(self, x, y, text, color=(200, 200, 50)):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, -50)
        self.text = str(text)
        self.color = color
        
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        
        self.alive = True
        self.lifetime = 0.5
        self.current_time = 0
        
    def update(self, dt):
        self.pos += self.velocity * dt
        self.current_time += dt

        if self.current_time >= self.lifetime:
            self.alive = False

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.pos.x, self.pos.y))
        screen.blit(text_surface, text_rect)