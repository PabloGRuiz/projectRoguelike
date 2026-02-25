from systems.collision import Collision
from entities.experience import Experience

class Combat:
    def check_entity_collision(player, enemies, projectiles, experiences):
        
        for xp in experiences:
                if Collision.check(player,xp):
                    player.xp += xp.experience
                    print("experiencia total: " + str(player.xp))
                    xp.dead()
            
        for enemy in enemies:
            for projectile in projectiles:
                
                if Collision.check(player,enemy):
                    if player.alive:
                        if player.live_points - enemy.damage <= 0 and player.alive:
                            print("Moriste!")
                        player.live_points -= enemy.damage
                            
                    
                if Collision.check(projectile,enemy):
                    if enemy.alive:
                        if enemy.live_points - projectile.damage <= 0:
                            xp = Experience(enemy.pos.x, enemy.pos.y, 1)
                            experiences.append(xp)
                        enemy.live_points -= projectile.damage
                        projectile.dead()  