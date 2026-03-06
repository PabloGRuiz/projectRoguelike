import pygame
import settings
from GUI.tools import Tools

class TimerUI:
    def __init__(self, color):
        self.color = color
    def draw_timer(self, screen, timer):
        Tools.draw_text(screen, f'{timer} s.', 20, (self.color), settings.WIDTH // 2, 20)