import pygame

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