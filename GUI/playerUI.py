import pygame
from GUI.tools import Tools

class PlayerUI:
    heart_surface = None

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

    @staticmethod
    def draw(screen, player):
        
        # --- LEVEL SQUARES ---
        for i in range(player.level):
            pygame.draw.rect(
                screen,
                (39, 49, 245),
                (20 + i * 20, 50, 15, 15)
            )
        
        # --- XP TEXT ---
        Tools.draw_text(screen, f'XP: {player.xp}', 20, (255, 255, 255), 20, 80)

        # --- HEALTH HEARTS ---
        heart_img = PlayerUI.get_heart_surface()
        
        for i in range(player.live_points):
            screen.blit(heart_img, (20 + i * 25, 15))