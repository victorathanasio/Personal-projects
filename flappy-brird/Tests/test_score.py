import unittest
import pygame
import os
import Tests.tests_env as T
from utils.bird import Bird
from utils.pipe import Pipe
from utils.score import Score

path = os.getcwd()
os.chdir(path + '/..')

T.init()


class Test_bird(unittest.TestCase):
    def test_score_draw(self):
        surf = T.create_surface()
        score = Score(T.WINDOW_WIDTH)
        score.draw(surf)
        assert surf.get_at(
            (T.WINDOW_WIDTH - score.score_design.get_width(), 10 + 25)) != T.white
        # pygame.image.save(surf, "test_score_draw.png")

    def test_score_count(self):
        surf = T.create_surface()
        bird = Bird()
        bird.y = 50
        pipe_distance = T.WINDOW_WIDTH / 6
        pipe = [Pipe(x=int(pipe_distance * 2))]
        score = Score(T.WINDOW_WIDTH)
        remaining_time = 70
        while remaining_time > 0:
            score.count(bird, pipe)
            pipe[0].move()
            remaining_time -= 1
        bird.draw(surf)
        pipe[0].draw(surf)
        score.draw(surf)
        assert score.counter > 0
        # pygame.image.save(surf, "test_score_count.png")


T.end()

if __name__ == '__main__':
    unittest.main()
