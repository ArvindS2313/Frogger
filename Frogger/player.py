import pygame 
import os

class Player:
    '''
    Player class: represents the character playing the game
    Atributes:
        - image
        - cooridnates 
        - how many lives
    Methods:
        - move player
    '''

    def __init__(self, WIN, vel=60):
        self.WIN = WIN
        self.num_lives = 3
        self._lives = self.num_lives
        self.FROG = pygame.image.load(os.path.join("Images", "frog1.png"))
        self.FROG = pygame.transform.rotate(self.FROG, 180)
        self.VEL = vel

        self.init_x = self.WIN.get_width()//2 - self.FROG.get_width()//2
        self.init_y = self.WIN.get_height() - self.FROG.get_height() - 10 
        self.player = pygame.Rect(self.init_x, self.init_y, self.FROG.get_width(), 
                                  self.FROG.get_height())

    def update(self):
        self.WIN.blit(self.FROG, (self.player.x, self.player.y))

    def get_lives(self):
        return self._lives

    def has_died(self):
        self._lives -= 1

    def inc_lives(self):
        # bug: also colliding with hedge, so this is temporary fix
        self._lives += 1

    def reset(self):
        self.player.x = self.init_x
        self.player.y = self.init_y       
        
    def move(self, dir):
        if dir == 'l' and self.player.x - self.VEL > 0:
            self.player.x -= self.VEL
        elif dir == 'r' and self.player.x + self.FROG.get_width() + self.VEL < self.WIN.get_width():
            self.player.x += self.VEL
        elif dir == 'd' and self.player.y + self.FROG.get_height() + self.VEL < self.WIN.get_height():
            self.player.y += self.VEL
        elif dir == 'u' and self.player.y - self.VEL > 0:
            self.player.y -= self.VEL
        return
    
    
