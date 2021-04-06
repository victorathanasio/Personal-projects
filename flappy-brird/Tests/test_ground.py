import unittest
import pygame
import os
import Tests.tests_env as T
from utils.ground import Ground

path = os.getcwd()
os.chdir(path + '/..')

T.init()


class Test_bird(unittest.TestCase):
    def test_ground_draw(self):
        surf = T.create_surface()
        ground = Ground()
        ground.draw(surf)
        assert surf.get_at((T.WINDOW_HEIGHT, T.WINDOW_WIDTH // 2)) != T.white
        # pygame.image.save(surf, "test_ground_draw.png")

    def test_ground_move(self):
        surf = T.create_surface()
        ground = Ground()
        initial_position = (ground.x_black, ground.x_white)
        remaining_time = 10
        while remaining_time > 0:
            ground.move()
            remaining_time -= 1
        ground.draw(surf)
        assert initial_position != (ground.x_black, ground.x_white)
        # pygame.image.save(surf, "test_ground_move.png")


T.end()

if __name__ == '__main__':
    unittest.main()
