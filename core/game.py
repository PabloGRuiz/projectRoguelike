import pygame
import settings
import random

from entities.player import Player
from entities.boss import Boss
from GUI.levelCards import draw_level_up_menu
from GUI.timerUI import TimerUI
from GUI.menus import draw_main_menu, draw_game_over_menu 
from systems.combat import Combat
from core.data_manager import ENEMY_DB, ITEMS_DB, UPGRADES_DB
from systems.spawner import Spawner
from systems.timer import Timer
from GUI.playerUI import PlayerUI
from systems.audio_manager import AudioManager

class Game:
    def __init__(self):
        pygame.init()

        # --- WINDOW SETUP ---
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT), 
            pygame.RESIZABLE | pygame.WINDOWMAXIMIZED
        )
        settings.WIDTH, settings.HEIGHT = self.screen.get_size()

        # --- WINDOW ICON ---
        try:
            icon_img = pygame.image.load("assets/icon.png") 
            pygame.display.set_icon(icon_img)
        except FileNotFoundError:
            pass

        self.clock = pygame.time.Clock()
        self.audio = AudioManager()

        # --- UI INITIALIZATION ---
        self.current_upgrades = []
        self.timerUI = TimerUI((255,255,255))
        self.update_button_positions()
        self.state = "MAIN_MENU"

        self.reSpawn()

    def update_button_positions(self):
        # --- UI RECTANGLES ---
        self.btn_jugar = pygame.Rect(settings.WIDTH // 2 - 100, settings.HEIGHT // 2 - 50, 200, 60)
        self.btn_reintentar = pygame.Rect(settings.WIDTH // 2 - 120, settings.HEIGHT // 2 - 50, 240, 60)
        self.btn_salir = pygame.Rect(settings.WIDTH // 2 - 100, settings.HEIGHT // 2 + 50, 200, 60)

    def reSpawn(self):
        # --- GAME RESET ---
        self.audio.play_music("assets/music/Pixel_Wings_Stage1_Theme.ogg", loop=True, volume=0.5)
        self.timerUI.color = (255,255,255)
        self.player = Player(settings.WIDTH // 2, settings.HEIGHT // 2, 5, self.audio)
        self.enemies = []
        self.items = []
        self.projectiles = []
        self.enemy_projectiles = []
        self.experiences = []
        self.floating_texts = []
        self.state = "PLAYING"
        self.spawner = Spawner(self.enemies, self.items)
        self.game_timer = Timer()
        
        # --- BOSS TRACKERS ---
        self.boss_spawned = False
        self.boss_defeated = False

    def check_entity_alive(self):
        # --- GARBAGE COLLECTION ---
        self.enemies[:] = [e for e in self.enemies if e.alive]
        self.projectiles[:] = [p for p in self.projectiles if p.alive]
        self.enemy_projectiles[:] = [ep for ep in self.enemy_projectiles if ep.alive]
        self.experiences[:] = [xp for xp in self.experiences if xp.alive]
        self.items[:] = [item for item in self.items if item.alive]
        self.floating_texts[:] = [text for text in self.floating_texts if text.alive]
        self.player.can_shoot = self.player.alive

    def generate_upgrade_options(self):
        # --- UPGRADE POOL ---
        available_upgrades = []
        for upgrade in UPGRADES_DB.values():
            stats = upgrade["upgrade"]
            if "projectile_type_equipped" in stats:
                if stats["projectile_type_equipped"] == self.player.projectile_type_equipped:
                    continue
            available_upgrades.append(upgrade)
            
        self.current_upgrades = random.sample(
            available_upgrades,
            min(3, len(available_upgrades))
        )

    def run(self):
        # --- MAIN LOOP ---
        running = True
        while running:
            dt = self.clock.tick(settings.FPS) / 1000

            running = self.handle_events()
            if self.state == "PLAYING":
                self.update_game(dt)
            self.draw_game_state()

        pygame.quit()

    def handle_events(self):
        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.VIDEORESIZE:
                settings.WIDTH = event.w
                settings.HEIGHT = event.h
                self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE | pygame.WINDOWMAXIMIZED)
                self.update_button_positions() 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reSpawn()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                # --- MAIN MENU CLICKS ---
                if self.state == "MAIN_MENU":
                    if self.btn_jugar.collidepoint(event.pos):
                        self.reSpawn() 
                    elif self.btn_salir.collidepoint(event.pos):
                        return False
                        
                # --- LEVEL UP CLICKS ---
                elif self.state == "LEVEL_UP":
                    for i, rect in enumerate(self.carta_rects):
                        if rect.collidepoint(event.pos):
                            selected_upgrade = self.current_upgrades[i]
                            self.player.apply_upgrade(selected_upgrade)
                            self.state = "PLAYING"
                            
                # --- GAME OVER CLICKS ---
                elif self.state == "GAME_OVER":
                    if self.btn_reintentar.collidepoint(event.pos):
                        self.reSpawn()
                    elif self.btn_salir.collidepoint(event.pos):
                        return False
        return True

    def update_game(self, dt):
        # --- GAME LOGIC ---
        self.game_timer.update(dt)

        new_projectiles = self.player.update(dt, self.enemies)
        if new_projectiles:
            if isinstance(new_projectiles, list):
                self.projectiles.extend(new_projectiles)
            else:
                self.projectiles.append(new_projectiles)

        self.spawner.update(dt, self.game_timer, self.player, self.timerUI)

        for enemy in self.enemies:
            enemy.chase(self.player)
            boss_projs = enemy.update(dt)
            if boss_projs:
                self.enemy_projectiles.extend(boss_projs)

        for projectile in self.projectiles:
            projectile.update(dt)
            
        for ep in self.enemy_projectiles:
            ep.update(dt)

        for text in self.floating_texts:
            text.update(dt)

        if self.player.leveled_up:
            self.generate_upgrade_options()
            self.state = "LEVEL_UP"
            self.player.leveled_up = False
            
        for xp in self.experiences:
            xp.update(dt)

        Combat.check_entity_collision(
            self.player, self.enemies, self.projectiles, self.enemy_projectiles,
            self.experiences, self.items, self.floating_texts
        )

        self.check_entity_alive()
        
        if not self.player.alive:
            self.state = "GAME_OVER"

        # --- DYNAMIC MUSIC & BOSS TRACKING ---
        boss_alive = any(isinstance(enemy, Boss) for enemy in self.enemies)
        
        if boss_alive:
            self.boss_spawned = True
        elif self.boss_spawned and not boss_alive:
            self.boss_defeated = True

        if boss_alive and self.state == "PLAYING":
            self.audio.play_music("assets/music/Crimson_Barrage_Boss1.ogg", loop=True, volume=settings.MUSIC_VOLUME)
        elif self.boss_defeated and self.state == "PLAYING":
            self.timerUI.color = (255,255,255)
            self.audio.play_music("assets/music/Pixel_Bloom_Stage2_Theme.ogg", loop=True, volume=settings.MUSIC_VOLUME)
        elif self.state == "PLAYING":
            self.audio.play_music("assets/music/Pixel_Wings_Stage1_Theme.ogg", loop=True, volume=settings.MUSIC_VOLUME)

    def draw_game_state(self):
        # --- RENDER ---
        self.screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos() 

        if self.state == "MAIN_MENU":
            draw_main_menu(self.screen, self.btn_jugar, self.btn_salir, mouse_pos)

        elif self.state in ["PLAYING", "LEVEL_UP", "GAME_OVER"]:
            self.draw_entities()

            if self.state == "LEVEL_UP":
                self.carta_rects = draw_level_up_menu(self.screen, self.player, self.current_upgrades)
            elif self.state == "GAME_OVER":
                draw_game_over_menu(self.screen, self.btn_reintentar, self.btn_salir, mouse_pos)

        pygame.display.flip()

    def draw_entities(self):
        # --- RENDER ENTITIES ---
        PlayerUI.draw(self.screen, self.player)
        self.timerUI.draw_timer(self.screen, self.game_timer.current_second)

        if self.player.alive:
            self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for item in self.items:
            item.draw(self.screen)

        for projectile in self.projectiles:
            projectile.draw(self.screen)
            
        for ep in self.enemy_projectiles:
            ep.draw(self.screen)

        for xp in self.experiences:
            xp.draw(self.screen)

        for text in self.floating_texts:
            text.draw(self.screen)