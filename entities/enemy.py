import pygame
from entities.entity import Entity
from core.data_manager import ENEMY_DB
class Enemy(Entity):
    def __init__(self, x, y, enemy_type="default"):
        stats = ENEMY_DB.get(enemy_type, ENEMY_DB["default"])
        size = stats["size"]
        color = tuple(stats["color"])
        super().__init__(x, y, size, color)
        self.total_hp = stats["hp"]
        self.live_points = stats["hp"]
        self.damage = stats["damage"]
        self.speed = stats["speed"]
    def chase(self,target):
        direction = target.pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
            self.velocity = direction * self.speed