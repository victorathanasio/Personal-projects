import unittest
import os
import Tests.tests_env as T
T.init()

from utils.Game import GameLoop
from utils.gamesettings import Game_settings

path = os.getcwd()
os.chdir(path + '/..')



settings = Game_settings().game_settings
settings['Speed'] = 'Turbo'


class Test_gameloop(unittest.TestCase):
    def test_game_loop(self):
        self.assertFalse(GameLoop(settings, T.window))
        pass

T.end()

if __name__ == '__main__':
    unittest.main()


