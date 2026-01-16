import pygame
import sys
import os

#initializer
pygame.init()

#setup variables
WIDTH, HEIGHT = 800, 640
PLAYER_BASE_SPEED = 4
PLAYER_SPRINT_SPEED = 8
TILE = 32
FEET_W, FEET_H = 24, 6
LAST_LEVEL = 10

#creates screen and sets up caption
screen = pygame.display.set.mode((WIDTH, HEIGHT))
pygame.display.set_caption("")

MAP_DIR = "/Users/leocabida/Desktop/PythonProject4"

def scale(img, factor):
    width, height = img.get_size()
    return pygame.transform.scale(img, (int(width* factor), int(height * factor) ))

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "sprites")
PLAYER_IMAGES = {
    "": scale(pygame.image.load(os.path.join(IMAGE_DIR, "")), 0.75),
    "": scale(pygame.image.load(os.path.join(IMAGE_DIR, "")), 0.75),
    "": scale(pygame.image.load(os.path.join(IMAGE_DIR, "")), 0.75),
    "": scale(pygame.image.load(os.path.join(IMAGE_DIR, "")), 0.75),
}

IMAGE_SAND = pygame.image.load(os.path.join(IMAGE_DIR, "plain sand.png"))

def load_map(filename):
    path = os.path.join(MAP_DIR, filename)
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]

def load_level(number):
    path = os.path.join(MAP_DIR, f"levels/level{number}.txt")

    if not os.path.exists(path):
        print("No More Levels")
        return None

    with open(path, "r") as f:
        raws = f.readlines()