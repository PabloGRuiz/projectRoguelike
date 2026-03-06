import pygame
import settings
from GUI.tools import Tools

class TimerUI:
    def __init__(self, color):
        self.color = color
    def draw_timer(self, screen, timer_seconds):

        minutes = timer_seconds // 60
        seconds = timer_seconds % 60

        time_text = f"{minutes}:{seconds:02d}"

        Tools.draw_text(
            screen,
            time_text,
            20,
            self.color,
            settings.WIDTH // 2 -5,
            20
        )