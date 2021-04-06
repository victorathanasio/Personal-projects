import pygame
import os


class Radio:

    def __init__(self, settings):
        """ 
        Method that initiates the object Radio for game sounds
        Input = (Dict)  
        """

        pygame.mixer.init()
        self.file_die_sound = pygame.mixer.Sound('Assets/Sounds/die.mp3')
        self.file_hit_sound = pygame.mixer.Sound('Assets/Sounds/hit.mp3')
        self.file_wing_sound = pygame.mixer.Sound('Assets/Sounds/wing.mp3')
        self.file_score_sound = pygame.mixer.Sound('Assets/Sounds/point.mp3')

        self.volume = settings['Sound Volume']

        self.file_score_sound.set_volume(self.volume * 0.3)
        self.file_die_sound.set_volume(self.volume)
        self.file_hit_sound.set_volume(self.volume)
        self.file_wing_sound.set_volume(self.volume)
        self.file_score_sound.set_volume(self.volume)

    def die_sound(self):
        """ 
        Method that play the death sound
        """

        self.file_die_sound.play()

    def score_sound(self):
        """ 
        Method that play the score sound
        """

        self.file_score_sound.play()

    def hit_sound(self):
        """ 
        Method that play the hit sound
        """

        self.file_hit_sound.play()

    def wing_sound(self):
        """ 
        Method that play the wing beat sound
        """

        self.file_wing_sound.play()
