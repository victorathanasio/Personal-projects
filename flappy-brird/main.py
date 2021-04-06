import pygame
from utils.gamesettings import Game_settings
import pygame_menu
from utils.Game import GameLoop
from utils.NEAT import run_ai

WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1200
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
gameIcon = pygame.image.load("Assets/Theme_orig/bird2.png")
pygame.display.set_caption('Flappy BRirds')
pygame.display.set_icon(gameIcon)
file = open("Assets/highscore.txt", "r")
highscore = file.readline()
file.close()

settings = Game_settings()


def start_the_game():
    """ 
    Method that gets the gamemode and sets the game up
    """

    mode = settings.game_settings['Mode']
    if mode == 'Regular':
        play_again = GameLoop(settings.game_settings, window)
        while play_again:
            play_again = GameLoop(settings.game_settings, window)
    elif mode == 'AI':
        run_ai(settings.game_settings, window)
    elif mode == 'Train AI':
        run_ai(settings.game_settings, window)


menu = pygame_menu.Menu(WINDOW_HEIGHT, WINDOW_WIDTH,
                        'Flappy Bird', theme=pygame_menu.themes.THEME_DARK)

menu.add_label('Your max score: {}'.format(highscore), label_id='score')
menu.add_label(' ')
menu.add_button('Play', start_the_game)


menu.add_selector('Difficulty :',
                  [('Normal', 'Normal'), ('Hard', "Hard"), ('Very Hard', "Very Hard"), ('Insane', "Insane"),
                   ('Meme', "Meme"), ('Easy', "Easy")], onchange=settings.set_difficulty)

menu.add_selector('Theme :', [('Original', 'Theme_orig'), ('France', 'Theme_fr'), ("MVP", 'Theme_mvp'),
                              ('Brazil', 'Theme_br'), ('Centrale', 'Theme_cs'), ('Neymar', 'Theme_ney')],
                  onchange=settings.set_theme)
menu.add_selector('Sound Volume:', [('100%', 1.0), ('0%', 0), ('25%', 0.25), ('50%', 0.5), ('75%', 0.75)],
                  onchange=settings.set_sound)
menu.add_selector('Mode :', [('Regular', 'Regular'), ('AI', 'AI'), ('Train AI', 'Train AI')],
                  onchange=settings.set_mode)
menu.add_selector('Speed :', [('Normal', 'Normal'), ('2x', '2x'), ('8x', '8x'), ('Turbo', 'Turbo')],
                  onchange=settings.set_speed)


menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(window)
