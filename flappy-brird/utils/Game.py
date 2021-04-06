import os

import pygame

from utils.bird import Bird
from utils.ground import Ground
from utils.pipe import Pipes
from utils.radio import Radio
from utils.score import Score
from utils.score_display import Score_display

from Tests.monkey_patcher_game import monkey_patch

local_dir = os.path.dirname(__file__)
file = open(local_dir + "/config.txt", "r")
a = file.readline().split()[-1]
if a == 'False':
    Testing = False
else:
    Testing = True
file.close()

if Testing:
    input_data = [0] * 7


def GameLoop(settings, window):
    """
    Function that runs the gameloop for the user based on given settings
    Input = (dict, Window object)
    Output = None or Boolean
    """

    WINDOW_WIDTH = settings['WINDOW_WIDTH']
    theme = settings['Theme']
    difficulty = settings["Difficulty"]
    clock = pygame.time.Clock()
    running = True
    frame_rate = 60
    frame_skip = 1
    if settings['Speed'] == 'Normal':
        frame_rate = 60
        frame_skip = 1
    elif settings['Speed'] == '2x':
        frame_rate = 120
        frame_skip = 2
    elif settings['Speed'] == '8x':
        frame_rate = 480
        frame_skip = 8
    elif settings['Speed'] == 'Turbo':
        frame_rate = 100000
        frame_skip = 10

    # Initialize

    bird = Bird(theme=theme)
    pipes = Pipes(theme=theme, difficulty=difficulty)
    ground = Ground(theme=theme)
    score = Score(WINDOW_WIDTH)
    radio = Radio(settings)
    score_display = Score_display(score)

    path = os.path.join("Assets/", theme)
    background = pygame.image.load(
        os.path.join(path, "bg_big.png")).convert_alpha()
    window.blit(background, (0, 0))
    time = 0

    while running:
        time += 1
        if difficulty != 'Meme':
            clock.tick(frame_rate)
        else:
            clock.tick(2*frame_rate)

        if Testing:
            bird.falling = True
            if len(pipes.list_next_pipes()) > 0:
                if monkey_patch(bird, pipes.list_next_pipes(), input_data):
                    bird.jump()
                    radio.wing_sound()
        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bird.jump()
                    radio.wing_sound()
                if event.type == pygame.QUIT:
                    running = False

        # collision

        for pipe in pipes:
            if pipe.collision(bird):
                bird.falling=True
                bird.alive = False
                running = False
                radio.hit_sound()
                radio.die_sound()

        if ground.collide(bird):
            bird.alive = False
            running = False
            radio.hit_sound()
            radio.die_sound()

        if score.count(bird, pipes):
            radio.score_sound()

        # movement
        bird.move()
        pipes.move()
        ground.move()

        # Pipe management
        pipes.delete_old_pipes()
        pipes.create_pipe(time)

        # draw
        if time % frame_skip == 0:
            window.blit(background, (0, 0))
            pipes.draw(window)
            score.draw(window)
            bird.draw(window)
            ground.draw(window)

        # Saving score
        if not running:
            score.save_score()

        # pygame.draw.rect(window, 'black', [pipes.get_next_pipe().x, pipes.get_next_pipe().gap_pos, 30, 30])
        pygame.display.flip()

    delay_to_end = 50
    while delay_to_end > 0:
        delay_to_end -= 1
        clock.tick(60)

        bird.move()

        window.blit(background, (0, 0))
        pipes.draw(window)
        score.draw(window)
        bird.draw(window)
        ground.draw(window)
        if bird.y > 540:
            play_again = score_display.draw(window)
            if play_again:
                return True
            else:
                break
        pygame.display.flip()

    # end main loop
    return False
