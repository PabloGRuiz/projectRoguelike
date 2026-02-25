import pygame
class Entity:
    def __init__(self,x,y,size,color):
        self.pos = pygame.Vector2(x,y)
        self.velocity = pygame.Vector2(0,0)
        self.size = size
        self.color = color
        self.alive = True
        self.live_points = 1
        
    def get_rect(self):
        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = (self.pos.x, self.pos.y)
        return rect
    
    def update(self,dt):
        self.pos += self.velocity * dt
        self.check_alive()
    
    def draw(self,screen):
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