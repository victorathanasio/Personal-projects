import pygame
import os

from utils.score import Score

local_dir = os.path.dirname(__file__)
file = open(local_dir + "/config.txt", "r")
a = file.readline().split()[-1]
if a == 'False':
    Testing = False
else:
    Testing = True
file.close()

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 40)


class Score_display:

    def __init__(self, score):
        """ 
        Method that initiates the Display of the score using pre-established specifications    
        Input = (Int)
        """
        file = open('Assets/highscore.txt', 'r')
        self.highscore = str(file.readline())
        self.counter = score

    def highscore(self):
        """
        Creates the highscore text to be displayed
        Output = Surface
        """

        self.highscore_text = STAT_FONT.render(
            'Highscore: ' + self.highscore, True, (0, 0, 0))
        return self.highscore_text

    def score(self):
        """
        Creates the score text to be displayed
        Output = Surface
        """

        # PEGAR SCORE FINAL
        counter = self.counter.counter
        self.counter_text = STAT_FONT.render(
            'Score: ' + str(counter), True, (0, 0, 0))
        return self.counter_text

    def restart_button(self):
        """
        Creates the restart button
        Output = Surface
        """

        self.restart_text = STAT_FONT.render('Restart', True, (100, 100, 100))
        return self.restart_text

    def menu_button(self):
        """
        Creates the menu button
        Output = Surface
        """

        self.menu_text = STAT_FONT.render('Menu', True, (100, 100, 100))
        return self.menu_text

    def draw(self, window):
        """
        Displays in the game window the score, the highscore and the options to restart or
        go to the menu after the game ends
        Input = (Window object)
        Output = None or Boolean
        """

        highscore_text = Score_display.highscore(self)
        score_text = Score_display.score(self)
        restart_text = Score_display.restart_button(self)
        menu_text = Score_display.menu_button(self)

        self.x_init = 600 - highscore_text.get_width() // 2

        pygame.draw.rect(window, (0, 0, 0), (self.x_init - 13,
                                             287, highscore_text.get_width() + 26, 216))
        pygame.draw.rect(window, (255, 255, 155), (self.x_init -
                                                   10, 290, highscore_text.get_width() + 20, 210))
        window.blit(highscore_text, (self.x_init, 300))
        window.blit(score_text, (self.x_init, 350))
        window.blit(restart_text, (self.x_init-5, 450))
        window.blit(menu_text, (self.x_init +
                                highscore_text.get_width() + 5 - menu_text.get_width(), 450))

        pygame.display.flip()

        menuAtivo = True
        while menuAtivo or not Testing:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                if evento.type == pygame.MOUSEBUTTONDOWN:

                    if pygame.mouse.get_pos()[0] >= self.x_init and pygame.mouse.get_pos()[
                            0] <= self.x_init + restart_text.get_width() and 450 <= pygame.mouse.get_pos()[
                            1] <= 450 + restart_text.get_height():
                        return True
                    elif pygame.mouse.get_pos()[0] >= self.x_init + highscore_text.get_width() + 5-menu_text.get_width() and \
                        pygame.mouse.get_pos()[
                        0] <= self.x_init + highscore_text.get_width() + 5 and \
                        pygame.mouse.get_pos()[1] >= 450 and pygame.mouse.get_pos()[
                            1] <= 450 + menu_text.get_height():
                        return False
