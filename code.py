
import pygame
import sys
import os
import json

#initializer
pygame.init()

#setup variables
WIDTH, HEIGHT = 910, 690#728, 552
PLAYER_BASE_SPEED = 4
PLAYER_SPRINT_SPEED = 5
ENEMY_SPEED = 2.5
TILE = 32
FEET_W, FEET_H = 24, 6
LAST_LEVEL = 10
FONT = pygame.font.SysFont(None, 25)
SPRITESHEET_TILE = 16


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


    return level_data, walls, checkpoints

def draw_level_json(level_data, camera_x, camera_y):

    for layer in level_data["layers"]:
        for tile in layer["tiles"]:

            x = tile["x"] * TILE
            y = tile["y"] * TILE

            tile_id = int(tile["id"])

            source_x = (tile_id % TILES_PER_ROW) * SPRITESHEET_TILE
            source_y = (tile_id // TILES_PER_ROW) * SPRITESHEET_TILE

            tile_image = SPRITESHEET.subsurface(pygame.Rect(source_x, source_y, SPRITESHEET_TILE, SPRITESHEET_TILE))
            tile_image = pygame.transform.scale(tile_image, (TILE, TILE))
            screen.blit(tile_image, (x - camera_x, y - camera_y))

class Player:
    def __init__(self, pos):
        self.image = PLAYER_IMAGES["down"]
        self.direction = "down"
        self.rect = self.image.get_rect(topleft = pos)
        self.feet = pygame.Rect(0, 0, FEET_W, FEET_H)
        self.feet.centerx = self.rect.centerx
        self.feet.bottom = self.rect.bottom
        self.speed = PLAYER_BASE_SPEED
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.health = 100
        self.max_health = 100
        self.cooldown = 0
        self.inventory = []
        self.equipped_weapon = None
        self.alive = True
        self.current_checkpoint = 0
        self.spawn_point = (75, 75)

    def move(self, dx, dy, walls):

        self.x += dx
        self.rect.x = int(self.x)

        self.feet.centerx = self.rect.centerx
        self.feet.bottom = self.rect.bottom

        for w in walls:
            if self.rect.colliderect(w):
                if dx > 0:
                    self.rect.right = w.left
                elif dx < 0:
                    self.rect.left = w.right
                self.x = self.rect.x

        self.y += dy
        self.rect.y = int(self.y)

        self.feet.centerx = self.rect.centerx
        self.feet.bottom = self.rect.bottom

        for w in walls:
            if self.rect.colliderect(w):
                if dy > 0:
                    self.rect.bottom = w.top
                elif dy < 0:
                    self.rect.top = w. bottom
                self.y = self.rect.y

                self.feet.centerx = self.rect.centerx
                self.feet.bottom = self.rect.bottom

        self.rect.clamp_ip(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))

        self.x = self.rect.x
        self.y = self.rect.y

        self.feet.centerx = self.rect.centerx
        self.feet.bottom = self.rect.bottom


    def change_direction(self, dx, dy):
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "down"
        elif dy < 0:
            self.direction = "up"
        self.image = PLAYER_IMAGES[self.direction]

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

        if self.equipped_weapon is not None:
            weapon_x = self.rect.centerx + 3.5
            weapon_y = self.rect.centery - 10

            self.equipped_weapon.rect.topleft = (weapon_x, weapon_y)

            surface.blit(self.equipped_weapon.image, (weapon_x - camera_x, weapon_y - camera_y))

