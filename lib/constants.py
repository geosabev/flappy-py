import pygame

MENU_BACKGROUND = pygame.image.load('assets/img/menu.png')
DEATH_SCREEN = pygame.image.load('assets/img/death.png')

BACKGROUND = pygame.image.load('assets/img/background.png')
GROUND = pygame.image.load('assets/img/ground.png')
PIPE = pygame.image.load('assets/img/pipe.png')
STONES = [pygame.image.load(
    f'assets/img/stones/stone_{i}.png') for i in range(1, 6)]

SNAKE_SKIN_SHEET_MAPPING = {
    'red': ('assets/img/snakes/red_snake.png', (36, 36)),
    'green': ('assets/img/snakes/green_snake.png', (36, 36)),
    'blue': ('assets/img/snakes/blue_snake.png', (36, 36))
}
HEDGEHOG_SKIN_SHEET_MAPPING = {
    'red': ('assets/img/hedgehogs/red_hedgehog.png', (42, 42)),
    'green': ('assets/img/hedgehogs/green_hedgehog.png', (48, 48)),
    'blue': ('assets/img/hedgehogs/blue_hedgehog.png', (52, 52))
}

BONUS_LIFE = pygame.image.load('assets/img/boosts/bonus_life.png')
SPEED_UP = pygame.image.load('assets/img/boosts/speed_up.png')
SLOW_DOWN = pygame.image.load('assets/img/boosts/slow_down.png')
SHRINK = pygame.image.load('assets/img/boosts/shrink.png')
GROW = pygame.image.load('assets/img/boosts/grow.png')

BOOST_SOUND = 'assets/audio/boost.ogg'
DEATH_SOUND = 'assets/audio/death.ogg'

LOCAL_SCORES_FILE = 'locals/scores.csv'

FONT = 'assets/fonts/FlappyBird.ttf'

SKIN_COLORS = ['red', 'green', 'blue']
BOOST_TYPES = ['BONUS_LIFE', 'SPEED_UP', 'SLOW_DOWN', 'SHRINK', 'GROW']
BOOST_SPRITES = {
    'BONUS_LIFE': BONUS_LIFE,
    'SPEED_UP': SPEED_UP,
    'SLOW_DOWN': SLOW_DOWN,
    'SHRINK': SHRINK,
    'GROW': GROW
}

PIPE_GAPS = [140, 150, 160, 170, 180, 190, 200]

SCROLL_SPEEDS = {
    'easy': 4,
    'medium': 5,
    'hard': 6
}

FPS = 60
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 735
PIPE_GAP = 200
MIN_STONE_X = 250
MIN_BOOST_FREQUENCY = 3000
MAX_BOOST_FREQUENCY = 8000
MIN_STONE_FREQUENCY = 5000
MAX_STONE_FREQUENCY = 10000
MIN_HEDGEHOG_FREQUENCY = 5000
MAX_HEDGEHOG_FREQUENCY = 10000
MIN_PIPE_FREQUENCY = 1000
MAX_PIPE_FREQUENCY = 2500
ENLARGEMENT_COEFFICIENT = 1.25
SHRINKING_COEFFICIENT = 0.75

NO_SCORES_YET_MESSAGE = 'No scores saved yet! Go back and start playing!'
