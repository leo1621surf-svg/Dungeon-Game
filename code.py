import pygame
import sys
import os
import json
import random

from settings import *
from player import Player
from enemy import Enemy
from weapon import Weapon

#initializer
pygame.init()

FONT = pygame.font.SysFont(None, 25)
POWERUP_FONT = pygame.font.SysFont(None, 35)

POWERUPS = ["Max Health Up", "Run Speed Up", "Damage Up", "Damage Reduction", "Attack Speed Up", "Enemy Poison", "Health Repair", "Remove Enemy"]

#creates screen and sets up caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")

clock = pygame.time.Clock()
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "sprites")
BASE_DIR = os.path.dirname(__file__)

MAP_DIR = os.path.join(BASE_DIR, "levels")

def scale(img, factor):
    width, height = img.get_size()
    return pygame.transform.scale(img, (int(width* factor), int(height * factor) ))

PLAYER_IMAGES = {
    "down": scale(pygame.image.load(os.path.join(IMAGE_DIR, "player.png")), 1.4),
    #"": scale(pygame.image.load(os.path.join(IMAGE_DIR, "")), 0.75),
   #"": scale(pygame.image.load(os.path.join(IMAGE_DIR, "")), 0.75),
   #"": scale(pygame.image.load(os.path.join(IMAGE_DIR, "")), 0.75),
}

ENEMY_IMAGES = {
    "cyclops": scale(pygame.image.load(os.path.join(IMAGE_DIR, "cyclops.png")), 1.2),
    "ghost": scale(pygame.image.load(os.path.join(IMAGE_DIR, "ghost.png")), 1.2),
}

IMAGE_SAND = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "plain sand.png")),(TILE, TILE))
IMAGE_WALL = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DIR, "plain brown tile.png")),(TILE, TILE))
IMAGE_DOOR = scale(pygame.image.load(os.path.join(IMAGE_DIR, "single door.png")), 2)
IMAGE_BARREL = scale(pygame.image.load(os.path.join(IMAGE_DIR, "barrel.png")), 2)
IMAGE_TOP = scale(pygame.image.load(os.path.join(IMAGE_DIR, "top wall.png")), 2)
IMAGE_TOP_LEFT = scale(pygame.image.load(os.path.join(IMAGE_DIR, "top wall.png")), 2)
IMAGE_CORNER = scale(pygame.image.load(os.path.join(IMAGE_DIR, "wall corner.png")), 2)
IMAGE_SPOTS = scale(pygame.image.load(os.path.join(IMAGE_DIR, "spotted sand.png")), 2)
IMAGE_SWORD = scale(pygame.image.load(os.path.join(IMAGE_DIR, "sword.png")), 1.3)
IMAGE_AXE = scale(pygame.image.load(os.path.join(IMAGE_DIR, "axe.png")), 1.3)

SPRITESHEET = pygame.image.load(os.path.join(IMAGE_DIR, "spritesheet.png")).convert_alpha()
TILES_PER_ROW = SPRITESHEET.get_width() // SPRITESHEET_TILE

MAP_WIDTH = 0
MAP_HEIGHT = 0

def load_level_json():
    path = os.path.join(MAP_DIR, "map.json")

    with open(path, "r") as f:
        level_data = json.load(f)

    walls = []
    checkpoints = []
    unlocks = []
    doors = []
    locks = []

    for layer in level_data["layers"]:

        if layer["name"] == "Walls":
            for tile in layer["tiles"]:
                x = tile["x"] * TILE
                y = tile["y"] * TILE

                walls.append(pygame.Rect(x, y, TILE, TILE))

        if layer["name"] == "Checkpoints":
            for tile in layer["tiles"]:
                x = tile["x"] * TILE
                y = tile["y"] * TILE

                checkpoints.append(pygame.Rect(x, y, TILE, TILE))

        if layer["name"] == "Unlocks":
            for tile in layer["tiles"]:
                x = tile["x"] * TILE
                y = tile["y"] * TILE

                unlocks.append(pygame.Rect(x, y, TILE, TILE))

        if layer["name"] == "Doors":
            for tile in layer["tiles"]:
                x = tile["x"] * TILE
                y = tile["y"] * TILE

                doors.append(pygame.Rect(x, y, TILE, TILE))

        if layer["name"] == "Locks":
            for tile in layer["tiles"]:
                x = tile["x"] * TILE
                y = tile["y"] * TILE

                locks.append(pygame.Rect(x, y, TILE, TILE))


    return level_data, walls, checkpoints, unlocks, doors, locks

