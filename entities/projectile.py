import pygame
import settings

class Projectile:
    def __init__(self, x, y, direction, speed, damage,  pierce=0, bounce=0):

        self.size = 4
        self.color = (149, 39, 245)
        self.radius = 5

        self.pos = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2(direction)

        if self.direction.length() != 0:
            self.direction = self.direction.normalize()

        self.speed = speed

        self.damage = damage
        self.pierce = pierce
        self.bounce = bounce

        self.alive = True

    def update(self, dt):
        self.pos += self.direction * self.speed * dt

        # Matar si sale de pantalla
        if (
            self.pos.x < 0 or
            self.pos.x > settings.WIDTH or
            self.pos.y < 0 or
            self.pos.y > settings.HEIGHT
        ):
            self.alive = False

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.pos.x), int(self.pos.y)),
            self.size
        )

    def get_rect(self):
        return pygame.Rect(
            self.pos.x - self.radius,
            self.pos.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def on_hit(self, enemies):
        if self.pierce > 0:
            self.pierce -= 1
        else:
            self.alive = False

        if self.bounce > 0:
            self.bounce -= 1
            nearest = self.find_nearest_enemy(enemies)
            if nearest:
                new_dir = nearest.pos - self.pos
                if new_dir.length() != 0:
                    self.direction = new_dir.normalize()

    def find_nearest_enemy(self, enemies):
        nearest = None
        min_dist = float("inf")

        for enemy in enemies:
            dist = (enemy.pos - self.pos).length()
            if dist < min_dist:
                min_dist = dist
                nearest = enemy

        return nearest