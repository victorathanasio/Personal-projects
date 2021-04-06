import pygame
import os



class Ground:
    speed = 5  # velocity of the surrondings

    def __init__(self, theme='Theme_mvp'):
        """ 
        Method that initiates the object Ground using pre-established specifications    
        """

        self.ground_img = pygame.image.load(os.path.join(
            'Assets/' + theme, 'base_big.png')).convert_alpha()
        self.size = self.ground_img.get_width()
        self.x_black = 0
        self.x_white = self.size
        self.y = 600  # where the floor starts

    def move(self):
        """
        Method that moves left the Ground
        """

        self.x_black += -self.speed
        self.x_white += -self.speed

        if self.x_black + self.size < 0:
            self.x_black = self.x_white + self.size
        if self.x_white + self.size < 0:
            self.x_white = self.x_black + self.size

    def collide(self, bird):
        """ 
        Method that checks for colisions with the bird
        Inputs = (Bird object)
        Output = None or Boolean
        """

        if bird.y > 540:
            if bird.alive:
                return True

    def draw(self, window):
        """
        Method that creates the visual representation for the ground
        Input = (Window object)
        """

        window.blit(self.ground_img, (self.x_black, self.y))
        window.blit(self.ground_img, (self.x_white, self.y))
