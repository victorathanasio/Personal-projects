import unittest
import pygame
import os
import Tests.tests_env as T
from utils.bird import Bird

path = os.getcwd()
os.chdir(path + '/..')

T.init()


class Test_bird(unittest.TestCase):
    def test_create_bird(self):
        surf = T.create_surface()
        bird = Bird()
        bird.falling = True
        self.assertEqual((bird.x, bird.y), (200, 200))
        for i in range(len(bird.Bird_imgs)):
            self.assertIsInstance(bird.Bird_imgs[i], pygame.Surface)

        bird.draw(surf)
        self.assertTrue(surf.get_at((bird.x + bird.img.get_width() // 2,
                                     bird.y + bird.img.get_height() // 2)) != T.white)

    def test_bird_move(self):
        bird = Bird()
        bird.falling = True

        # test bird jump does not goes beyond the sealing
        tick = 0
        while tick < 100:
            tick += 1
            bird.jump()
            bird.move()
            self.assertGreater(bird.y, -1)

        # test bird falling does not goes beyond the ground
        tick = 0
        while tick < 100:
            tick += 1
            bird.move()
            self.assertLess(bird.y, 550)

    def test_bird_draw(self):
        os.chdir(path + '/..')
        surf = T.create_surface()
        bird = Bird()
        for i in range(100):
            bird.draw(surf)
            self.assertTrue(surf.get_at((bird.x + bird.img.get_width() // 2,
                                         bird.y + bird.img.get_height() // 2)) != T.white)
        # pygame.image.save(surf, "test_bird_draw.png")


T.end()

if __name__ == '__main__':
    unittest.main()
