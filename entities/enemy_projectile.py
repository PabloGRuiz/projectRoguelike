import pygame
from entities.entity import Entity

class EnemyProjectile(Entity):
    def __init__(self, x, y, dir_x, dir_y, damage, speed=300):
        super().__init__(x, y, 10, (255, 100, 0))
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.damage = damage
        self.speed = speed

        self.lifetime = 5.0 
        self.current_time = 0.0

    def update(self, dt):
        self.velocity.x = self.dir_x * self.speed
        self.velocity.y = self.dir_y * self.speed
        
        super().update(dt)

        self.current_time += dt
        if self.current_time >= self.lifetime:
            self.dead()