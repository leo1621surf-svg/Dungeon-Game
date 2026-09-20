import pygame
from settings import ENEMY_SPEED

class Enemy:
    def __init__(self, pos, name, image, font):
        self.image = image
        self.font = font
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
            player.health -= 15
            player.health = max(player.health, 0)
            player.cooldown = 180

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

        if self.timer > 0:
            text = self.font.render(self.text, True, (255,0 ,0))
            surface.blit(text, (self.rect.centerx - camera_x - text.get_width() //2, self.rect.top - camera_y - 20))
