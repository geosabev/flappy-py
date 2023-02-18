import pygame


class SpriteSheet():
    def __init__(self, sheet):
        self.sheet = pygame.image.load(sheet[0]).convert_alpha()
        self.w, self.h = sheet[1]

    def get_sheet(self):
        return self.sheet

    def get_image(self, frame, scale, color=(0, 0, 0)):
        image = pygame.Surface((self.w, self.h))
        image.blit(self.sheet, (0, 0), ((frame * self.w), 0, self.w, self.h))
        image = pygame.transform.scale(image, (self.w * scale, self.h * scale))
        image.set_colorkey(color)

        return image

    def get_count(self):
        return self.sheet.get_width() / self.w
