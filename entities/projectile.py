import pygame
import settings
import systems.collision
from entities.entity import Entity


class Projectile(Entity):
    def __init__(self, x, y, dmg):
        super().__init__(x, y, 5, (250,250,250))
        self.damage = dmg
        
    def shoot(self,targets):
        closerTarget = None
        min_dist = float('inf')
        for target in targets:
            dist = (target.pos - self.pos).length()
            if dist < min_dist:
                min_dist = dist
                closerTarget = target
        if closerTarget:
            direction = closerTarget.pos - self.pos
            if direction.length() > 0:
                self.velocity = direction.normalize() * settings.PROJECTILE_SPEED
                
    def update(self, dt):
        if (self.pos.x < 0 or self.pos.x > settings.WIDTH 
            or 
            self.pos.y < 0 or self.pos.y > settings.HEIGHT):
            super().dead()
        super().update(dt)
    
    def draw(self,screen):
        pygame.draw.circle(
            screen,
            self.color,
            self.pos,
            self.size
        )