from entities.entity import Entity

class Collision:
    def check(e1,e2):
        return e1.get_rect().colliderect(e2.get_rect())