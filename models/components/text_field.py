import pygame


class TextField(pygame.sprite.Sprite):
    def __init__(self, value, font, text_color, active_border_color, disabled_border_color, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.font = font
        self.text_color = text_color
        self.active_border_color = active_border_color
        self.disabled_border_color = disabled_border_color
        self.border_color = self.disabled_border_color

        self.active = False
        self.value = value
        self.x = x
        self.y = y

        self.text = self.font.render(self.value, True, self.text_color)
        self.rect = self.text.get_rect(center=(x, y))

    def update(self, screen):
        screen.blit(self.text, self.rect)
        pygame.draw.rect(screen, self.border_color,
                         pygame.Rect.inflate(self.rect, 10, 5), 2)

    def get_value(self):
        return self.value

    def set_value(self, text):
        self.value = text

        self.text = self.font.render(
            self.value, True, self.text_color)
        self.rect = self.text.get_rect(center=(self.x, self.y))

    def check_for_click(self, x, y):
        return x in range(self.rect.left, self.rect.right) and y in range(self.rect.top, self.rect.bottom)

    def change_border_color(self):
        if self.active:
            self.border_color = self.active_border_color
        else:
            self.border_color = self.disabled_border_color

    def activate(self):
        self.active = True
        self.change_border_color()

    def disable(self):
        self.active = False
        self.change_border_color()

    def is_active(self):
        return self.active
