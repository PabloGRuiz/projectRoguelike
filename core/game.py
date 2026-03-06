import pygame
import settings
import random

from entities.player import Player
from GUI.levelCards import draw_level_up_menu
from GUI.timerUI import TimerUI
from systems.combat import Combat
from core.data_manager import ENEMY_DB, ITEMS_DB, UPGRADES_DB
from systems.spawner import Spawner
from systems.timer import Timer
from GUI.playerUI import PlayerUI
from systems.audio_manager import AudioManager  

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.audio = AudioManager() 
        self.reSpawn()
        self.current_upgrades = []

    def reSpawn(self):
        self.player = Player(settings.WIDTH // 2, settings.HEIGHT // 2, 5)
        self.audio.play_music("assets/music/Pixel_Wings_Stage1_Theme.ogg", loop=True, volume=0.5)
        self.enemies = []
        self.items = []
        self.projectiles = []
        self.enemy_projectiles = [] # RESTORED: Boss bullets list
        self.experiences = []
        self.floating_texts = []
        self.state = "PLAYING"
        self.spawner = Spawner(self.enemies, self.items)
        self.game_timer = Timer()

    def check_entity_alive(self):
        self.enemies[:] = [e for e in self.enemies if e.alive]
        self.projectiles[:] = [p for p in self.projectiles if p.alive]
        self.enemy_projectiles[:] = [ep for ep in self.enemy_projectiles if ep.alive] # RESTORED
        self.experiences[:] = [xp for xp in self.experiences if xp.alive]
        self.items[:] = [item for item in self.items if item.alive]
        self.floating_texts[:] = [text for text in self.floating_texts if text.alive]

        self.player.can_shoot = self.player.alive

    def generate_upgrade_options(self):
        all_upgrades = list(UPGRADES_DB.values())
        self.current_upgrades = random.sample(
            all_upgrades,
            min(3, len(all_upgrades))
        )

    def run(self):
        running = True

        while running:
            dt = self.clock.tick(settings.FPS) / 1000

            # --- EVENTS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reSpawn()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "LEVEL_UP":
                        for i, rect in enumerate(self.carta_rects):
                            if rect.collidepoint(event.pos):
                                selected_upgrade = self.current_upgrades[i]
                                self.player.apply_upgrade(selected_upgrade)
                                self.state = "PLAYING"

            # --- UPDATE ---
            if self.state == "PLAYING":

                self.game_timer.update(dt)

                # Player update
                new_projectiles = self.player.update(dt, self.enemies)

                if new_projectiles:
                    if isinstance(new_projectiles, list):
                        self.projectiles.extend(new_projectiles)
                    else:
                        self.projectiles.append(new_projectiles)

                # Spawner
                self.spawner.update(dt, self.game_timer, self.player)

                # Enemies
                for enemy in self.enemies:
                    enemy.chase(self.player)
                    boss_projs = enemy.update(dt)
                    if boss_projs:
                        self.enemy_projectiles.extend(boss_projs)

                # Player Projectiles
                for projectile in self.projectiles:
                    projectile.update(dt)
                    
                # RESTORED: Enemy Projectiles
                for ep in self.enemy_projectiles:
                    ep.update(dt)

                # Floating texts
                for text in self.floating_texts:
                    text.update(dt)

                # Level up trigger
                if self.player.leveled_up:
                    self.generate_upgrade_options()
                    self.state = "LEVEL_UP"
                    self.player.leveled_up = False

                # --- COLLISIONS ---
                Combat.check_entity_collision(
                    self.player,
                    self.enemies,
                    self.projectiles,
                    self.enemy_projectiles,
                    self.experiences,
                    self.items,
                    self.floating_texts
                )

                # --- CLEAN-UP ---
                self.check_entity_alive()

            # --- DRAW ---
            self.screen.fill((30, 30, 30))

            PlayerUI.draw(self.screen, self.player)
            TimerUI.draw_timer(self.screen, self.game_timer.current_second)

            if self.player.alive:
                self.player.draw(self.screen)

            for enemy in self.enemies:
                enemy.draw(self.screen)

            for item in self.items:
                item.draw(self.screen)

            for projectile in self.projectiles:
                projectile.draw(self.screen)
                
            # RESTORED: Draw boss bullets
            for ep in self.enemy_projectiles:
                ep.draw(self.screen)

            for xp in self.experiences:
                xp.draw(self.screen)

            for text in self.floating_texts:
                text.draw(self.screen)

            if self.state == "LEVEL_UP":
                self.carta_rects = draw_level_up_menu(
                    self.screen,
                    self.player,
                    self.current_upgrades
                )

            pygame.display.flip()

        pygame.quit()