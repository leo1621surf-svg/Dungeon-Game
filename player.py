import pygame

from settings import TILE, FEET_W, FEET_H, PLAYER_BASE_SPEED

class Player:
    def __init__(self, pos, player_images, map_width, map_height):
        self.image = player_images["down"]
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
        self.spawn_point = (1060, 130)
        self.weapon_side = "right"
        self.map_width = map_width
        self.map_height = map_height

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

        self.rect.clamp_ip(pygame.Rect(0, 0, self.map_width, self.map_height))

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
            weapon_y = self.rect.centery - 10

            if self.weapon_side == "right":
                weapon_x = self.rect.centerx + 3.5
            else:
                weapon_x = self.rect.left - self.equipped_weapon.rect.width + 10

            self.equipped_weapon.rect.topleft = (weapon_x, weapon_y)

            surface.blit(self.equipped_weapon.image, (weapon_x - camera_x, weapon_y - camera_y))
