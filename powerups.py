import pygame

POWERUPS = ["Max Health Up", "Run Speed Up", "Damage Up", "Damage Reduction", "Attack Speed Up", "Enemy Poison", "Health Repair", "Remove Enemy"]

def apply_powerup(name, player, remove_enemy):
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
        if not player.damage_powerup_active:
            player.original_damage = player.eqquiped_weapon.damage
            player.eqquiped_weapon.damage *= 1.25
            player.damage_powerup_active = True

        player.damage_powerup_endtime = pygame.time.get_ticks()+30000
        print("this worked!!!")

    elif name == "Damage Reduction":
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

