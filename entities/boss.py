import pygame
import math
import random
import settings
from entities.enemy import Enemy
from entities.enemy_projectile import EnemyProjectile
from core.data_manager import ENEMY_DB

class Boss(Enemy):
    def __init__(self, x, y, enemy_type="boss_ojo_maldito"):
        super().__init__(x, y, enemy_type)

        stats = ENEMY_DB.get(enemy_type, {})

        self.move_pattern = stats.get("move_pattern", "center")
        self.base_attack_cooldown = stats.get("attack_cooldown", 2.5)
        self.attack_cooldown = self.base_attack_cooldown

        self.shoot_timer = 0.0
        self.target_pos = pygame.Vector2(settings.WIDTH // 2, settings.HEIGHT // 2)

        # --- STATES ---
        self.phase = 1
        self.max_hp = self.live_points 
        self.shoot_pattern = stats.get("shoot_pattern", "ring")

        # --- PATTERN VARIABLES ---
        self.pattern_rotation = 0
        self.spiral_angle_1 = 0
        self.spiral_angle_2 = 180
        self.current_target = None 

    # --- MOVEMENT ---
    def chase(self, target):
        self.current_target = target 
        
        if self.move_pattern == "center":
            direction = self.target_pos - self.pos
            if direction.length() > 5:
                self.velocity = direction.normalize() * self.speed
            else:
                self.velocity = pygame.Vector2(0, 0)

        elif self.move_pattern == "static":
            self.velocity = pygame.Vector2(0, 0)
            
        elif self.move_pattern == "chase_player":
            if self.current_target:
                direction = self.current_target.pos - self.pos
                if direction.length() > 0:
                    self.velocity = direction.normalize() * (self.speed * 0.7)

    # --- UPDATE ---
    def update(self, dt): 
        super().update(dt)

        self.shoot_timer += dt
        new_projectiles = []
        life_ratio = self.live_points / self.max_hp

        # --- PHASE CONTROL ---
        if life_ratio <= 0.60 and self.phase == 1:
            self.phase = 2
            self.attack_cooldown = 0.1 

        if life_ratio <= 0.30 and self.phase == 2:
            self.phase = 3
            self.attack_cooldown = 1.2 
            self.move_pattern = "chase_player" 

        # --- COMBAT ---
        if self.shoot_timer >= self.attack_cooldown:
            self.shoot_timer = 0.0

            if self.shoot_pattern == "ring":
                if self.phase == 1:
                    new_projectiles = self.fire_pulsing_flower()
                elif self.phase == 2:
                    new_projectiles = self.fire_double_spiral()
                elif self.phase == 3:
                    new_projectiles = self.fire_shotgun_chase()

        return new_projectiles

    # --- PATTERNS ---
    def fire_pulsing_flower(self):
        projectiles = []
        bullet_amount = 12
        self.pattern_rotation += 15
        speeds = [150, 250, 350] 

        for speed in speeds:
            for i in range(bullet_amount):
                angle = math.radians(i * (360 / bullet_amount) + self.pattern_rotation)
                dir_x = math.cos(angle)
                dir_y = math.sin(angle)

                bullet = EnemyProjectile(self.pos.x, self.pos.y, dir_x, dir_y, self.damage, speed=speed)
                projectiles.append(bullet)

        return projectiles

    def fire_double_spiral(self):
        projectiles = []
        self.spiral_angle_1 += 18 
        self.spiral_angle_2 -= 18 

        for angle_deg in [self.spiral_angle_1, self.spiral_angle_2]:
            angle = math.radians(angle_deg)
            dir_x = math.cos(angle)
            dir_y = math.sin(angle)

            bullet = EnemyProjectile(self.pos.x, self.pos.y, dir_x, dir_y, self.damage, speed=280)
            projectiles.append(bullet)

        return projectiles

    def fire_shotgun_chase(self):
        projectiles = []
        
        if not self.current_target:
            return projectiles

        direction = self.current_target.pos - self.pos
        if direction.length() == 0:
            return projectiles

        base_dir = direction.normalize()
        
        bullet_amount = 5
        spread = 15

        for i in range(bullet_amount):
            angle_offset = spread * (i - (bullet_amount - 1) / 2)
            rotated = base_dir.rotate(angle_offset)
            
            bullet = EnemyProjectile(self.pos.x, self.pos.y, rotated.x, rotated.y, self.damage, speed=400)
            projectiles.append(bullet)

        ring_amount = 8
        for i in range(ring_amount):
            angle = math.radians(i * (360 / ring_amount) + self.pattern_rotation)
            dir_x = math.cos(angle)
            dir_y = math.sin(angle)
            
            bullet = EnemyProjectile(self.pos.x, self.pos.y, dir_x, dir_y, self.damage, speed=100)
            projectiles.append(bullet)
            
        self.pattern_rotation += 20

        return projectiles