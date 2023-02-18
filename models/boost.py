import random
import pygame

from lib.constants import BOOST_SPRITES, BOOST_TYPES


class Boost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.type = random.choice(BOOST_TYPES)
        self.image = BOOST_SPRITES[self.type]

        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.left = x

        self.countdown = random.randint(3000, 8000)
        self.caught = False

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed

        if self.rect.right < 0 or self.caught:
            self.kill()
