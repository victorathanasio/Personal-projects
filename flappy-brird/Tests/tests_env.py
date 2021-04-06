from pytest import *
import os
import pygame
from utils.bird import Bird
from utils.ground import Ground
from utils.pipe import Pipes, Pipe
from utils.score import Score


# WINDOW_HEIGHT = 700
# WINDOW_WIDTH = 1200
#
# STAT_FONT = pygame.font.SysFont("comicsans", 50)
# theme = "Theme_orig"
# difficulty = 'Normal'
# clock = pygame.time.Clock()
# window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#
# black = pygame.Color('black')
# white = pygame.Color('white')

def end():
    local_dir = os.path.dirname(__file__)
    file1 = open(local_dir[:-5] + "utils/config.txt", "w")
    file1.write('Testing = False')
    file1.close()


def init():
    global WINDOW_HEIGHT
    global WINDOW_WIDTH
    global white
    global window
    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 1200

    pygame.init()
    pygame.font.init()

    STAT_FONT = pygame.font.SysFont("comicsans", 50)
    theme = "Theme_orig"
    difficulty = 'Normal'
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    black = pygame.Color('black')
    white = pygame.Color('white')

    local_dir = os.path.dirname(__file__)
    file1 = open(local_dir[:-5] + "utils/config.txt", "w")
    file1.write('Testing = True')
    file1.close()


def create_surface():
    surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    surf.fill(white)
    return surf
#
#

#


#




# test_bird_draw()
# test_bird_move()
# test_bird_jump()
# test_pipe_draw()
# test_pipe_move_left()
# test_ground_draw()
# test_ground_move()
# test_collision_ground()
# test_collision_pipe()
# test_score_draw()
# test_score_count()
# test_pipe_move_up()
# test_pipe_move_down()
# test_pipe_close_gap()
# test_pipe_open_gap()
