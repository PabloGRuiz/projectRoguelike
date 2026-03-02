import math
import random
import settings

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT

def GenerateCoords(player, radius = 600):
    angle = random.uniform(0, 2 * math.pi)
    x = player.pos.x + radius * math.cos(angle)
    y = player.pos.y + radius * math.sin(angle)
    return x, y

    