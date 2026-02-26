import pygame

from entities.entity import Entity

from core.data_manager import ITEMS_DB

class Items(Entity):
    def __init__(self, x, y, items_type="heal"):
        stats = ITEMS_DB.get(items_type, ITEMS_DB["heal"])
        size = stats["size"]
        color = tuple(stats["color"])
        super().__init__(x, y, size, color)
        self.type = items_type
        self.name = stats["name"]
        self.amount = stats["amount"]
    
    def draw(self,screen):
        pygame.draw.circle(
            screen,
            self.color,
            self.pos,
            self.size
        )
    