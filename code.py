import pygame
import sys
import os

#initializer
pygame.init()

#setup variables
WIDTH, HEIGHT = 800, 600
PLAYER_BASE_SPEED = 4
PLAYER_SPRINT_SPEED = 8
TILE = 32
FEET_W, FEET_H = 24, 6
LAST_LEVEL = 5

#creates screen and sets up caption
screen = pygame.display.set.mode((WIDTH, HEIGHT))
pygame.display.set_caption("")

