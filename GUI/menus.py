import pygame
import settings
from GUI.tools import Tools

def draw_button(screen, rect, text, default_color, hover_color, mouse_pos):
    is_hovered = rect.collidepoint(mouse_pos)
    current_color = hover_color if is_hovered else default_color

    shadow_rect = rect.copy()
    shadow_rect.y += 4
    pygame.draw.rect(screen, (20, 20, 20), shadow_rect, border_radius=10)

    pygame.draw.rect(screen, current_color, rect, border_radius=10)

    font = pygame.font.SysFont("Arial", 32, bold=True)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_main_menu(screen, btn_jugar, btn_salir, mouse_pos):
    Tools.draw_text(screen, "DARK PATH", 72, (200, 50, 50), settings.WIDTH // 2 - 180, settings.HEIGHT // 4)
    
    draw_button(screen, btn_jugar, "JUGAR", (50, 160, 50), (70, 200, 70), mouse_pos)
    draw_button(screen, btn_salir, "SALIR", (180, 50, 50), (220, 70, 70), mouse_pos)

def draw_game_over_menu(screen, btn_reintentar, btn_salir, mouse_pos):
    overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((50, 0, 0)) 
    screen.blit(overlay, (0, 0))
    
    Tools.draw_text(screen, "HAS MUERTO", 72, (255, 50, 50), settings.WIDTH // 2 - 200, settings.HEIGHT // 4)
    
    draw_button(screen, btn_reintentar, "REINTENTAR", (50, 120, 180), (70, 150, 220), mouse_pos)
    draw_button(screen, btn_salir, "SALIR", (180, 50, 50), (220, 70, 70), mouse_pos)