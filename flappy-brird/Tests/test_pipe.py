import unittest
import pygame
import os
import Tests.tests_env as T
from utils.pipe import Pipe

path = os.getcwd()
os.chdir(path + '/..')

T.init()


class Test_bird(unittest.TestCase):
    def test_pipe_draw(self):
        surf = T.create_surface()
        pipe_distance = T.WINDOW_WIDTH / 6
        pipe = Pipe(x=pipe_distance * 2)
        top_coord = (int(pipe.x) + pipe.top_img.get_width() // 2,
                     20)
        bottom_coord = (int(pipe.x) + pipe.top_img.get_width() // 2,
                        T.WINDOW_HEIGHT - 20)
        pipe.draw(surf)
        assert surf.get_at(top_coord) != T.white
        assert surf.get_at(bottom_coord) != T.white
        # pygame.image.save(surf, "test_pipe_draw.png")

    def test_pipe_move_left(self):
        surf = T.create_surface()
        pipe_distance = T.WINDOW_WIDTH / 6
        pipe = Pipe(x=pipe_distance * 2)
        X0 = pipe.x
        remaining_time = 50
        while remaining_time > 0:
            pipe.move()
            remaining_time -= 1
        pipe.draw(surf)
        assert X0 != pipe.x
        # pygame.image.save(surf, "test_pipe_move_left.png")

    def test_pipe_open_gap(self):
        surf = T.create_surface()
        pipe_distance = T.WINDOW_WIDTH / 6
        pipe = Pipe(x=pipe_distance * 2, difficulty='Normal')
        d = abs(pipe.top - pipe.bottom)
        remaining_time = 50
        pipe.draw(surf)
        while remaining_time > 0:
            pipe.change_gap_open()
            pipe.move()
            remaining_time -= 1
        pipe.draw(surf)
        assert d < abs(pipe.top - pipe.bottom)

    def test_pipe_close_gap(self):
        surf = T.create_surface()
        pipe_distance = T.WINDOW_WIDTH / 6
        pipe = Pipe(x=pipe_distance * 2, difficulty='Normal')
        d = abs(pipe.top - pipe.bottom)
        remaining_time = 50
        pipe.draw(surf)
        while remaining_time > 0:
            pipe.change_gap_close()
            pipe.move()
            remaining_time -= 1
        pipe.draw(surf)
        assert d > abs(pipe.top - pipe.bottom)
        # pygame.image.save(surf, "test_pipe_close_gap.png")

    def test_pipe_move_up(self):
        surf = T.create_surface()
        pipe_distance = T.WINDOW_WIDTH / 6
        pipe = Pipe(x=pipe_distance * 2)
        initial_position = (pipe.top, pipe.bottom)
        remaining_time = 10
        pipe.draw(surf)
        while remaining_time > 0:
            pipe.move_up()
            pipe.move()
            remaining_time -= 1
        pipe.draw(surf)
        assert initial_position[0] > pipe.top and initial_position[1] > pipe.bottom
        # pygame.image.save(surf, "test_pipe_move_up.png")

    def test_pipe_move_down(self):
        surf = T.create_surface()
        pipe_distance = T.WINDOW_WIDTH / 6
        pipe = Pipe(x=pipe_distance * 2)
        initial_position = (pipe.top, pipe.bottom)
        remaining_time = 10
        pipe.draw(surf)
        while remaining_time > 0:
            pipe.move_down()
            pipe.move()
            remaining_time -= 1
        pipe.draw(surf)
        assert initial_position[0] < pipe.top and initial_position[1] < pipe.bottom
        # pygame.image.save(surf, "test_pipe_move_down.png")


T.end()

if __name__ == '__main__':
    unittest.main()
