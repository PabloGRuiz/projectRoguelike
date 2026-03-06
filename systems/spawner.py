import random
from entities.enemy import Enemy
from entities.item import Item
from entities.boss import Boss
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
        
        # --- TIMERS ---
        self.enemy_time = 0.0
        self.base_enemy_spawn_rate = 1.5
        self.current_enemy_spawn_rate = 1.5

        self.item_time = 0.0
        self.item_spawn_rate = 15.0
        
        self.boss_spawned = False

    def update(self, dt, timer, player, timerUI):
        seconds = timer.get_seconds()
        boss_alive = any(isinstance(e, Boss) for e in self.enemy_list)

        if seconds >= 240 and not self.boss_spawned:
            timerUI.color = (250,50,50)
            self.spawn_boss(player)
            self.boss_spawned = True
            boss_alive = True

        self.item_time += dt
        if self.item_time >= self.item_spawn_rate:
            self.spawn_item(player)
            self.item_time = 0.0

        if boss_alive:
            return 
            
        # --- DYNAMIC DIFFICULTY ---
        self.enemy_time += dt
        speed_reduction = (seconds // 10) * 0.05
        self.current_enemy_spawn_rate = max(0.2, self.base_enemy_spawn_rate - speed_reduction)
        
        power_limit = 2.0 + (seconds / 15.0)
        
        self.allowed_enemies = [
            e_type for e_type, power in self.enemy_power_map.items() 
            if power <= power_limit
        ]
        
        if not self.allowed_enemies:
            weakest = min(self.enemy_power_map, key=self.enemy_power_map.get)
            self.allowed_enemies.append(weakest)
            
        if self.enemy_time >= self.current_enemy_spawn_rate:
            self.spawn_enemy(player)
            self.enemy_time = 0.0

    def spawn_enemy(self, player):
        spawn_x, spawn_y = GenerateCoords(player)
        random_type = random.choice(self.allowed_enemies)
        enemy = Enemy(spawn_x, spawn_y, random_type) 
        self.enemy_list.append(enemy)
        
    def spawn_item(self, player):
        spawn_x, spawn_y = GenerateCoords(player, 100)
        random_type = random.choice(self.item_types)
        item = Item(spawn_x, spawn_y, random_type) 
        self.item_list.append(item)

    def spawn_boss(self, player):
        spawn_x, spawn_y = GenerateCoords(player, 800)
        boss = Boss(spawn_x, spawn_y, "boss_ojo_maldito")
        self.enemy_list.append(boss)
        print(f"WARNING: BOSS SPAWNED WITH {boss.live_points} HP!")