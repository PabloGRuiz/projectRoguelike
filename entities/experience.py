import pygame
import math
from entities.entity import Entity

class Experience(Entity):
    def __init__(self, x, y, xp):
        super().__init__(x, y, 6, (20, 20, 200))
        self.experience = xp
        # --- MAGNET SYSTEM ---
        self.target = None
        self.magnet_speed = 800 
        
        # --- PRE-RENDER ---
        surface_size = self.size * 2
        self.image = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        center = (self.size, self.size)
        points = self.generate_star_points(center, 5, self.size, self.size / 2.5)
        pygame.draw.polygon(self.image, self.color, points)
        
    def generate_star_points(self, center, num_points, outer_rad, inner_rad):
        points = []
        angle = -math.pi / 2 
        angle_step = math.pi / num_points 
        
        for i in range(num_points * 2):
            radius = outer_rad if i % 2 == 0 else inner_rad
            x = center[0] + math.cos(angle) * radius
            y = center[1] + math.sin(angle) * radius
            points.append((x, y))
            angle += angle_step
            
        return points

    def update(self, dt):
        # --- MAGNET LOGIC ---
        if self.target and self.target.alive:
            direction = self.target.pos - self.pos
            if direction.length() > 0:
                self.velocity = direction.normalize() * self.magnet_speed
                
        super().update(dt)

    def draw_entity(self, screen):
        # --- DRAW ---
        screen.blit(self.image, (self.pos.x - self.size, self.pos.y - self.size))