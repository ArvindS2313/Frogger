import pygame 
import os
import math

class Enemy:
    '''
    Enemy class: represents an enemy car
    Attributes:
        - enemy velocity
        - enemy rectangle sprite
    Methods:
        - 
    '''

    def __init__(self, WIN, dir, y_cor, x_cor=-10):
        self.WIN = WIN
        self.VEL = 1
        self.dir = 0       # will move rightward by default
        if dir == -1:      # flip car if moving leftward
            self.dir = 180

        self.CAR = pygame.image.load(os.path.join('Images', 'car.png'))
        self.CAR = pygame.transform.rotate(self.CAR, self.dir)

        self.enemy = pygame.Rect(x_cor, y_cor, self.CAR.get_width(), self.CAR.get_height())

    def move(self):
        self.enemy.x += math.cos(self.dir)*self.VEL

    def speed_up(self):
        self.VEL += 1

    def change_x(self):
        if self.dir == 0:
            if self.enemy.x > self.WIN.get_width():
                # enemy beyond border; not acceptable, must redraw
                self.enemy.x = -self.enemy.width
        if self.dir == 180:
            if self.enemy.x < -self.enemy.width:
                # enemy beyond border; not acceptable, must redraw
                self.enemy.x = self.WIN.get_width()

    def update(self):
        self.WIN.blit(self.CAR, (self.enemy.x, self.enemy.y))


