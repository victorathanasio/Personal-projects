import unittest
import os
import Tests.tests_env as T

T.init()

from utils.NEAT import run_ai
from utils.gamesettings import Game_settings

path = os.getcwd()
os.chdir(path + '/..')

settings = Game_settings().game_settings
settings['Speed'] = 'Turbo'


class Test_gameloop_AI(unittest.TestCase):
    def test_game_loop_AI(self):
        settings['Mode'] = 'AI'
        self.assertTrue(run_ai(settings, T.window))
        pass

    def test_game_loop_train_AI(self):
        settings['Mode'] = 'Train AI'
        self.assertTrue(run_ai(settings, T.window))
        pass


T.end()

if __name__ == '__main__':
    unittest.main()
