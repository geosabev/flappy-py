import pygame
from lib.constants import ENLARGEMENT_COEFFICIENT, SHRINKING_COEFFICIENT, GAME_SCREEN_BACKGROUND, SNAKE_SKIN_SHEET_MAPPING
from models.spritesheet import SpriteSheet


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y, skin):
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = SpriteSheet(SNAKE_SKIN_SHEET_MAPPING[skin])
        self.sprite_height = self.sprite_sheet.get_sheet().get_height()

        self.scale_coefficient = 1

        self.index = 0
        self.counter = 0

        self.lifes = 1

        self.speed = 0.5
        self.velocity = 0

        self.dead = False
        self.flying = False
        self.has_boost = False
        self.pressed = False

        self.image = self.sprite_sheet.get_image(
            self.index, self.scale_coefficient)

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        if self.flying:
            self.velocity += self.speed

            if self.velocity > 8.5:
                self.velocity = 8.5

            if self.rect.top < 0:
                self.rect.y = 0

            if self.rect.bottom < 576:
                self.rect.y += int(self.velocity)

        if not self.dead:
            if pygame.mouse.get_pressed()[0] == 1 and not self.pressed:
                self.pressed = True
                self.velocity = -10

            if pygame.mouse.get_pressed()[0] == 0:
                self.pressed = False

            self.counter += 1
            flap_cooldown = 6

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1

                if self.index >= self.sprite_sheet.get_count() - 1:
                    self.index = 0

            self.image = self.sprite_sheet.get_image(
                self.index, self.scale_coefficient)

            self.image = pygame.transform.rotate(
                self.image, self.velocity * -2)
        else:
            self.image = pygame.transform.rotate(self.image, -90)

    def update_rect_size(self):
        self.rect.w = self.sprite_height * self.scale_coefficient
        self.rect.h = self.sprite_height * self.scale_coefficient

    def get_bonus_life(self):
        self.lifes += 1

    def shrink(self):
        self.scale_coefficient = SHRINKING_COEFFICIENT
        self.update_rect_size()

    def grow(self):
        self.scale_coefficient = ENLARGEMENT_COEFFICIENT
        self.update_rect_size()

    def reset(self):
        self.scale_coefficient = 1
        self.update_rect_size()

    def activate_boost(self, boost):
        self.has_boost = True

        if boost.type == 'BONUS_LIFE':
            self.get_bonus_life()
        elif boost.type == 'GROW':
            self.grow()
        elif boost.type == 'SHIRNK':
            self.shrink()

    def deactivate_boost(self):
        self.has_boost = False

        self.reset()

    def has_active_boost(self):
        return self.has_boost

    def has_hit_ground(self):
        return self.rect.bottom >= GAME_SCREEN_BACKGROUND.get_height()

    def is_under_pipe(self, pipe):
        return self.rect.left > pipe.rect.left and self.rect.left < pipe.rect.right

    def has_passed_pipe(self, pipe):
        return self.rect.left > pipe.rect.right

    def has_hit_entity(self, entity):
        return pygame.sprite.collide_rect(self, entity)

    def get_lifes(self):
        return self.lifes

    def lose_life(self):
        self.lifes -= 1

    def die(self):
        self.dead = True
        self.flying = False

    def fly_to_center(self):
        self.rect.centery = GAME_SCREEN_BACKGROUND.get_height() / 2

    def is_dead(self):
        return self.dead

    def is_flying(self):
        return self.flying
