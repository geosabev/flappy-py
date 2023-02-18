import pygame
from pygame.locals import *

from lib.constants import PIPE


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, gap, rotate=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = PIPE

        self.rect = self.image.get_rect()

        if rotate:
            self.image = pygame.transform.flip(self.image, False, True)

            self.rect.bottomleft = [x, y - (gap / 2)]
        else:
            self.rect.topleft = [x, y + (gap / 2)]

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed

        if self.rect.right < 0:
            self.kill()
