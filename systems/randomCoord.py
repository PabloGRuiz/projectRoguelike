import random
import settings

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT

def GenerateCoords():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    return x, y
