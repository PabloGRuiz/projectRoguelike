import pygame
import settings
from entities.player import Player
from entities.enemy import Enemy
from entities.experience import Experience
from systems.randomCoord import GenerateCoords
from systems.collision import Collision
from systems.combat import Combat

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.reSpawn()
        self.projectiles = []
        self.experiences = []

    def reSpawn(self):
        self.player = Player(400, 250, 5)
        self.enemies = []
        
        for i in range(5):
            spawn_x, spawn_y = GenerateCoords()
            enemy = Enemy(spawn_x, spawn_y, 3, 1)
            self.enemies.append(enemy)
            
    def check_entity_alive(self):
        self.enemies = [e for e in self.enemies if e.alive]
        self.projectiles = [p for p in self.projectiles if p.alive]
        self.experiences = [xp for xp in self.experiences if xp.alive]
        
        if not self.player.alive:
            self.player.can_shoot = False
        elif self.player.alive and len(self.enemies) == 0:
            self.player.can_shoot = False
        else:
            self.player.can_shoot = True
    
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(settings.FPS) / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reSpawn()
            
            # UPDATE
            projectile = self.player.update(dt,self.enemies)
            if projectile:
                self.projectiles.append(projectile)
            
            for enemy in self.enemies:
                enemy.chase(self.player)
                enemy.update(dt)
                
            for projectile in self.projectiles:
                projectile.update(dt)
            
            # COLLISIONS      
            Combat.check_entity_collision(self.player, self.enemies, self.projectiles, self.experiences)
            
            # CLEAN-UP
            self.check_entity_alive()
            
            # DRAW
            self.screen.fill((30,30,30))
            
            if self.player.alive:
                self.player.draw(self.screen)
            
            for enemy in self.enemies:
                enemy.draw(self.screen)
                
            for projectile in self.projectiles:
                projectile.draw(self.screen)
                    
            for xp in self.experiences:
                xp.draw(self.screen)
                            
            pygame.display.flip()
        
        pygame.quit()