import csv
import pygame
from lib.constants import BONUS_LIFE, FONT, LOCAL_SCORES_FILE, SCREEN_WIDTH


def get_current_scores():
    '''
    Reads existing scores saved locally in a CSV file.

    If the file does not exist, it creates it with appropriate headers.
    '''
    current_scores = []
    with open(LOCAL_SCORES_FILE, 'a+', newline='') as csvfile:
        csvfile.seek(0)

        reader = csv.reader(csvfile, delimiter=',')
        for score in reader:
            current_scores.append(score)

        if len(current_scores) == 0:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Player', 'Score'])

    return current_scores


def add_new_score(player, points):
    '''
    Appends new score at end of local CSV file.

    If the file does not exist, it creates it with appropriate headers.
    '''
    current_scores = []
    with open(LOCAL_SCORES_FILE, 'a+', newline='') as csvfile:
        csvfile.seek(0)

        reader = csv.reader(csvfile, delimiter=',')
        for score in reader:
            current_scores.append(score)

        writer = csv.writer(csvfile, delimiter=',')
        if len(current_scores) == 0:
            writer.writerow(['Player', 'Score'])
        else:
            writer.writerow([player, points])


def get_font(size):
    '''
    Returns an instance of a font with specific size.

    Takes path to the font and wanted size as arguments.
    '''
    return pygame.font.Font(FONT, size)


def draw_text(screen, value, font_style, color, x, y):
    '''
    Renders a given value on the screen.

    Takes value, style, color and coordinates as arguments.
    '''
    text = font_style.render(value, True, color)
    text_rect = text.get_rect(center=(x, y))

    screen.blit(text, text_rect)


def entity_is_due(current_time, last_entity, next_entity):
    '''
    Checks if a new entity could be generated based on current time.
    '''
    return current_time - last_entity > next_entity


def can_generate_entity(x, y, sprite_group):
    '''
    Checks if an entity with center (x, y) would collide with a sprite group.
    '''
    point = pygame.sprite.Sprite()
    point.rect = pygame.Rect(x, y, 1, 1)

    collisions = pygame.sprite.spritecollide(point, sprite_group, False)

    return len(collisions) == 0


def play_sound_effect(sound_effect):
    '''
    Plays a sound effect specified by a path to it.
    '''
    pygame.mixer.init()
    pygame.mixer.music.load(sound_effect)
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()


def print_lifes(screen, lifes_count):
    heart_image = pygame.transform.scale(BONUS_LIFE, (16, 16))
    deviation = (lifes_count - 1) * 10
    for _ in range(lifes_count):
        heart_image_rect = heart_image.get_rect(
            center=((SCREEN_WIDTH / 2) - deviation, 80))
        screen.blit(heart_image, heart_image_rect)
        deviation -= 20
