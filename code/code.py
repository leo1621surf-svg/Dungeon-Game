
import pygame
import sys
import os

#initializer
pygame.init()

#setup variables
WIDTH, HEIGHT = 800, 640
PLAYER_BASE_SPEED = 4
PLAYER_SPRINT_SPEED = 8
ENEMY_SPEED = 5
TILE = 32
FEET_W, FEET_H = 24, 6
LAST_LEVEL = 10

#creates screen and sets up caption
screen = pygame.display.set.mode((WIDTH, HEIGHT))
pygame.display.set_caption("")

MAP_DIR = "/"

def scale(img, factor):
    width, height = img.get_size()
    return pygame.transform.scale(img, (int(width* factor), int(height * factor) ))

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "sprites")
PLAYER_IMAGES = {
    "player.png": scale(pygame.image.load(os.path.join(IMAGE_DIR, "player.png")), 0.75),
    "": scale(pygame.image.load(os.path.join(IMAGE_DIR, "")), 0.75),
    "": scale(pygame.image.load(os.path.join(IMAGE_DIR, "")), 0.75),
    "": scale(pygame.image.load(os.path.join(IMAGE_DIR, "")), 0.75),
}

ENEMY_IMAGES = {
    "cyclops.png": scale(pygame.image.load(os.path.join(IMAGE_DIR, "cyclops.png")), 0.75),
    "ghost.png": scale(pygame.image.load(os.path.join(IMAGE_DIR, "ghost.png")), 0.75),
}

IMAGE_SAND = pygame.image.load(os.path.join(IMAGE_DIR, "plain sand.png"))
IMAGE_WALL = pygame.image.load(os.path.join(IMAGE_DIR, "wall.png"))

def load_map(filename):
    path = os.path.join(MAP_DIR, filename)
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]

def load_level(number):
    path = os.path.join(MAP_DIR, f"levels/level{number}.txt")

    if not os.path.exists(path):
        print("No More Levels")
        return None

    walls = []
    with open(path, "r") as f:
        rows = f.readlines()
    return walls

class Player:
    def __init__(self, pos):
        self.image = PLAYER_IMAGES["down"]
        self.direction = "down"
        self.rect = self.image.get_rect(topleft = pos)
        self.feet = pygame.Rect(0, 0, FEET_W, FEET_H)
        self.feet.centerx = self.rect.centerx
        self.feet.bottom = self.rect.bottom
        self.speed = PLAYER_BASE_SPEED
        self.lives = 5

    def move(self, dx, dy, walls):

        self.rect.x += dx

        self.feet.centerx = self.rect.centerx
        self.feet.bottom = self.rect.bottom

        for w in walls:
            if self.feet.colliderect(w):
                if dx > 0:
                    self.feet.right = w.left
                elif dx < 0:
                    self.rect.left = w.right

        self.rect.y += dy

        self.feet.centerx = self.rect.centerx
        self.feet.bottom = self.rect.bottom

        for w in walls:
            if dy > 0:
                self.rect.bottom = w.top
            elif dy < 0:
                self.rect.top = w. bottom

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
        self.image = "cyclops.png"
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = ENEMY_SPEED
        self.cooldown = 0

    def move(self, player, walls):
        dx = dy = 0

        if player.rect.centerx > self.rect.centerx:
            dx = self.speed
        elif player.rect.centerx < self.rect.centerx:
            dx = -self.speed

        if player.rect.centery > self.rect.centerx:
            dy = self.speed
        elif player.rect.centery < self.rect.centerx:
            dy = -self.speed

        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right

        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom

        if self.cooldown > 0:
            self.cooldown -= 1

    def attack(self, player):
        if self.cooldown == 0 and self.rect.colliderect(player.rect):
            player.lives -= 1
            self.cooldown = 180

def draw(self, surface):
    surface.blit(self.image, self.rect.topleft)

def build(level_map):
    walls = []
    return walls

def main():
    current_level = 1
    walls = load_level(current_level)

