import pygame
import math
from GUI.tools import Tools

class PlayerUI:
    heart_surface = None
    star_surface = None

    @classmethod
    def get_heart_surface(cls):
        if cls.heart_surface is None:
            size = 20
            cls.heart_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            heart_color = (220, 20, 60)
            
            pygame.draw.circle(cls.heart_surface, heart_color, (6, 6), 6)
            pygame.draw.circle(cls.heart_surface, heart_color, (14, 6), 6)
            pygame.draw.polygon(cls.heart_surface, heart_color, [(1, 9), (19, 9), (10, 19)])

        return cls.heart_surface

    @classmethod
    def get_star_surface(cls):
        if cls.star_surface is None:
            size = 20
            cls.star_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            star_color = (255, 215, 0) # Gold
            
            # Procedural star generation
            points = []
            num_points = 5
            outer_rad = 10
            inner_rad = 4
            center = (10, 10)
            angle = -math.pi / 2 # Start pointing up

            for i in range(num_points * 2):
                radius = outer_rad if i % 2 == 0 else inner_rad
                x = center[0] + math.cos(angle) * radius
                y = center[1] + math.sin(angle) * radius
                points.append((x, y))
                angle += math.pi / num_points

            pygame.draw.polygon(cls.star_surface, star_color, points)

        return cls.star_surface

    @staticmethod
    def draw(screen, player):
        
        # --- LEVEL ---
        star_img = PlayerUI.get_star_surface()
        y_pos_level = 50
        
        if player.level <= 5:
            for i in range(player.level):
                screen.blit(star_img, (20 + i * 25, y_pos_level))
        else:
            screen.blit(star_img, (20, y_pos_level))
            Tools.draw_text(screen, f'x{player.level}', 22, (255, 255, 255), 50, y_pos_level)
        
        # --- XP ---
        Tools.draw_text(screen, f'XP: {player.xp} / {player.xp_necesaria}', 20, (255, 255, 255), 20, 80)

        # --- HEALTH ---
        heart_img = PlayerUI.get_heart_surface()
        y_pos_health = 15
        
        if player.live_points <= 5:
            for i in range(player.live_points):
                screen.blit(heart_img, (20 + i * 25, y_pos_health))
        else:
            screen.blit(heart_img, (20, y_pos_health))
            Tools.draw_text(screen, f'x{player.live_points}', 22, (255, 255, 255), 50, y_pos_health)