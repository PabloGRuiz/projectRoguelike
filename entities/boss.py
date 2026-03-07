import pygame
import math
import settings
from entities.enemy import Enemy
from entities.enemy_projectile import EnemyProjectile
from core.data_manager import ENEMY_DB

class Boss(Enemy):

    def __init__(self, x, y, enemy_type="boss_cursed_eye"):
        super().__init__(x, y, enemy_type)

        stats = ENEMY_DB.get(enemy_type, {})

        self.move_pattern = stats.get("move_pattern", "center")
        self.base_attack_cooldown = stats.get("attack_cooldown", 2.5)
        self.attack_cooldown = self.base_attack_cooldown

        self.shoot_timer = 0.0
        self.target_pos = pygame.Vector2(settings.WIDTH // 2, settings.HEIGHT // 2)

        self.phase = 1
        self.max_hp = self.live_points

        self.pattern_rotation = 0
        self.spiral_angle = 0

        self.current_target = None
        
        self.orbit_angle = 0
        self.orbit_radius = 200

        self.phase_thresholds = [0.60, 0.30]

        if enemy_type == "boss_cursed_eye":

            self.patterns = {
                1: self.eye_ring,
                2: self.eye_double_spiral,
                3: self.eye_shotgun_ring
            }

        elif enemy_type == "boss_golem":

                self.patterns = {
                    1: self.golem_ring,
                    2: self.golem_wall,
                    3: self.golem_wall_ring
                }

    # --- MOVEMENT ---

    def chase(self, target, dt):

        self.current_target = target

        if self.move_pattern == "orbit_player":

            self.orbit_angle += 60 * dt

            orbit_x = target.pos.x + math.cos(math.radians(self.orbit_angle)) * self.orbit_radius
            orbit_y = target.pos.y + math.sin(math.radians(self.orbit_angle)) * self.orbit_radius

            desired = pygame.Vector2(orbit_x, orbit_y)
            direction = desired - self.pos

            if direction.length() > 5:
                self.velocity = direction.normalize() * self.speed

        elif self.move_pattern == "center_static":

            center = pygame.Vector2(settings.WIDTH//2, settings.HEIGHT//2)
            direction = center - self.pos

            if direction.length() > 5:
                current_speed = self.speed if self.speed > 0 else 150
                self.velocity = direction.normalize() * current_speed
            else:
                self.pos.x = center.x
                self.pos.y = center.y
                self.velocity = pygame.Vector2()

        elif self.move_pattern == "chase_player":

            direction = target.pos - self.pos

            if direction.length() > 0:
                self.velocity = direction.normalize() * self.speed

    # --- UPDATE ---

    def update(self, dt):

        super().update(dt)

        self.shoot_timer += dt
        self.update_phase()

        if self.shoot_timer >= self.attack_cooldown:
            self.shoot_timer = 0
            return self.patterns[self.phase]()

        return []

    # --- PHASE SYSTEM ---

    def update_phase(self):

        life_ratio = self.live_points / self.max_hp

        if self.phase == 1 and life_ratio <= self.phase_thresholds[0]:
            self.phase = 2
            self.attack_cooldown = 0.18

        elif self.phase == 2 and life_ratio <= self.phase_thresholds[1]:
            self.phase = 3
            self.attack_cooldown = 0.9
            self.move_pattern = "chase_player"

    # --- BULLET SPAWNER ---

    def spawn_bullet(self, direction, speed):

        return EnemyProjectile(
            self.pos.x,
            self.pos.y,
            direction.x,
            direction.y,
            self.damage,
            speed=speed
        )

    # --- PATTERNS ---
    
    def eye_ring(self):

        projectiles = []

        bullet_amount = 16
        step = 360 / bullet_amount
        self.pattern_rotation += 12

        for i in range(bullet_amount):

            direction = pygame.Vector2(1,0).rotate(i*step + self.pattern_rotation)

            projectiles.append(self.spawn_bullet(direction, 250))

        return projectiles
    
    def eye_double_spiral(self):

        projectiles = []

        self.spiral_angle += 18

        for offset in [0,180]:

            direction = pygame.Vector2(1,0).rotate(self.spiral_angle + offset)

            projectiles.append(self.spawn_bullet(direction, 320))

        return projectiles
    
    def eye_shotgun_ring(self):

        projectiles = []

        if not self.current_target:
            return projectiles

        direction = (self.current_target.pos - self.pos).normalize()

        for i in range(5):

            angle = (i-2)*10
            rotated = direction.rotate(angle)

            projectiles.append(self.spawn_bullet(rotated, 420))

        return projectiles
    
    def golem_ring(self):

        projectiles = []

        bullet_amount = 20
        step = 360 / bullet_amount

        for i in range(bullet_amount):

            direction = pygame.Vector2(1,0).rotate(i*step)

            projectiles.append(self.spawn_bullet(direction, 200))

        return projectiles
    
    def golem_wall(self):

        projectiles = []

        spacing = 80

        for x in range(0, settings.WIDTH, spacing):

            pos = pygame.Vector2(x,0)
            direction = pygame.Vector2(0,1)

            projectiles.append(
                EnemyProjectile(pos.x,pos.y,direction.x,direction.y,self.damage,200)
            )

        return projectiles
    
    def golem_wall_ring(self):

        projectiles = self.golem_wall()

        ring = self.golem_ring()

        projectiles.extend(ring)

        return projectiles