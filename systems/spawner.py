import random
from entities.enemy import Enemy
from entities.item import Item
from systems.randomCoord import GenerateCoords
from core.data_manager import ENEMY_DB
from core.data_manager import ITEMS_DB

class Spawner:
    def __init__(self, enemy_list, item_list): 
        self.enemy_list = enemy_list
        self.item_list = item_list
        
        self.enemy_types = list(ENEMY_DB.keys())
        self.item_types = list(ITEMS_DB.keys())
        
        self.enemy_power_map = {}
        for e_type, stats in ENEMY_DB.items():
            power = (stats["hp"] + stats["damage"]) / 2.0
            self.enemy_power_map[e_type] = power
            
        self.allowed_enemies = []
        
        #---Enemies Timer
        self.enemy_time = 0.0
        self.base_enemy_spawn_rate = 1.5
        self.current_enemy_spawn_rate = 1.5
        #---Items Timer
        self.item_time = 0.0
        self.item_spawn_rate = 15.0

    def update(self, dt, timer):
        self.enemy_time += dt
        self.item_time += dt
        
        segundos = timer.get_seconds()
        
        #---Dynamic Difficulty
        reduccion_velocidad = (segundos // 10) * 0.05
        self.current_enemy_spawn_rate = max(0.2, self.base_enemy_spawn_rate - reduccion_velocidad)
        
        limite_poder = 2.0 + (segundos / 15.0)
        
        self.allowed_enemies = [
            e_type for e_type, power in self.enemy_power_map.items() 
            if power <= limite_poder
        ]
        
        if not self.allowed_enemies:
            mas_debil = min(self.enemy_power_map, key=self.enemy_power_map.get)
            self.allowed_enemies.append(mas_debil)
            
        #---Inteliget Spawner
        
        if self.enemy_time >= self.current_enemy_spawn_rate:
            self.spawn_enemy()
            self.enemy_time = 0.0
            
        if self.item_time >= self.item_spawn_rate:
            self.spawn_item()
            self.item_time = 0.0

    def spawn_enemy(self):
        spawn_x, spawn_y = GenerateCoords()
        random_type = random.choice(self.allowed_enemies)
        enemy = Enemy(spawn_x, spawn_y, random_type) 
        self.enemy_list.append(enemy)
        
    def spawn_item(self):
        spawn_x, spawn_y = GenerateCoords()
        random_type = random.choice(self.item_types)
        item = Item(spawn_x, spawn_y, random_type) 
        self.item_list.append(item)