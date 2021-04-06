import os



class Game_settings:
    WINDOW_HEIGHT = 700
    WINDOW_WIDTH = 1200

    def __init__(self):
        """
        Method that initiates the object Game settings
        """

        self.game_settings = {
            'WINDOW_HEIGHT': 700,
            'WINDOW_WIDTH': 1200,
            'Theme': 'Theme_orig',
            'Difficulty': 'Normal',
            'Sound Volume': 0.3,
            'Mode': 'Regular',
            'Speed': 'Normal'
        }

    def set_difficulty(self, label, value):
        """
        Method that changes the difficulty of the game in the object
        Input = (str,str)
        """

        self.game_settings['Difficulty'] = value

    def set_theme(self, label, value):
        """
        Method that changes the theme of the game in the object
        Input = (str,str)
        """

        self.game_settings['Theme'] = value

    def set_sound(self, label, value):
        """
        Method that changes the sound level of the game in the object
        Input = (str,str)
        """

        self.game_settings['Sound Volume'] = value

    def set_mode(self, label, value):
        """
        Method that changes the mode of the game in the object
        Input = (str,str)
        """

        self.game_settings['Mode'] = value

    def get_settting(self, label):
        """
        Method that returns the value of the dict
        Input = (str)
        Output = Obj
        """

        return self.game_settings[label]

    def set_speed(self, label, value):
        """
        Method that changes the speed of the game in the object
        Input = (str,str)
        """

        self.game_settings['Speed'] = value
