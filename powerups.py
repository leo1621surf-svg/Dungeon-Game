import pygame
import math

#POWERUPS = ["Max Health Up", "Run Speed Up", "Damage Up", "Damage Reduction", "Attack Speed Up", "Enemy Poison", "Health Repair", "Remove Enemy"]
POWERUPS = ["Run Speed Up", "Damage Up", "Damage Reduction"]

def apply_powerup(name, player, enemies):
    if name  == "Max Health Up":
        player.max_health += 20
        print("health increased!!!")

    elif name == "Run Speed Up":
        if not player.speed_powerup_active:
            player.speed += 0.5
            player.speed_powerup_active = True

        player.speed_powerup_endtime = pygame.time.get_ticks()+30000
        print("speed increased!!!")

    elif name == "Damage Up":
        if player.equipped_weapon is not None:
            if not player.damage_powerup_active:
                player.damage_powerup_weapon = player.equipped_weapon
                player.original_damage = player.equipped_weapon.damage
                player.equipped_weapon.damage = math.ceil(player.equipped_weapon.damage * 1.25)
                player.damage_powerup_active = True

        player.damage_powerup_endtime = pygame.time.get_ticks()+30000
        print("this worked!!!")

    elif name == "Damage Reduction":
        if not player.damage_reduction_active:
            player.original_enemy_damage = {}

            for enemy in enemies:
                player.original_enemy_damage[enemy] = enemy.damage
                enemy.damage *= 0.85

            player.damage_reduction_active = True
        player.damage_reduction_endtime = pygame.time.get_ticks()+30000
        print("this worked!!!")

    elif name == "Attack Speed Up":
        print("this worked!!!")

    elif name == "Enemy Poison":
        print("this worked!!!")

    elif name == "Health Repair":
        player.health = min(player.health + 50, player.max_health)
        print("this worked!!!")

    elif name == "Remove Enemy":
        print("enemy removed")

