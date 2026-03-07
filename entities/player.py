import pygame
import math
import settings
from entities.entity import Entity
from entities.projectile import Projectile 

class Player(Entity):
    def __init__(self, x, y, lp, audio_manager):
        super().__init__(x, y, 30, (40, 180, 40))
        
        self.live_points = lp
        self.audio = audio_manager
        
        self.can_shoot = False
        self.shoot_timer = 0
        self.shoot_cooldown = 1.2
        self.shoot_damage = 1
        self.shoot_backwards = False
        self.multi_shoot = 1
        self.side_shots = False
        self.extra_projectiles = 0
        self.amount_projectile = 1
        self.projectile_type_equipped = "basic"
        
        # --- SISTEMA DE RÁFAGA ---
        self.burst_queue = 0      
        self.burst_timer = 0      
        self.burst_delay = 0.1   
        
        self.speed = 250
        self.xp = 0 
        self.level = 1
        self.xp_necesaria = 3
        self.leveled_up = False
        
    def handle_input(self):
        if self.alive:
            keys = pygame.key.get_pressed()
            self.velocity.x = 0
            self.velocity.y = 0
            
            if keys[pygame.K_a]:
                self.velocity.x = -self.speed
            if keys[pygame.K_d]:
                self.velocity.x = self.speed
            if keys[pygame.K_w]:
                self.velocity.y = -self.speed
            if keys[pygame.K_s]:
                self.velocity.y = self.speed
                    
    def update(self, dt, targets):
        self.limit()
        self.handle_input()
        
        projectiles = []
        self.shoot_timer += dt
        
        if self.shoot_timer >= self.shoot_cooldown and self.can_shoot:
            self.shoot_timer = 0
            self.burst_queue = self.multi_shoot 
            self.burst_timer = self.burst_delay 

        if self.burst_queue > 0:
            self.burst_timer += dt
            if self.burst_timer >= self.burst_delay:
                self.burst_timer = 0
                batch = self.create_projectiles(targets)
                projectiles.extend(batch)
                self.burst_queue -= 1
        
        super().update(dt)
        return projectiles
    
    def create_projectiles(self, targets):
        if not targets:
            return []

        closest = min(
            targets,
            key=lambda enemy: (enemy.pos - self.pos).length()
        )

        base_direction = closest.pos - self.pos
        if base_direction.length() == 0:
            return []

        base_direction = base_direction.normalize()
        spread_angle = 30
        total = self.amount_projectile

        directions = []
        for i in range(total):
            if total > 1:
                angle_offset = spread_angle * (i - (total - 1) / 2)
                rotated = base_direction.rotate(angle_offset)
                directions.append(rotated)
            else:
                directions.append(base_direction)

        if self.shoot_backwards:
            directions.append(-base_direction)

        if self.side_shots:
            directions.append(base_direction.rotate(90))
            directions.append(base_direction.rotate(-90))

        for _ in range(self.extra_projectiles):
            directions.append(base_direction)

        spawned = []
        for direction in directions:
            projectile = Projectile(
                self.pos.x,
                self.pos.y,
                direction,
                self.projectile_type_equipped
            )
            spawned.append(projectile)

        if spawned:
            self.audio.play_sound("assets/sfx/shoot.wav", volume=0.3)

        return spawned

    def level_up(self, xp):
        self.xp += xp
        if self.xp >= self.xp_necesaria:
            self.xp -= self.xp_necesaria
            self.level += 1
            self.xp_necesaria = int(self.xp_necesaria * 1.5) 
            self.leveled_up = True

    def apply_upgrade(self, upgrade_data):
        for attr, value in upgrade_data["upgrade"].items():
            if hasattr(self, attr):
                current_value = getattr(self, attr)
                if isinstance(value, str):
                    new_value = value
                else:
                    new_value = current_value + value
                    if attr == "shoot_cooldown":
                        new_value = max(0.2, new_value)
                setattr(self, attr, new_value)

    def limit(self):
        self.pos.x = max(0, min(self.pos.x, settings.WIDTH))
        self.pos.y = max(0, min(self.pos.y, settings.HEIGHT))