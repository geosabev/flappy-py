import pygame


class SpriteSheet():
    def __init__(self, sheet):
        self.sheet = pygame.image.load(sheet[0]).convert_alpha()
        self.w, self.h = sheet[1]

    def get_sheet(self):
        '''
        Returns whole sprite sheet.
        '''
        return self.sheet

    def get_image(self, frame, scale, color=(0, 0, 0)):
        '''
        Returns a single sprite of the sheet that can be scaled.

        Accepts index of frame (starting from 0), scale and color to remove.
        '''
        image = pygame.Surface((self.w, self.h))
        image.blit(self.sheet, (0, 0), ((frame * self.w), 0, self.w, self.h))
        image = pygame.transform.scale(image, (self.w * scale, self.h * scale))
        image.set_colorkey(color)

        return image

    def get_count(self):
        '''
        Returns number of images based on width of each individual sprite.
        '''
        return self.sheet.get_width() / self.w
