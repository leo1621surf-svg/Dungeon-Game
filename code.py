
import pygame
import sys
import os

#initializer
pygame.init()

#setup variables
WIDTH, HEIGHT = 800, 640
PLAYER_BASE_SPEED = 1.5
PLAYER_SPRINT_SPEED = 5
ENEMY_SPEED = 0.75
TILE = 32
FEET_W, FEET_H = 24, 6
LAST_LEVEL = 10

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

def load_level(number):
    path = os.path.join(MAP_DIR, f"level{number}.txt")
    print("looking for", path)

    if not os.path.exists(path):
        return None, None

    with open(path, "r") as f:
        level_map = [line.strip() for line in f.readlines()]

    walls = []
    enemies = []

    for row_index, row in enumerate(level_map):
        for column_index, char in enumerate(row):
            x = column_index * TILE
            y = row_index * TILE
            if char == "#":
                walls.append(pygame.Rect(x, y, TILE, TILE))
            elif char == "e":
                enemies.append((x, y))

    return level_map, walls, enemies

def draw_level(level_map):
    for row_index, row in enumerate(level_map):
        for column_index, char in enumerate(row):
            x = column_index * TILE
            y = row_index * TILE

            screen.blit(IMAGE_SAND, (x, y))

            if char == "#":
                screen.blit(IMAGE_WALL, (x, y))

            elif char == "D":
                screen.blit(IMAGE_DOOR, (x, y))

            elif char == "B":
                screen.blit(IMAGE_BARREL, (x, y))

            elif char == "T":
                screen.blit(IMAGE_TOP, (x, y))

            elif char == "L":
                rotated = pygame.transform.rotate(IMAGE_TOP_LEFT, 90)
                screen.blit(rotated, (x, y))

            elif char == "C":
                screen.blit(IMAGE_CORNER, (x, y))

            elif char == "S":
                screen.blit(IMAGE_SPOTS, (x, y))

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

        self.rect.clamp_ip(screen.get_rect())
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

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Enemy:
    def __init__(self, pos):
        self.image = ENEMY_IMAGES["cyclops"]
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = ENEMY_SPEED
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.health = 100
        self.max_health = 100

    def move(self, player, walls):
        dx = dy = 0

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

        self.y += dy
        self.rect.y = int(self.y)
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom

    def attack(self, player):
        if player.cooldown == 0 and self.rect.colliderect(player.rect):
            player.health -= 20
            player.health = max(player.health, 0)
            player.cooldown = 180

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Weapon:
    def __init__(self, pos, name):
        self.image = IMAGE_SWORD
        self.rect = self.image.get_rect(topleft=pos)
        self.collected = False
        self.name = name

    def check_collect(self, player):
        if self.rect.colliderect(player.rect):
            self.collected = True

            player.inventory.append(self)

            if player.equipped_weapon is None:
                player.equipped_weapon = self

    def draw(self, surface):
        if not self.collected:
            surface.blit(self.image, self.rect.topleft)

def draw_health_bar(surface, player):
    width = 200
    height = 20
    x, y = 10, 10

    pygame.draw.rect(surface, (200, 0, 0), (x, y, width, height))

    ratio = player.health / player.max_health

    pygame.draw.rect(surface, (0, 200, 0), (x, y, width * ratio, height))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)

def main():
    current_level = 1
    level_map, walls, enemy_positions = load_level(current_level)

    if level_map is None:
        print ("level not found")
        pygame.quit()
        return

    player = Player((TILE, TILE))
    enemies = [Enemy(pos) for pos in enemy_positions]
    weapon = Weapon((300, 300))

    running = True
    while running:

        screen.fill((0, 0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        if player.cooldown > 0:
            player.cooldown -= 1

        for enemy in enemies:
            enemy.move(player, walls)
            enemy.attack(player)

        weapon.check_collect(player)

        draw_level(level_map)
        weapon.draw(screen)
        player.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        draw_health_bar(screen, player)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()