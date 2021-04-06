import pygame
import os

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Score:
    def __init__(self, WIDTH):
        """ 
        Method that initiates the object Score using pre-established specifications    
        """

        self.Screen_WIDTH = WIDTH
        self.counter = 0
        self.score_design = ''

    def count(self, bird, pipes):
        """
        Flow that counts the score of the game
        Input = (Bird object, List)
        Output = None or Boolean
        """

        for pipe in pipes:
            if not pipe.passed:
                if pipe.x + pipe.top_img.get_width() // 2 < bird.x:
                    self.counter += 1
                    pipe.passed = True
                    return True

    def draw(self, window):
        """
        Visual representation of the score
        Input = (Bird object, List)
        """

        self.score_design = STAT_FONT.render(
            'Score: ' + str(self.counter), True, (255, 255, 255))
        window.blit(self.score_design, (self.Screen_WIDTH -
                                        self.score_design.get_width() - 15, 10))

        self.score_design = STAT_FONT.render(
            'Score: ' + str(self.counter), True, (0, 0, 0))

        window.blit(self.score_design, (self.Screen_WIDTH -
                                        self.score_design.get_width() - 13, 12))

    def save_score(self):
        """
        Saves the highest score to a .txt file
        """

        file = open("Assets/highscore.txt", "r")
        if int(file.readline()) < self.counter:
            file.close()
            file1 = open("Assets/highscore.txt", "w")
            file1.write('%i' % self.counter)
            file1.close()
        else:
            file.close()
