import pygame

from entities.entity import Entity

from core.data_manager import ITEMS_DB

class Item(Entity):
    def __init__(self, x, y, items_type="heal"):
        stats = ITEMS_DB.get(items_type, ITEMS_DB["heal"])
        size = stats["size"]
        color = tuple(stats["color"])
        super().__init__(x, y, size, color)
        self.type = items_type
        self.name = stats["name"]
        self.amount = stats["amount"]
    
    def draw(self,screen):
        top = (self.pos.x, self.pos.y - self.size)
        left = (self.pos.x - self.size, self.pos.y + self.size)
        right = (self.pos.x + self.size, self.pos.y + self.size)
        pygame.draw.polygon(
            screen,
            self.color,
            [top, left, right]
        )
    