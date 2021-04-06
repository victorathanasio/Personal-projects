import pygame
import random
import os


class Pipe:
    vel = 5

    vel_up = 2
    vel_gap = 3
    min_height = 50
    max_height = 350
    max_dif = 50
    min_dif = -40

    def __init__(self, theme='Theme_mvp', x=1300, difficulty='Normal'):
        """ 
        Method that creates a pair of pipes using pre-established specifications    
        """

        self.gap = 180
        if difficulty == 'Easy':
            self.gap = 240
        self.difficulty = difficulty
        pipe_img = pygame.transform.scale2x(
            pygame.image.load(os.path.join("assets/" + theme, "pipe.png")).convert_alpha())

        self.dif = 0

        self.x = x
        self.gap = self.gap

        self.top = 0
        self.bottom = 0
        self.gap_pos = 0

        self.top_img = pygame.transform.flip(pipe_img, False, True)
        self.bottom_img = pipe_img

        self.passed = False
        self.set_height()

        self.up = True
        self.change = True

        self.top_mask = pygame.mask.from_surface(self.top_img)
        self.bottom_mask = pygame.mask.from_surface(self.bottom_img)

        self.width = self.top_img.get_width() // 2

    def set_height(self):
        """ 
        Method that calculates the positioning for the pipes, taking in consideration that
        the gap is in a random height 
        """

        self.gap_pos = random.randrange(50, 350)
        self.top = self.gap_pos - self.top_img.get_height() - self.dif
        self.bottom = self.gap_pos + self.gap + self.dif

    def move(self):
        """ 
        Method that moves the pipe
        """

        self.x -= self.vel
        if self.difficulty in ['Hard', 'Very Hard', 'Insane', 'Meme']:
            if self.up:
                self.move_up()
            else:
                self.move_down()

        if self.difficulty in ['Very Hard', 'Insane', 'Meme']:
            if self.change:
                self.change_gap_open()
            else:
                self.change_gap_close()

    def move_up(self):
        """ 
        Method that moves a pair of pipes upwards
        """

        if self.gap_pos > self.min_height:
            self.gap_pos -= self.vel_up
            self.top = self.gap_pos - self.top_img.get_height() - self.dif
            self.bottom = self.gap_pos + self.gap + self.dif
        else:
            self.up = False

    def move_down(self):
        """ 
        Method that moves a pair of pipes downwards
        """

        if self.gap_pos < self.max_height:
            self.gap_pos += self.vel_up
            self.top = self.gap_pos - self.top_img.get_height() - self.dif
            self.bottom = self.gap_pos + self.gap + self.dif
        else:
            self.up = True

    def change_gap_open(self):
        """ 
        Method that increases the size of the gap between a pair of pipes
        """

        if self.dif < self.max_dif:
            self.dif += self.vel_gap
            self.top = self.gap_pos - self.top_img.get_height() - self.dif
            self.bottom = self.gap_pos + self.gap + self.dif

        else:
            self.change = False

    def change_gap_close(self):
        """ 
        Method that decreases the size of the gap between a pair of pipes
        """

        if self.dif > self.min_dif:
            self.dif -= self.vel_gap
            self.top = self.gap_pos - self.top_img.get_height() - self.dif
            self.bottom = self.gap_pos + self.gap + self.dif

        else:
            self.change = True

    def draw(self, window):
        """ 
        Method that creates the visual representation of the pipe
        Input = (Window object)
        """

        window.blit(self.top_img, (self.x, self.top))
        window.blit(self.bottom_img, (self.x, self.bottom))

    def collision(self, bird):
        """ 
        Method that checks for colisions with the bird
        Inputs = (Bird object)
        Output = None or Boolean
        """

        bird_mask = bird.get_mask()

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(self.bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(self.top_mask, top_offset)

        if b_point or t_point:
            return True

    def expired(self):
        """ 
        Method that checks if the pipe no longer needs to be rendered
        Output = Boolean
        """

        if self.x + self.top_img.get_width() < 0:
            return True
        return False


class Pipes:

    def __init__(self, theme='Theme_orig', difficulty='Normal'):
        """ 
        Method that creates a list pair of pipes using pre-established specifications    
        """

        self.difficulty = difficulty
        self.theme = theme
        self.pipes = []
        self.nextpipe = 0

    def move(self):
        """ 
        Method that moves the pipes from a list of pipes
        """

        for pipe in self.pipes:
            pipe.move()

    def draw(self, window):
        """ 
        Method that creates the visual representation of the pipes
        Input = (Window object)
        """

        for pipe in self.pipes:
            pipe.draw(window)

    def delete_old_pipes(self):
        """ 
        Method that removes from the list pipes that are out of the screen
        """

        for i, pipe in enumerate(self.pipes):
            if pipe.expired():
                self.pipes.pop(i)

    def create_pipe(self, time):
        """ 
        Method that adds pipes to the list of pipes
        Input = (tick)
        """
        if time % 80 == 1 and self.difficulty not in {'Meme','Insane'}:
            self.pipes.append(
                Pipe(theme=self.theme, difficulty=self.difficulty))

        elif time % 30 == 1 and self.difficulty=='Meme':
            self.pipes.append(
                Pipe(theme=self.theme, difficulty=self.difficulty))
        
        elif time % 60 == 1 and self.difficulty=='Insane':
            self.pipes.append(
                Pipe(theme=self.theme, difficulty=self.difficulty))

        

    def get_next_pipe(self):
        """ 
        Method that returns the tube closest to the bird that has not yet been passed
        Output = Pipe object
        """

        return min((pipe for pipe in self.pipes if not pipe.passed), key=lambda pipe: pipe.x)

    def list_next_pipes(self):
        """ 
        Method that returns the tubes closest to the bird that have not yet been passed
        Output = List
        """

        return sorted((pipe for pipe in self.pipes if not pipe.passed), key=lambda pipe: pipe.x)

    def collision(self, bird):
        """ 
        Method that checks if any collision happened between the bird and the pipes
        Input = (Bird object)
        Output = Boolean
        """

        for pipe in self.pipes:
            if pipe.collision(bird):
                return True
            else:
                return False

    def __iter__(self):
        """ 
        Method creates iter method for object
        """

        return iter(self.pipes)

    def __len__(self):
        """ 
        Method creates len method for object
        """

        return len(self.pipes)
