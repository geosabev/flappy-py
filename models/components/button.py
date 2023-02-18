import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, value, font, base_color, hovering_color, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color

        self.value = value
        self.text = self.font.render(self.value, True, self.base_color)
        self.rect = self.text.get_rect(center=(x, y))

    def update(self, screen):
        screen.blit(self.text, self.rect)

    def check_for_input(self, x, y):
        return x in range(self.rect.left, self.rect.right) and y in range(self.rect.top, self.rect.bottom)

    def change_color(self, x, y):
        if x in range(self.rect.left, self.rect.right) and y in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.value, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.value, True, self.base_color)
