import pygame

class EnemyProjectile:
    def __init__(self, x, y, dir_x, dir_y, damage, speed=300):
        
        # --- BASE STATS ---
        self.pos = pygame.Vector2(x, y)
        self.size = 6
        self.color = (255, 100, 0)
        self.alive = True
        
        # --- PROJECTILE STATS ---
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.damage = damage
        self.speed = speed
        self.lifetime = 10.0 
        self.current_time = 0.0

    def update(self, dt):
        
        # --- MOVEMENT ---
        self.pos.x += self.dir_x * self.speed * dt
        self.pos.y += self.dir_y * self.speed * dt

        # --- LIFETIME ---
        self.current_time += dt
        if self.current_time >= self.lifetime:
            self.dead()

    def draw(self, screen):
        
        # --- DRAW ---
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.pos.x), int(self.pos.y)),
            self.size
        )

    def get_rect(self):
        
        # --- COLLISION ---
        return pygame.Rect(
            self.pos.x - self.size,
            self.pos.y - self.size,
            self.size * 2,
            self.size * 2
        )
        
    def dead(self):
        
        # --- DESTROY ---
        self.alive = False