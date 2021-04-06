import pygame
import os


VEL_JUMP = -23
G = 98 * 1.5
MAX_D = 16
X0 = 200
Y0 = 200


class Bird:
    def __init__(self, theme='Theme_mvp'):
        """ 
        Method that initiates the object Bird using pre-established specifications    
        """

        path = os.path.join("Assets/", theme)

        path1 = os.path.join(path, "bird1.png")
        path2 = os.path.join(path, "bird2.png")
        path3 = os.path.join(path, "bird3.png")

        self.Bird_imgs = [pygame.transform.scale2x(pygame.image.load(path1)).convert_alpha(),
                          pygame.transform.scale2x(
                              pygame.image.load(path2)).convert_alpha(),
                          pygame.transform.scale2x(pygame.image.load(path3)).convert_alpha()]
        self.x = X0
        self.y = Y0
        self.vel = 0
        self.height = self.y
        self.time = 0
        self.img = self.Bird_imgs[0]
        self.falling = False
        self.angle = -30
        self.time_img = 0
        self.time_anim = 5
        self.alive = True

        self.img_size = (self.Bird_imgs[0].get_width(
        ) // 2, self.Bird_imgs[0].get_height() // 2)

    def move(self):
        """
        Method that calculates the trajectory of the bird
        Output = Boolean
        """

        if self.falling:
            self.time += 1

        d = self.vel * (self.time / 60) + G / 2 * (self.time / 60) ** 2
        if not self.alive:
            d = G / 2 * (self.time / 60) ** 2

        # maximum speed:
        if abs(d) >= MAX_D:
            d = (d / abs(d)) * MAX_D

        if d < 0:
            d -= 4

        if self.falling:
            self.y += d

        if self.y < 0:
            self.y = 0

        if self.y > 541:
            self.y = 541
        self.angle = self.get_angle()
        return False

    def get_angle(self):
        """ 
        Method that calculates the angle of the bird for the animation
        Output = Int
        """

        if self.falling:
            if self.y < 540:
                if self.vel * (self.time / 60) + G / 2 * (self.time / 60) ** 2 < 10 and self.alive:
                    self.angle -= 3
                    if self.angle < -30:
                        self.angle = -30
                else:
                    self.angle += 1 + 0.2 * self.time ** 0.56
                    # angle = -110 + (self.time)**2/30
                if self.angle > 90:
                    self.angle = 90
                if self.angle < -90:
                    self.angle = -90
        else:
            return 0
        return self.angle

    def draw(self, window):
        """
        Method that creates the visual representation for the bird
        Input = (Window object)
        Output = Boolean
        """

        self.time_img += 1
        if self.alive:
            if self.time_img < self.time_anim:
                self.img = self.Bird_imgs[0]
            elif self.time_img < self.time_anim * 2:
                self.img = self.Bird_imgs[1]
            elif self.time_img < self.time_anim * 3:
                self.img = self.Bird_imgs[2]
            elif self.time_img < self.time_anim * 4:
                self.img = self.Bird_imgs[1]
            elif self.time_img < self.time_anim * 5:
                self.img = self.Bird_imgs[0]
                self.time_img = 0
        
        self.rot_img = pygame.transform.rotate(self.img, -self.angle)

        window.blit(self.rot_img, (self.x, self.y))

        return False

    def jump(self):
        """
        Method that makes the bird jump
        Output = None or Boolean
        """

        if self.alive:
            self.falling = True
            self.vel = VEL_JUMP
            self.time = 0
            self.height = self.y
            return False

    def get_mask(self):
        """
        Method that returns the mask of the bird
        This is useful for checking collisions using the vectorized image
        Output = Array
        """

        return pygame.mask.from_surface(pygame.transform.rotate(self.img, -self.get_angle()))