def draw_level_json(level_data, camera_x, camera_y):

    for layer in level_data["layers"]:

        if layer["name"] == "Doors":
            continue

        for tile in layer["tiles"]:

            x = tile["x"] * TILE
            y = tile["y"] * TILE

            tile_id = int(tile["id"])

            source_x = (tile_id % TILES_PER_ROW) * SPRITESHEET_TILE
            source_y = (tile_id // TILES_PER_ROW) * SPRITESHEET_TILE

            tile_image = SPRITESHEET.subsurface(pygame.Rect(source_x, source_y, SPRITESHEET_TILE, SPRITESHEET_TILE))
            tile_image = pygame.transform.scale(tile_image, (TILE, TILE))
            screen.blit(tile_image, (x - camera_x, y - camera_y))


def draw_doors(level_data, camera_x, camera_y):
    for layer in level_data["layers"]:

        if layer["name"] != "Doors":
            continue

        for tile in layer["tiles"]:
            x = tile["x"] * TILE
            y = tile["y"] * TILE

            tile_id = int(tile["id"])

            source_x = (tile_id % TILES_PER_ROW) * SPRITESHEET_TILE
            source_y = (tile_id // TILES_PER_ROW) * SPRITESHEET_TILE

            tile_image = SPRITESHEET.subsurface(pygame.Rect(source_x, source_y, SPRITESHEET_TILE, SPRITESHEET_TILE))
            tile_image = pygame.transform.scale(tile_image, (TILE, TILE))
            screen.blit(tile_image, (x - camera_x, y - camera_y))

def draw_health_bar(surface, player):
    width = 200
    height = 20
    x, y = 10, 10

    pygame.draw.rect(surface, (200, 0, 0), (x, y, width, height))

    ratio = player.health / player.max_health

    pygame.draw.rect(surface, (0, 200, 0), (x, y, width * ratio, height))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)

def text_wrap(surface, text, font, font_color, center_x, y, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word

        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    line_height = font.get_linesize()

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, font_color)
        text_rect = text_surface.get_rect(center=(center_x, y + i * line_height))
        surface.blit(text_surface, text_rect)


def draw_powerup_menu(surface, available_powerups):
    width, height = 600, 450
    x = (WIDTH - width) // 2
    y = (HEIGHT - height) // 2
    rectangle = pygame.Rect(x, y, width, height)

    pygame.draw.rect(surface, (0, 0, 0), rectangle)
    pygame.draw.rect(surface, (255, 255, 255), rectangle, 3)

    button_width = 150
    button_height = 75
    button_y = y + 320

    button1 = pygame.Rect(x + 40, button_y, button_width, button_height)
    button2 = pygame.Rect(x + 225, button_y, button_width, button_height)
    button3 = pygame.Rect(x + 410, button_y, button_width, button_height)

    buttons = [button1, button2, button3]

    for i in range(3):

        pygame.draw.rect(surface, (70, 70, 70), buttons[i])
        pygame.draw.rect(surface, (255, 255, 255), buttons[i], 3)

        text_wrap(surface, available_powerups[i], POWERUP_FONT, (255, 255, 255), buttons[i].centerx, button_y -50, button_width - 10)

        select_text = FONT.render("SELECT", True, (255, 255, 255))
        select_rect = select_text.get_rect(center=buttons[i].center)
        surface.blit(select_text, select_rect)

    return buttons


def main():

    json_level, walls, checkpoints, unlocks, doors, locks = load_level_json()

    global MAP_WIDTH, MAP_HEIGHT
    MAP_WIDTH = json_level["mapWidth"] * TILE
    MAP_HEIGHT = json_level["mapHeight"] * TILE

    current_room = 1
    menu_open = False
    power_selected = False
    available_powerups = []

    player = Player((1060, 130), PLAYER_IMAGES, MAP_WIDTH, MAP_HEIGHT)
    doors_open = False

    game_state = "Playing"
    powerup_claimed = False

    camera_x = 0
    camera_y = 0

    room_one_enemies = [Enemy((100, 200), "Cyclops", ENEMY_IMAGES["cyclops"], FONT)]#[Enemy((100, 200), "Cyclops", ENEMY_IMAGES["cyclops"], FONT),Enemy((300, 75), "Cyclops", ENEMY_IMAGES["cyclops"], FONT),
                        #Enemy((200, 550), "Ghost", ENEMY_IMAGES["ghost"], FONT)]
    room_two_enemies = [Enemy((100, 1250), "Ghost", ENEMY_IMAGES["ghost"], FONT), Enemy((500, 1250), "Ghost", ENEMY_IMAGES["ghost"], FONT)]
    room_three_enemies = []
    room_four_enemies = []
    room_five_enemies = []
    room_six_enemies = []
    room_seven_enemies = []
    room_eight_enemies = []
    room_nine_enemies = []
    room_ten_enemies = []

    weapon = [Weapon((300, 100), "Sword", IMAGE_SWORD, 25), Weapon((100, 550), "Axe", IMAGE_AXE, 35)]

    running = True
    while running:

        screen.fill((0, 0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "Playing":
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_1:
                        if len(player.inventory) >= 1:

                            for w in player.inventory:
                                w.equipped = False

                            player.inventory[0].equipped = True
                            player.equipped_weapon = player.inventory[0]

                    if event.key == pygame.K_2:
                        if len(player.inventory) >= 2:

                            for w in player.inventory:
                                w.equipped = False

                            player.inventory[1].equipped = True
                            player.equipped_weapon = player.inventory[1]

                    if event.key == pygame.K_3:
                        if len(player.inventory) >= 3:

                            for w in player.inventory:
                                w.equipped = False

                            player.inventory[2].equipped = True
                            player.equipped_weapon = player.inventory[2]

                    if event.key == pygame.K_4:
                        if len(player.inventory) >= 4:

                            for w in player.inventory:
                                w.equipped = False

                            player.inventory[3].equipped = True
                            player.equipped_weapon = player.inventory[3]

                    if event.key == pygame.K_5:
                        if len(player.inventory) >= 5:

                            for w in player.inventory:
                                w.equipped = False

                            player.inventory[4].equipped = True
                            player.equipped_weapon = player.inventory[4]

                    if event.key == pygame.K_q:
                        if player.weapon_side == "right":
                            player.weapon_side = "left"
                        else:
                            player.weapon_side = "right"

            elif game_state == "Powerup_Choice":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()

                    width, height = 600, 450
                    x = (WIDTH - width) // 2
                    y = (HEIGHT - height) // 2

                    button_width = 150
                    button_height = 75
                    button_y = y + 320

                    button1 = pygame.Rect(x + 40, button_y, button_width, button_height)
                    button2 = pygame.Rect(x + 225, button_y, button_width, button_height)
                    button3 = pygame.Rect(x + 410, button_y, button_width, button_height)

                    buttons = [button1, button2, button3]
                    for i in range(3):
                        if buttons[i].collidepoint(mouse_position):
                            selected_powerup = available_powerups[i]
                            power_selected = True
                            game_state = "Playing"
                            menu_open = False
                            powerup_claimed = True
                            break

        if game_state == "Playing":

            keys = pygame.key.get_pressed()
            dx = 0
            dy = 0

            if keys[pygame.K_a]:
                dx = -player.speed
            if keys[pygame.K_d]:
                dx = player.speed
            if keys[pygame.K_s]:
                dy = player.speed
            if keys[pygame.K_w]:
                dy = -player.speed

            collision_rects = walls.copy()

            if not doors_open:
                collision_rects.extend(doors)

            player.move(dx, dy, collision_rects)

            for checkpoint in checkpoints:
                if player.rect.colliderect(checkpoint):
                    player.spawn_point = (checkpoint.centerx - player.rect.width // 2,checkpoint.centery - player.rect.height // 2)

            for checkpoint in checkpoints:
                pygame.draw.rect(screen, (255, 0, 0), (checkpoint.x - camera_x, checkpoint.y - camera_y, TILE, TILE), 2)

            camera_x = player.rect.centerx - WIDTH // 2
            camera_y = player.rect.centery - HEIGHT // 2

            camera_x = max(0, min(camera_x, MAP_WIDTH - WIDTH))
            camera_y = max(0, min(camera_y, MAP_HEIGHT - HEIGHT))

            if player.cooldown > 0:
                player.cooldown -= 1

            if current_room == 1:
                enemies = room_one_enemies
            elif current_room == 2:
                enemies = room_two_enemies
            elif current_room == 3:
                enemies = room_three_enemies
            elif current_room == 4:
                enemies = room_four_enemies
            elif current_room == 5:
                enemies = room_five_enemies
            elif current_room == 6:
                enemies = room_six_enemies
            elif current_room == 7:
                enemies = room_seven_enemies
            elif current_room == 8:
                enemies = room_eight_enemies
            elif current_room == 9:
                enemies = room_nine_enemies
            else:
                enemies = room_ten_enemies

            if len(enemies) == 0 and power_selected:
                for unlock in unlocks:
                    if player.rect.colliderect(unlock):
                        doors_open = True


            for enemy in enemies:
                enemy.move(player, walls)
                enemy.attack(player)

            if player.health <= 0:
                player.health = player.max_health * 0.75

                player.rect.topleft = player.spawn_point
                player.x = player.rect.x
                player.y = player.rect.y

                player.feet.centerx = player.rect.centerx
                player.feet.bottom = player.rect.bottom


            if player.equipped_weapon is not None:

                for enemy in enemies:
                    if player.equipped_weapon.rect.colliderect(enemy.rect):
                        if enemy.enemy_cooldown == 0:

                            d = player.equipped_weapon.damage
                            enemy.health -= d
                            enemy.text = str(d)
                            enemy.timer = 60
                            enemy.enemy_cooldown = 60

            for enemy in enemies[:]:
                if enemy.health <= 0:
                    enemies.remove(enemy)

            if len(enemies) == 0 and not powerup_claimed:
                game_state = "Powerup_Choice"
                powerup_claimed = True
                menu_open = True
                available_powerups = random.sample(POWERUPS, 3)
            else:
                menu_open = False

            if doors_open:
                for lock in locks:
                    if lock.contains(player.rect):
                        doors_open = False
                        current_room += 1
                        powerup_claimed = False
                        power_selected = False
                        game_state = "Playing"
                        menu_open = False
                        break

            if len(enemies) == 0 and powerup_claimed:
                for unlock in unlocks:
                    if player.rect.colliderect(unlock):
                        doors_open = True

            for w in weapon:
                w.check_collect(player)

        draw_level_json(json_level, camera_x, camera_y)

        for w in weapon:
            w.draw(screen, camera_x, camera_y)

        if player.alive:
            player.draw(screen, camera_x, camera_y)

        draw_doors(json_level, camera_x, camera_y)

        for enemy in enemies:
            enemy.draw(screen, camera_x, camera_y)

        draw_health_bar(screen, player)
        if menu_open:
            menu_height = 300
            menu_width = 500

            x = (WIDTH - menu_width) // 2
            y = (HEIGHT - menu_height) // 2

            pygame.draw.rect(screen, (50, 50, 50), (x, y, menu_width, menu_height))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, menu_width, menu_height), 3)

        if game_state == "Powerup_Choice":
            draw_powerup_menu(screen, available_powerups)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()