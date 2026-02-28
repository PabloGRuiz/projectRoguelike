import pygame
import settings

from entities.player import Player

from systems.combat import Combat
from core.data_manager import ENEMY_DB, ITEMS_DB
from systems.spawner import Spawner
from systems.timer import Timer
from GUI.playerUI import PlayerUI   

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.reSpawn()
        self.projectiles = []
        self.experiences = []
        self.floating_texts = []

    def reSpawn(self):
        self.player = Player(400, 250, 5)
        self.enemies = []
        self.items = []
        self.spawner = Spawner(self.enemies, self.items)
        self.game_timer = Timer()
        
    def check_entity_alive(self):
        self.enemies[:] = [e for e in self.enemies if e.alive]
        self.projectiles[:] = [p for p in self.projectiles if p.alive]
        self.experiences[:] = [xp for xp in self.experiences if xp.alive]
        self.items[:] = [item for item in self.items if item.alive]
        self.floating_texts[:] = [text for text in self.floating_texts if text.alive]
        
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
            self.game_timer.update(dt)
            projectile = self.player.update(dt,self.enemies)
            if projectile:
                self.projectiles.append(projectile)
            
            self.spawner.update(dt)  
            
            for enemy in self.enemies:
                enemy.chase(self.player)
                enemy.update(dt)
                
            for projectile in self.projectiles:
                projectile.update(dt)
                
            for text in self.floating_texts:
                text.update(dt)
            
            # COLLISIONS      
            Combat.check_entity_collision(self.player,
                self.enemies,
                self.projectiles,
                self.experiences,
                self.items,
                self.floating_texts
                )
            
            # CLEAN-UP
            self.check_entity_alive()
            
            # DRAW
            self.screen.fill((30,30,30))

            PlayerUI.draw(self.screen, self.player)
            
            if self.player.alive:
                self.player.draw(self.screen)
            
            for enemy in self.enemies:
                enemy.draw(self.screen)

            for item in self.items:
                item.draw(self.screen)
                
            for projectile in self.projectiles:
                projectile.draw(self.screen)
                    
            for xp in self.experiences:
                xp.draw(self.screen)
                
            for text in self.floating_texts:
                text.draw(self.screen)
                            
            pygame.display.flip()
        
        pygame.quit()