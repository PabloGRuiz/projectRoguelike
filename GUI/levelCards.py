import pygame
from GUI.tools import Tools
import settings


def draw_level_up_menu(screen, player, upgrades):
    overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    Tools.draw_text(
        screen,
        f"¡Nivel {player.level}!",
        48,
        (255, 215, 0),
        settings.WIDTH // 2 - 100,
        settings.HEIGHT // 2 - 150
    )

    card_width = 200
    card_height = 250
    card_spacing = 50

    init_x = (settings.WIDTH - (3 * card_width + 2 * card_spacing)) // 2
    init_y = settings.HEIGHT // 2 - card_height // 2

    carta_rects = []

    for index, upgrade in enumerate(upgrades):
        x = init_x + index * (card_width + card_spacing)

        card_rect = pygame.Rect(x, init_y, card_width, card_height)
        carta_rects.append(card_rect)

        pygame.draw.rect(screen, (50, 50, 80), card_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), card_rect, 3, border_radius=15)

        Tools.draw_text(
            screen,
            upgrade["name"],
            24,
            (255, 255, 255),
            x + 20,
            init_y + 100
        )

    return carta_rects