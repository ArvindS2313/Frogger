import pygame
import math
import os 

class Log:
    '''
    Log class: defines a log object which the player can jump onto
    Methods:
        - 
    Attributes:
        - 
    '''

    def __init__(self, WIN, dir, y_cor, x_cor=-10):
        self.WIN = WIN
        self.VEL = 1
        self.dir = 0       # will move rightward by default
        if dir == -1:      # flip car if moving leftward
            self.dir = 180

        self.LOG = pygame.image.load(os.path.join('Images', 'log.png'))
        self.LOG = pygame.transform.rotate(self.LOG, self.dir)

        self.log = pygame.Rect(x_cor, y_cor, self.LOG.get_width(), self.LOG.get_height())

    def move(self):
        self.log.x += math.cos(self.dir)*self.VEL

    def speed_up(self):
        self.VEL += 1

    def change_x(self):
        if self.dir == 0:
            if self.log.x > self.WIN.get_width():
                # log beyond border; not acceptable, must redraw
                self.log.x = -self.log.width
        if self.dir == 180:
            if self.log.x < -self.log.width:
                # log beyond border; not acceptable, must redraw
                self.log.x = self.WIN.get_width()

    def update(self):
        self.WIN.blit(self.LOG, (self.log.x, self.log.y))

