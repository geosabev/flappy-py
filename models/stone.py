import random
import pygame

from lib.constants import STONES


class Stone(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)

        stone_image = random.choice(STONES)
        scaling_factor = random.uniform(0.5, 1)

        self.width = stone_image.get_width() * scaling_factor
        self.height = stone_image.get_height() * scaling_factor

        self.image = pygame.transform.scale(
            stone_image, (self.width, self.height))

        self.falling_speed = random.randint(5, 7)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = 0

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed

        if self.rect.bottom < 576:
            self.rect.y += self.falling_speed

        if self.rect.right < 0:
            self.kill()
