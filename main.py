import random
import sys
import pygame
from pygame.locals import *
from lib.constants import *
from lib.utils import *
from models.snake import Snake
from models.pipe import Pipe
from models.hedgehog import Hedgehog
from models.spritesheet import SpriteSheet
from models.stone import Stone
from models.boost import Boost
from models.components.button import Button
from models.components.text_field import TextField


pygame.init()
game_clock = pygame.time.Clock()


def main_menu(screen, player, skin, difficulty):
    '''
    Display the main menu.

    Navigates to the other screens.
    '''
    play_button = Button('Play', get_font(
        75), 'deepskyblue4', 'deepskyblue3', SCREEN_WIDTH / 2, 250)
    options_button = Button('Options', get_font(
        75), 'deepskyblue4', 'deepskyblue3', SCREEN_WIDTH / 2, 350)
    scores_button = Button('Scores', get_font(
        75), 'deepskyblue4', 'deepskyblue3', SCREEN_WIDTH / 2, 450)
    quit_button = Button('Quit', get_font(
        75), 'deepskyblue4', 'deepskyblue3', SCREEN_WIDTH / 2, 550)

    while True:
        screen.blit(MENU_SCREEN_BACKGROUND, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        draw_text(screen, 'Flappy Py', get_font(
            100), 'orange', SCREEN_WIDTH/2, 125)

        for button in [play_button, options_button, scores_button, quit_button]:
            button.change_color(mouse_x, mouse_y)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_click(mouse_x, mouse_y):
                    play(screen, player, skin, difficulty)

                if options_button.check_for_click(mouse_x, mouse_y):
                    options(screen, player, skin, difficulty)

                if scores_button.check_for_click(mouse_x, mouse_y):
                    scores(screen, player, skin, difficulty)

                if quit_button.check_for_click(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def play(screen, player, skin, difficulty):
    '''
    Execute the main game logic.
    '''
    score = 0

    boost_countdown = 0
    boost_start_time = 0

    ground_scroll = 0
    scroll_speed = SCROLL_SPEEDS[difficulty]
    scroll_coefficient = 1

    already_under_pipe = False

    next_pipe = random.randint(MIN_PIPE_FREQUENCY, MAX_PIPE_FREQUENCY)
    next_stone = random.randint(
        MIN_STONE_FREQUENCY, MAX_STONE_FREQUENCY)
    next_hedgehog = random.randint(
        MIN_HEDGEHOG_FREQUENCY, MAX_HEDGEHOG_FREQUENCY)
    next_boost = random.randint(MIN_BOOST_FREQUENCY, MAX_BOOST_FREQUENCY)

    last_pipe = next_pipe
    last_stone = next_stone
    last_hedgehog = next_hedgehog
    last_boost = next_boost

    pipe_group = pygame.sprite.Group()
    stone_group = pygame.sprite.Group()
    hedgehog_group = pygame.sprite.Group()
    boost_group = pygame.sprite.Group()

    snake = Snake(200, SCREEN_HEIGHT / 2, skin)

    while True:
        game_clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        time_since_boost = current_time - boost_start_time

        screen.blit(GAME_SCREEN_BACKGROUND, (0, 0))

        for group in [pipe_group, stone_group, hedgehog_group, boost_group]:
            group.draw(screen)

        screen.blit(
            GROUND, (ground_scroll, GAME_SCREEN_BACKGROUND.get_height()))

        screen.blit(snake.image, snake.rect)
        snake.update()

        # Handling pipe collisions
        if len(pipe_group) > 0:
            hit_pipes = pygame.sprite.spritecollide(snake, pipe_group, False)
            for pipe in hit_pipes:
                if snake.get_lifes() > 1:
                    pipe.kill()
                    snake.lose_life()
                else:
                    snake.die()
                    play_sound_effect(DEATH_SOUND)

            incoming_pipe = pipe_group.sprites()[0]

            if snake.is_under_pipe(incoming_pipe) and not already_under_pipe:
                already_under_pipe = True

            if already_under_pipe and snake.has_passed_pipe(incoming_pipe):
                score += 1
                already_under_pipe = False

        # Handling stone and hedgehog collisions
        for group in [stone_group, hedgehog_group]:
            if len(group) > 0:
                incoming_entity = group.sprites()[0]

                if snake.has_hit_entity(incoming_entity):
                    if snake.get_lifes() > 1:
                        incoming_entity.kill()
                        snake.lose_life()
                    else:
                        snake.die()
                        play_sound_effect(DEATH_SOUND)

        # Remove boost if over
        if snake.has_active_boost():
            if time_since_boost >= boost_countdown:
                snake.deactivate_boost()
                boost_countdown = 0
                scroll_coefficient = 1

        # Handling boost collisions
        if len(boost_group) > 0:
            incoming_boost = boost_group.sprites()[0]

            if snake.has_hit_entity(incoming_boost):
                if incoming_boost.type == 'SLOW_DOWN':
                    scroll_coefficient = 0.75
                elif incoming_boost.type == 'SPEED_UP':
                    scroll_coefficient = 1.25

                snake.activate_boost(incoming_boost)

                play_sound_effect(BOOST_SOUND)

                boost_countdown = incoming_boost.countdown
                boost_start_time = current_time

                incoming_boost.kill()

        # Handling ground collisions
        if snake.has_hit_ground():
            if snake.get_lifes() > 1:
                snake.lose_life()
                snake.fly_to_center()
            else:
                snake.die()
                play_sound_effect(DEATH_SOUND)

        # Creation of entities
        if not snake.is_dead() and snake.is_flying():
            # Pipes
            if entity_is_due(current_time, last_pipe, next_pipe):
                pipe_gap = random.choice(PIPE_GAPS)
                height_deviation = random.randint(-150, 100)
                y = (SCREEN_HEIGHT / 2) + height_deviation

                bottom_pipe = Pipe(SCREEN_WIDTH, y, pipe_gap)
                top_pipe = Pipe(SCREEN_WIDTH, y, pipe_gap, True)

                pipe_group.add(bottom_pipe)
                pipe_group.add(top_pipe)

                last_pipe = current_time
                next_pipe = random.randint(
                    MIN_PIPE_FREQUENCY, MAX_PIPE_FREQUENCY)

            # Stones
            if entity_is_due(current_time, last_stone, next_stone):
                x = random.randint(MIN_STONE_X, SCREEN_WIDTH)

                if can_generate_entity(x, 1, pipe_group):
                    stone = Stone(x)

                    stone_group.add(stone)

                    last_stone = current_time
                    next_stone = random.randint(
                        MIN_STONE_FREQUENCY, MAX_STONE_FREQUENCY)

            # Hedgehogs
            if entity_is_due(current_time, last_hedgehog, next_hedgehog):
                height_deviation = random.randint(-200, 150)
                y = (SCREEN_HEIGHT / 2) + height_deviation

                if can_generate_entity(SCREEN_WIDTH, y, pipe_group):
                    hedgehog = Hedgehog(SCREEN_WIDTH, y)

                    hedgehog_group.add(hedgehog)

                    last_hedgehog = current_time
                    next_hedgehog = random.randint(
                        MIN_HEDGEHOG_FREQUENCY, MAX_HEDGEHOG_FREQUENCY)

            # Boosts
            if entity_is_due(current_time, last_boost, next_boost) and len(boost_group) == 0 and not snake.has_active_boost():
                height_deviation = random.randint(-250, 150)
                y = (SCREEN_HEIGHT / 2) + height_deviation

                if can_generate_entity(SCREEN_HEIGHT, y, pipe_group):
                    boost = Boost(SCREEN_HEIGHT, y)

                    boost_group.add(boost)

                    last_boost = current_time
                    next_boost = random.randint(
                        MIN_BOOST_FREQUENCY, MAX_BOOST_FREQUENCY)

            # Scrolling background effect
            ground_scroll -= scroll_speed * scroll_coefficient
            if abs(ground_scroll) > 70:
                ground_scroll = 0

            pipe_group.update(scroll_speed * scroll_coefficient)
            stone_group.update(scroll_speed * scroll_coefficient)
            hedgehog_group.update(scroll_speed * scroll_coefficient)
            boost_group.update(scroll_speed * scroll_coefficient)

        if snake.is_dead():
            death_screen(screen, score, player, skin, difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not snake.is_flying() and not snake.is_dead():
                game_started = pygame.time.get_ticks()

                snake.flying = True

                last_pipe = game_started + next_pipe
                last_stone = game_started + next_stone
                last_hedgehog = game_started + next_hedgehog
                last_boost = game_started + next_boost

        draw_text(screen, f'{score}', get_font(55), 'black',
                  SCREEN_WIDTH / 2, 50)

        print_lifes(screen, snake.get_lifes())

        pygame.display.update()


def options(screen, player, skin, difficulty):
    '''
    Display the settings menu.

    Modifies username, skin and speed level.
    '''
    selected_name = player
    selected_skin = skin
    selected_difficulty = difficulty

    skins = {color: SpriteSheet(
        SNAKE_SKIN_SHEET_MAPPING[color]) for color in SKIN_COLORS}
    current_skin = skins[selected_skin]
    skin_idx = SKIN_COLORS.index(selected_skin)
    image_idx = 0
    counter = 0

    text_field = TextField(selected_name, get_font(
        40), 'white', 'white', 'grey', SCREEN_WIDTH/2, 270)

    previous_button = Button('Prev', get_font(
        30), 'white', 'grey', SCREEN_WIDTH / 2 - 80, 390)
    next_button = Button('Next', get_font(
        30), 'white', 'grey', SCREEN_WIDTH / 2 + 80, 390)
    easy_button = Button('Easy', get_font(
        30), 'white', 'grey', SCREEN_WIDTH / 2 - 80, 500)
    medium_button = Button('Medium', get_font(
        30), 'white', 'grey', SCREEN_WIDTH / 2, 500)
    hard_button = Button('Hard', get_font(
        30), 'white', 'grey', SCREEN_WIDTH / 2 + 80, 500)
    save_button = Button('Save changes', get_font(
        60), 'deepskyblue4', 'deepskyblue3', SCREEN_WIDTH / 2, 600)
    cancel_button = Button('Discard changes', get_font(
        60), 'deepskyblue4', 'deepskyblue3', SCREEN_WIDTH / 2, 650)

    # Used for drawing border around selected difficulty without if/elif/else
    button_difficulty_mapping = {
        'easy': easy_button,
        'medium': medium_button,
        'hard': hard_button
    }

    while True:
        screen.blit(MENU_SCREEN_BACKGROUND, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        current_name = text_field.get_value()
        current_skin = skins[selected_skin]
        current_difficulty = button_difficulty_mapping[selected_difficulty]

        counter += 1
        flap_cooldown = 3
        if counter > flap_cooldown:
            counter = 0
            image_idx += 1

            if image_idx >= current_skin.get_count() - 1:
                image_idx = 0

        draw_text(screen, 'Options', get_font(
            100), 'orange', SCREEN_WIDTH/2, 125)
        draw_text(screen, 'Player name', get_font(
            50), 'deepskyblue4', SCREEN_WIDTH / 2, 225)
        draw_text(screen, 'Skin', get_font(50),
                  'deepskyblue4', SCREEN_WIDTH / 2, 340)
        draw_text(screen, 'Difficulty', get_font(50),
                  'deepskyblue4', SCREEN_WIDTH/2, 455)

        skin_frame = current_skin.get_image(image_idx, 1)
        skin_frame_rect = skin_frame.get_rect(center=(SCREEN_WIDTH / 2, 390))
        pygame.draw.rect(screen, 'white',
                         pygame.Rect.inflate(skin_frame_rect, 10, 5), 2)
        screen.blit(skin_frame, skin_frame_rect)

        pygame.draw.rect(screen, 'white',
                         pygame.Rect.inflate(current_difficulty.rect, 10, 5), 2)

        for button in [previous_button, next_button, easy_button, medium_button, hard_button, save_button, cancel_button]:
            button.change_color(mouse_x, mouse_y)
            button.update(screen)

        text_field.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if text_field.is_active():
                    if event.key == pygame.K_BACKSPACE:
                        text_field.set_value(current_name[:-1])
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        text_field.disable()
                    else:
                        text_field.set_value(current_name + event.unicode)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_field.check_for_click(mouse_x, mouse_y):
                    text_field.activate()
                else:
                    text_field.disable()

                if previous_button.check_for_click(mouse_x, mouse_y):
                    skin_idx -= 1

                    if skin_idx < 0:
                        skin_idx = len(SKIN_COLORS) - 1

                    selected_skin = SKIN_COLORS[skin_idx]

                if next_button.check_for_click(mouse_x, mouse_y):
                    skin_idx += 1

                    if skin_idx >= len(SKIN_COLORS):
                        skin_idx = 0

                    selected_skin = SKIN_COLORS[skin_idx]

                if easy_button.check_for_click(mouse_x, mouse_y):
                    selected_difficulty = 'easy'

                if medium_button.check_for_click(mouse_x, mouse_y):
                    selected_difficulty = 'medium'

                if hard_button.check_for_click(mouse_x, mouse_y):
                    selected_difficulty = 'hard'

                if save_button.check_for_click(mouse_x, mouse_y):
                    main_menu(screen, text_field.get_value(), selected_skin,
                              selected_difficulty)

                if cancel_button.check_for_click(mouse_x, mouse_y):
                    main_menu(screen, player, skin, difficulty)

        pygame.display.update()


def scores(screen, player, skin, difficulty):
    '''
    Display the leaderboard.

    Reads data from local text file containing the scores.
    '''
    current_scores = get_current_scores()

    menu_button = Button('Back to Main Menu', get_font(
        70), 'deepskyblue4', 'deepskyblue3', SCREEN_WIDTH / 2, 600)

    while True:
        screen.blit(MENU_SCREEN_BACKGROUND, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        draw_text(screen, 'Scores', get_font(
            100), 'orange', SCREEN_WIDTH/2, 125)

        if len(current_scores) < 2:
            draw_text(screen, NO_SCORES_YET_MESSAGE, get_font(
                40), 'black', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        else:
            scores_only = current_scores[1:]
            scores_only.sort(key=lambda x: int(x[1]), reverse=True)

            for idx, score in enumerate(scores_only[0:9]):
                player = get_font(40).render(f'{score[0]}', True, 'black')
                player_rect = player.get_rect(
                    center=(SCREEN_WIDTH / 2 - 90, 200 + (idx + 1) * 35))

                value = get_font(40).render(f'{score[1]}', True, 'black')
                value_rect = value.get_rect(
                    center=(SCREEN_WIDTH / 2 + 90, 200 + (idx + 1) * 35))

                screen.blit(player, player_rect)
                screen.blit(value, value_rect)

        menu_button.change_color(mouse_x, mouse_y)
        menu_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.check_for_click(mouse_x, mouse_y):
                    main_menu(screen, player, skin, difficulty)

        pygame.display.update()


def death_screen(screen, points, player, skin, difficulty):
    '''
    Display Game Over screen.

    Restarts game, redirects to main menu or exits.
    '''
    add_new_score(player, points)

    correct_form = 'points' if points != 1 else 'point'

    restart_button = Button('Try again', get_font(
        70), 'orange', 'orange4', SCREEN_WIDTH / 2, 300)
    menu_button = Button('Back to Main Menu', get_font(
        70), 'orange', 'orange4', SCREEN_WIDTH / 2, 400)
    quit_button = Button('Quit', get_font(
        70), 'orange', 'orange4', SCREEN_WIDTH / 2, 500)

    while True:
        screen.blit(DEATH_SCREEN_BACKGROUND, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        draw_text(screen, 'Game Over', get_font(
            100), 'white', SCREEN_WIDTH/2, 150)
        draw_text(screen, f'You scored {points} {correct_form}.', get_font(
            50), 'grey', SCREEN_WIDTH/2, 200)

        for button in [restart_button, menu_button, quit_button]:
            button.change_color(mouse_x, mouse_y)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.check_for_click(mouse_x, mouse_y):
                    play(screen, player, skin, difficulty)

                if menu_button.check_for_click(mouse_x, mouse_y):
                    main_menu(screen, player, skin, difficulty)

                if quit_button.check_for_click(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    pygame.display.set_caption('Flappy Py')
    display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    main_menu(display_screen, 'Player 1', 'green', 'easy')
