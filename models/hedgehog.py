import random
import pygame

from lib.constants import HEDGEHOG_SKIN_SHEET_MAPPING, SKIN_COLORS
from models.spritesheet import SpriteSheet


class Hedgehog(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.skin = random.choice(SKIN_COLORS)
        self.sprite_sheet = SpriteSheet(
            HEDGEHOG_SKIN_SHEET_MAPPING[self.skin])

        self.index = 0
        self.counter = 0

        self.image = self.sprite_sheet.get_image(self.index, 1)

        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.left = x

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed * 2

        self.counter += 1
        flap_cooldown = 6

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1

            if self.index >= self.sprite_sheet.get_count() - 1:
                self.index = 0

        self.image = self.sprite_sheet.get_image(self.index, 1)

        if self.rect.right < 0:
            self.kill()
