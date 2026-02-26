import random
from entities.enemy import Enemy
from systems.randomCoord import GenerateCoords
from core.data_manager import ENEMY_DB

class Spawner:
    def __init__(self, enemy_list):
        self.enemy_list = enemy_list
        self.enemy_types = list(ENEMY_DB.keys())
        self.current_time = 0
        self.spawn_rate = 1.5

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.spawn_rate:
            self.spawn_enemy()
            self.current_time = 0

    def spawn_enemy(self):
        spawn_x, spawn_y = GenerateCoords()
        random_type = random.choice(self.enemy_types)
        enemy = Enemy(spawn_x, spawn_y, random_type) 
        self.enemy_list.append(enemy)