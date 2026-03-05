import pygame
import math
import random # Required for the erratic behavior
import settings
from entities.enemy import Enemy
from entities.enemy_projectile import EnemyProjectile
from core.data_manager import ENEMY_DB


class Boss(Enemy):
    def __init__(self, x, y, enemy_type="boss_ojo_maldito"):
        super().__init__(x, y, enemy_type)

        stats = ENEMY_DB.get(enemy_type, {})

        self.move_pattern = stats.get("move_pattern", "center")
        
        # Store the base cooldown so we can scale it down in later phases
        self.base_attack_cooldown = stats.get("attack_cooldown", 2.5)
        self.attack_cooldown = self.base_attack_cooldown

        self.shoot_timer = 0.0
        self.target_pos = pygame.Vector2(settings.WIDTH // 2, settings.HEIGHT // 2)

        # Phase system
        self.phase = 1
        self.max_hp = self.live_points 
        self.shoot_pattern = stats.get("shoot_pattern", "ring")

        # Used for rotating patterns
        self.pattern_rotation = 0
        self.current_target = None 

    # -------------------------
    # Movement Logic
    # -------------------------
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
            
        # NEW: Phase 3 movement pattern
        elif self.move_pattern == "chase_player":
            if self.current_target:
                direction = self.current_target.pos - self.pos
                if direction.length() > 0:
                    # We multiply by 0.7 so the boss is slightly slower than a normal enemy, 
                    # giving the player a chance to dodge while shooting
                    self.velocity = direction.normalize() * (self.speed * 0.7)

    # -------------------------
    # Main Update & Phase Control
    # -------------------------
    def update(self, dt): 
        super().update(dt)

        self.shoot_timer += dt
        new_projectiles = []

        # Calculate remaining life percentage (0.0 to 1.0)
        life_ratio = self.live_points / self.max_hp

        # --- PHASE TRANSITIONS ---
        # Phase 2: 59% to 30% HP
        if life_ratio <= 0.60 and self.phase == 1:
            self.phase = 2
            # Shoot much faster (e.g., from 2.5s to 0.75s)
            self.attack_cooldown = self.base_attack_cooldown * 0.3 
            print("BOSS PHASE 2: Erratic Attack!") 

        # Phase 3: 29% to 0% HP
        if life_ratio <= 0.30 and self.phase == 2:
            self.phase = 3
            # Shoot even faster and start chasing the player
            self.attack_cooldown = self.base_attack_cooldown * 0.2
            self.move_pattern = "chase_player" 
            print("BOSS PHASE 3: Chasing Player!") 

        # --- ATTACK LOGIC ---
        if self.shoot_timer >= self.attack_cooldown:
            self.shoot_timer = 0.0

            # Here we check the JSON pattern. This allows you to add different 
            # phase logic for different bosses in the future (like "spiral" or "burst")
            if self.shoot_pattern == "ring":
                if self.phase == 1:
                    new_projectiles = self.fire_simple_ring()
                elif self.phase == 2:
                    new_projectiles = self.fire_erratic_ring()
                elif self.phase == 3:
                    new_projectiles = self.fire_erratic_ring()

        return new_projectiles

    # -------------------------
    # Attack Patterns
    # -------------------------

    # Phase 1: Clean, predictable radial burst
    def fire_simple_ring(self):
        projectiles = []
        bullet_amount = 12

        # Fixed rotation so the player can learn the safe spots
        self.pattern_rotation += 15

        for i in range(bullet_amount):
            angle = math.radians(i * (360 / bullet_amount) + self.pattern_rotation)
            dir_x = math.cos(angle)
            dir_y = math.sin(angle)

            bullet = EnemyProjectile(self.pos.x, self.pos.y, dir_x, dir_y, self.damage)
            projectiles.append(bullet)

        return projectiles

    # Phases 2 & 3: Chaotic, unpredictable radial burst
    def fire_erratic_ring(self):
        projectiles = []
        bullet_amount = 10 # Slightly fewer bullets, but shot way more often
        
        # Erratic Rotation: Jumps randomly forward or backward by a large angle
        random_jump = random.uniform(20, 70) * random.choice([-1, 1])
        self.pattern_rotation += random_jump

        for i in range(bullet_amount):
            angle = math.radians(i * (360 / bullet_amount) + self.pattern_rotation)
            dir_x = math.cos(angle)
            dir_y = math.sin(angle)

            # Optional: We can randomize bullet speed slightly for a true "hell" effect
            random_speed = random.uniform(250, 400)

            bullet = EnemyProjectile(
                self.pos.x, 
                self.pos.y, 
                dir_x, 
                dir_y, 
                self.damage,
                speed=random_speed # Assumes your EnemyProjectile accepts a speed parameter
            )
            projectiles.append(bullet)

        return projectiles