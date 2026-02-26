from systems.collision import Collision
from entities.experience import Experience
from entities.floating_text import FloatingText

class Combat:
    def check_entity_collision(player, enemies, projectiles, experiences, items, floating_texts):
        
        for xp in experiences:
                if Collision.check(player,xp):
                    player.level_up(xp.experience)
                    print("experiencia total: " + str(player.xp))
                    xp.dead()
        
        for item in items:
                if Collision.check(player,item):
                    if item.type == "heal":
                        player.live_points += item.amount
                    elif item.type == "increase_damage":
                        player.shoot_damage += item.amount
                    elif item.type == "increase_speed":
                        player.speed += item.amount
                    print(f"Recogiste un {item.name}!")
                    item.dead()

        for enemy in enemies:
            for projectile in projectiles:
                
                if Collision.check(player,enemy):
                    if player.alive:
                        if player.live_points - enemy.damage <= 0 and player.alive:
                            print("Moriste!")
                        player.live_points -= enemy.damage
                            
                    
                if Collision.check(projectile,enemy):
                    if enemy.alive:
                        damage_text = FloatingText(enemy.pos.x, enemy.pos.y - 10, projectile.damage)
                        floating_texts.append(damage_text)
                        if enemy.live_points - projectile.damage <= 0:
                            xp = Experience(enemy.pos.x, enemy.pos.y, 1)
                            experiences.append(xp)
                        enemy.live_points -= projectile.damage
                        projectile.dead()  