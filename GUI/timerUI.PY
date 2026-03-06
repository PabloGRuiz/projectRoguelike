import pygame
import settings
from GUI.tools import Tools

class TimerUI:
    def draw_timer(screen,timer):
        Tools.draw_text(screen, f'{timer} s.', 20, (255,255,255), settings.WIDTH // 2, 20)