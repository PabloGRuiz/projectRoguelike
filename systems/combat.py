import pygame
from systems.collision import Collision
from entities.experience import Experience
from entities.floating_text import FloatingText
from entities.boss import Boss

class Combat:
    
    @staticmethod
    def apply_item_effect(item, player, enemies, experiences, floating_texts):
        # Apply dynamic stat changes
        for stat_name, amount in item.stats_changes.items():
            if hasattr(player, stat_name):
                current_value = getattr(player, stat_name)
                setattr(player, stat_name, current_value + amount)
                
                sign = "+" if amount > 0 else ""
                feedback_text = f"{sign}{amount} {stat_name}"
                floating_text = FloatingText(player.pos.x, player.pos.y - 20, feedback_text, (150, 255, 50))
                floating_texts.append(floating_text)
                
        # Handle special events
        for event in item.special_events:
            if event == "clear_screen":
                for enemy in enemies:
                    # Prevent instant boss deletion
                    if enemy.alive and not isinstance(enemy, Boss):
                        enemy.dead()
                        xp = Experience(enemy.pos.x, enemy.pos.y, 1)
                        experiences.append(xp)
                        floating_texts.append(FloatingText(enemy.pos.x, enemy.pos.y, "BOOM!", (255, 100, 0)))


    @staticmethod
    def check_entity_collision(player, enemies, projectiles, enemy_projectiles, experiences, items, floating_texts):
        # Get internal clock for I-Frames
        current_time = pygame.time.get_ticks()

        # --- XP COLLISIONS ---
        for xp in experiences:
            if xp.alive and Collision.check(player, xp):
                player.level_up(xp.experience)
                xp.dead()

        # --- ITEM COLLISIONS ---
        for item in items:
            if item.alive and Collision.check(player, item):
                Combat.apply_item_effect(item, player, enemies, experiences, floating_texts)
                item.dead()

        # --- ENEMY COLLISIONS ---
        for enemy in enemies:
            
            # 1. Player vs Enemy (Melee)
            if enemy.alive and Collision.check(player, enemy):
                if player.alive:
                    last_player_hit = getattr(player, 'last_hit_time', 0)
                    
                    # Player I-Frames: 1000ms (1 second)
                    if current_time - last_player_hit > 1000:
                        if player.live_points - enemy.damage <= 0:
                            print("You died!")
                        player.live_points -= enemy.damage
                        player.last_hit_time = current_time

                        damage_text = FloatingText(player.pos.x, player.pos.y - 10, enemy.damage, (255, 50, 50))
                        floating_texts.append(damage_text)

            # 2. Player Projectiles vs Enemy
            for projectile in projectiles:
                if enemy.alive and projectile.alive and Collision.check(projectile, enemy):
                    last_enemy_hit = getattr(enemy, 'last_hit_time', 0)
                    
                    # Enemy I-Frames: 100ms
                    if current_time - last_enemy_hit > 100:
                        damage_text = FloatingText(enemy.pos.x, enemy.pos.y - 10, projectile.damage)
                        floating_texts.append(damage_text)

                        if enemy.live_points - projectile.damage <= 0:
                            xp = Experience(enemy.pos.x, enemy.pos.y, 1)
                            experiences.append(xp)

                        enemy.live_points -= projectile.damage
                        enemy.last_hit_time = current_time
                        
                        # New dynamic projectile system
                        projectile.on_hit(enemies)

        # --- BOSS PROJECTILES VS PLAYER ---
        for ep in enemy_projectiles:
            if ep.alive and Collision.check(player, ep):
                if player.alive:
                    last_player_hit = getattr(player, 'last_hit_time', 0)
                    
                    # Player I-Frames against bullets: 500ms
                    if current_time - last_player_hit > 500:
                        if player.live_points - ep.damage <= 0:
                            print("You died!")
                        player.live_points -= ep.damage
                        player.last_hit_time = current_time
                        
                        damage_text = FloatingText(player.pos.x, player.pos.y - 10, ep.damage, (255, 50, 50))
                        floating_texts.append(damage_text)

                ep.dead()