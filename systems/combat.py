from systems.collision import Collision
from entities.experience import Experience
from entities.floating_text import FloatingText

class Combat:
    
    @staticmethod
    def apply_item_effect(item, player, enemies, experiences, floating_texts):

        for stat_name, amount in item.stats_changes.items():
            if hasattr(player, stat_name):
                current_value = getattr(player, stat_name)
                setattr(player, stat_name, current_value + amount)
                signo = "+" if amount > 0 else ""
                texto_feedback = f"{signo}{amount} {stat_name}"
                texto_flotante = FloatingText(player.pos.x, player.pos.y - 20, texto_feedback, (150, 255, 50))
                floating_texts.append(texto_flotante)
                
        for event in item.special_events:
            if event == "clear_screen":
                for enemy in enemies:
                    if enemy.alive:
                        enemy.dead()
                        xp = Experience(enemy.pos.x, enemy.pos.y, 1)
                        experiences.append(xp)
                        floating_texts.append(FloatingText(enemy.pos.x, enemy.pos.y, "BOOM!", (255, 100, 0)))


    @staticmethod
    def check_entity_collision(player, enemies, projectiles, experiences, items, floating_texts):

        for xp in experiences:
            if Collision.check(player, xp):
                player.level_up(xp.experience)
                xp.dead()

        for item in items:
            if Collision.check(player, item):
                Combat.apply_item_effect(item, player, enemies, experiences, floating_texts)
                print(f"Recogiste un/a {item.name}!")
                item.dead()

        for enemy in enemies:

            if Collision.check(player, enemy):
                if player.alive:
                    if player.live_points - enemy.damage <= 0:
                        print("Moriste!")
                    player.live_points -= enemy.damage

            for projectile in projectiles:
                if Collision.check(projectile, enemy):
                    if enemy.alive and projectile.alive:

                        damage_text = FloatingText(
                            enemy.pos.x,
                            enemy.pos.y - 10,
                            projectile.damage
                        )
                        floating_texts.append(damage_text)

                        if enemy.live_points - projectile.damage <= 0:
                            xp = Experience(enemy.pos.x, enemy.pos.y, 1)
                            experiences.append(xp)

                        enemy.live_points -= projectile.damage

                        # 🔥 ahora sí usamos el sistema nuevo
                        projectile.on_hit(enemies)