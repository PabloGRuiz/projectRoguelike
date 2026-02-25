import pygame
from entities.entity import Entity

class Experience(Entity):
    def __init__(self, x, y, xp):
        super().__init__(x, y, 3, (20,20,150))
        self.experience = xp
    
    def draw(self,screen):
        pygame.draw.circle(
            screen,
            self.color,
            self.pos,
            self.size
        )