class Enemy:
    def __init__(self, pos, name, image):
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = ENEMY_SPEED
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.health = 100
        self.max_health = 100
        self.enemy_cooldown = 60
        self.text = ""
        self.timer = 0
        self.name = name
        self.range = 125

    def move(self, player, walls):
        dx = dy = 0

        x_distance = player.rect.centerx - self.rect.centerx
        y_distance = player.rect.centery - self.rect.centery
        distance = (x_distance**2 + y_distance**2) **0.5

        if distance <= self.range:

            if player.rect.centerx > self.rect.centerx:
                dx = self.speed
            elif player.rect.centerx < self.rect.centerx:
                dx = -self.speed

            if player.rect.centery > self.rect.centery:
                dy = self.speed
            elif player.rect.centery < self.rect.centery:
                dy = -self.speed

        self.x += dx
        self.rect.x = int(self.x)
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right
                self.x = self.rect.x

        self.y += dy
        self.rect.y = int(self.y)
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom
                self.y = self.rect.y

        if self.enemy_cooldown > 0:
            self.enemy_cooldown -= 1

        if self.timer > 0:
            self.timer -= 1

    def attack(self, player):
        if player.cooldown == 0 and self.rect.colliderect(player.rect):
            player.health -= 25
            player.health = max(player.health, 0)
            player.cooldown = 180

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

        if self.timer > 0:
            text = FONT.render(self.text, True, (255,0 ,0))
            surface.blit(text, (self.rect.centerx - camera_x - text.get_width() //2, self.rect.top - camera_y - 20))


class Weapon:
    def __init__(self, pos, name, image, damage):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.collected = False
        self.name = name
        self.equipped = False
        self.damage = damage


    def check_collect(self, player):
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True

            player.inventory.append(self)

            if player.equipped_weapon is None:
                player.equipped_weapon = self

    def draw(self, surface, camera_x, camera_y):
        if not self.collected:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

def draw_health_bar(surface, player):
    width = 200
    height = 20
    x, y = 10, 10

    pygame.draw.rect(surface, (200, 0, 0), (x, y, width, height))

    ratio = player.health / player.max_health

    pygame.draw.rect(surface, (0, 200, 0), (x, y, width * ratio, height))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)

def main():

    json_level, walls, checkpoints = load_level_json()

    global MAP_WIDTH, MAP_HEIGHT
    MAP_WIDTH = json_level["mapWidth"] * TILE
    MAP_HEIGHT = json_level["mapHeight"] * TILE

    player = Player((75, 75))

    camera_x = 0
    camera_y = 0

    enemies = [Enemy((200, 200), "Cyclops", ENEMY_IMAGES["cyclops"]), Enemy((1000, 400), "Ghost", ENEMY_IMAGES["ghost"])]
    weapon = [Weapon((300, 100), "Sword", IMAGE_SWORD, 25), Weapon((100, 550), "Axe", IMAGE_AXE, 30)]

    running = True
    while running:

        screen.fill((0, 0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        player.move(dx, dy, walls)

        if player.current_checkpoint < len(checkpoints):
            if player.rect.colliderect(checkpoints[player.current_checkpoint]):
                print("touched checkpoint")
                player.current_checkpoint += 1

        for checkpoint in checkpoints:
            pygame.draw.rect(screen, (255, 0, 0), (checkpoint.x - camera_x, checkpoint.y - camera_y, TILE, TILE), 2)

        camera_x = player.rect.centerx - WIDTH // 2
        camera_y = player.rect.centery - HEIGHT // 2

        camera_x = max(0, min(camera_x, MAP_WIDTH - WIDTH))
        camera_y = max(0, min(camera_y, MAP_HEIGHT - HEIGHT))

        if player.cooldown > 0:
            player.cooldown -= 1

        for enemy in enemies:
            enemy.move(player, walls)
            enemy.attack(player)

        if player.health <= 0:
            player.alive = False

        if player.equipped_weapon is not None:

            for enemy in enemies:
                if player.equipped_weapon.rect.colliderect(enemy.rect):
                    if enemy.enemy_cooldown == 0:

                        d = player.equipped_weapon.damage
                        enemy.health -= d
                        enemy.text = str(d)
                        enemy.timer = 60
                        print(enemy.health)
                        enemy.enemy_cooldown = 60

        for enemy in enemies[:]:
            if enemy.health <= 0:
                enemies.remove(enemy)

        for w in weapon:
            w.check_collect(player)

        draw_level_json(json_level, camera_x, camera_y)

        for w in weapon:
            w.draw(screen, camera_x, camera_y)

        if player.alive:
            player.draw(screen, camera_x, camera_y)

        for enemy in enemies:
            enemy.draw(screen, camera_x, camera_y)

        draw_health_bar(screen, player)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()