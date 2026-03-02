import pygame
import settings
from entities.entity import Entity
from entities.projectile import Projectile 

class Player(Entity):
    def __init__(self, x, y, lp):
        super().__init__(x, y, 30, (50,200,50))
        self.live_points = lp
        self.shoot_timer = 0
        self.shoot_cooldown = 0.8
        self.shoot_damage = 1
        self.can_shoot = False
        
        self.speed = 250
        
        self.xp = 0 
        self.level = 1
        self.xp_necesaria = 3
        self.leveled_up = False
        
    def handle_input(self):
        if self.alive:
            keys = pygame.key.get_pressed()
            self.velocity.x = 0
            self.velocity.y = 0
            
            if keys[pygame.K_a]:
                self.velocity.x = -self.speed
            if keys[pygame.K_d]:
                self.velocity.x = self.speed
            if keys[pygame.K_w]:
                self.velocity.y = -self.speed
            if keys[pygame.K_s]:
                self.velocity.y = self.speed
                    
    def update(self, dt, targets):
        self.limit()
        self.handle_input()
        
        projectile = None
        
        self.shoot_timer += dt
        if self.shoot_timer > self.shoot_cooldown and self.can_shoot:
            self.shoot_timer = 0
            projectile = self.create_projectiles(targets)
        
        super().update(dt)
        return projectile
    
    def create_projectiles(self, targets):
        projectile = Projectile(self.pos.x, self.pos.y, self.shoot_damage)
        projectile.shoot(targets)
        return projectile

    def level_up(self, xp):
        self.xp += xp
        
        if self.xp >= self.xp_necesaria:
            self.xp -= self.xp_necesaria
            self.level += 1
            self.xp_necesaria = int(self.xp_necesaria * 1.5) 
            
            self.leveled_up = True

    def limit(self):
        self.pos.x = max(0, min(self.pos.x, settings.WIDTH))
        self.pos.y = max(0, min(self.pos.y, settings.HEIGHT))