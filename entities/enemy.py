import pygame
from entities.entity import Entity
import settings
class Enemy(Entity):
    def __init__(self, x, y, lp, dmg):
        super().__init__(x, y, 25, (200,50,50))
        self.live_points = lp
        self.damage = dmg
    def chase(self,target):
        direction = target.pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
            self.velocity = direction * settings.ENEMY_SPEED