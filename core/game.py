import pygame
import settings

from entities.player import Player
from systems.combat import Combat
from core.data_manager import ENEMY_DB, ITEMS_DB
from systems.spawner import Spawner
from systems.timer import Timer
from GUI.playerUI import PlayerUI   
from GUI.tools import Tools

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.reSpawn()

    def reSpawn(self):
        self.player = Player(400, 250, 5)
        self.enemies = []
        self.items = []
        self.projectiles = []
        self.experiences = []
        self.floating_texts = []
        self.state = "PLAYING"
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
    
    def draw_level_up_menu(self):
        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        Tools.draw_text(self.screen, "¡Nivel " + str(self.player.level) + "!", 48, (255, 215, 0), settings.WIDTH // 2 - 100, settings.HEIGHT // 2 - 150)
        
        card_width = 200
        card_height = 250
        card_spacing = 50
        init_x = (settings.WIDTH - (3 * card_width + 2 * card_spacing)) // 2
        init_y = settings.HEIGHT // 2 - card_height // 2

        self.carta_rects = []

        for i in range(3):
            x = init_x + i * (card_width + card_spacing)
            card_rect = pygame.Rect(x, init_y, card_width, card_height)
            self.carta_rects.append(card_rect)
            
            pygame.draw.rect(self.screen, (50, 50, 80), card_rect, border_radius=15)
            pygame.draw.rect(self.screen, (255, 255, 255), card_rect, 3, border_radius=15)
            Tools.draw_text(self.screen, f"Mejora {i + 1}", 24, (255, 255, 255), x + 20, init_y + 100)

    def run(self):
        running = True
        
        opciones_mejora = [
            {"nombre": "+ Daño", "tipo": "damage", "valor": 1},
            {"nombre": "+ Velocidad", "tipo": "speed", "valor": 30},
            {"nombre": "- Recarga", "tipo": "cooldown", "valor": 0.1}
        ]

        while running:
            dt = self.clock.tick(settings.FPS) / 1000

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reSpawn()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    if self.state == "LEVEL_UP":
                        if hasattr(self, 'carta_rects'): 
                            for i, rect in enumerate(self.carta_rects):
                                if rect.collidepoint(event.pos):
                                    mejora = opciones_mejora[i]
                                    if mejora["tipo"] == "damage":
                                        self.player.shoot_damage += mejora["valor"]
                                    elif mejora["tipo"] == "speed":
                                        self.player.speed += mejora["valor"]
                                    elif mejora["tipo"] == "cooldown":
                                        self.player.shoot_cooldown = max(0.2, self.player.shoot_cooldown - mejora["valor"])
                                    
                                    self.state = "PLAYING"

            # UPDATE
            if self.state == "PLAYING":
                self.game_timer.update(dt)
                
                projectile = self.player.update(dt, self.enemies)
                if projectile:
                    self.projectiles.append(projectile)
                
                self.spawner.update(dt, self.game_timer, self.player)  
                
                for enemy in self.enemies:
                    enemy.chase(self.player)
                    enemy.update(dt)
                    
                for projectile in self.projectiles:
                    projectile.update(dt)
                    
                for text in self.floating_texts:
                    text.update(dt)
                
                if self.player.leveled_up:
                    self.state = "LEVEL_UP"
                    self.player.leveled_up = False
            
                # COLLISIONS      
                Combat.check_entity_collision(
                    self.player,
                    self.enemies,
                    self.projectiles,
                    self.experiences,
                    self.items,
                    self.floating_texts
                )
                
                # CLEAN-UP
                self.check_entity_alive()
            
            # DRAW
            self.screen.fill((30, 30, 30))

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

            if self.state == "LEVEL_UP":
                self.draw_level_up_menu()

            pygame.display.flip()
        
        pygame.quit()