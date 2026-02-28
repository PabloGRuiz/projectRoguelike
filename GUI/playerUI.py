import pygame

from GUI.tools import Tools

class PlayerUI:

    def draw( screen, player):

        for i in range(player.level):
            pygame.draw.rect(
                screen,
                (39, 49, 245),
                (20 + i * 20, 50, 15, 15)
            )
        
        Tools.draw_text(screen, f'XP: {player.xp}', 20, (255,255,255), 20, 80)

        for i in range(player.live_points):
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (20 + i * 20, 20),
                10
            )
            