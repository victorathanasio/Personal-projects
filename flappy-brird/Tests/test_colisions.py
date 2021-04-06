import unittest
import pygame
import os
import Tests.tests_env as T
from utils.bird import Bird
from utils.pipe import Pipe
from utils.ground import Ground

# path = os.getcwd()
# os.chdir(path + '/..')

T.init()


class Test_bird(unittest.TestCase):
    def test_collision_ground(self):
        surf = T.create_surface()
        bird = Bird()
        ground = Ground()
        ground.draw(surf)
        bird.falling = True
        bird.vel = -1
        remaining_time = 50
        while remaining_time > 0:
            bird.move()
            remaining_time -= 1
        bird.draw(surf)
        assert ground.collide(bird) == True
        # pygame.image.save(surf, "test_collision_ground.png")

    def test_collision_pipe(self):
        surf = T.create_surface()
        bird1 = Bird()
        bird1.y = 50
        bird2 = Bird()
        bird2.y = 500
        pipe_distance = T.WINDOW_WIDTH / 6
        pipe = Pipe(x=int(pipe_distance * 2))
        remaining_time = 50
        collisions = [False, False]
        while remaining_time > 0:
            if pipe.collision(bird1):
                collisions[0] = True
            if pipe.collision(bird2):
                collisions[1] = True
            pipe.move()
            remaining_time -= 1
        bird1.draw(surf)
        bird2.draw(surf)
        pipe.draw(surf)
        assert collisions == [True, True]
        # pygame.image.save(surf, "test_collision_pipe.png")


T.end()

if __name__ == '__main__':
    unittest.main()
