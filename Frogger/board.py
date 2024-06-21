import pygame 
import os
import player
import enemy
import log
import random
pygame.font.init()

class Board:
    '''
    Board class: represents the Frogger board
    Attributes:
        - dimensions 
        - list of enemies 
    Methods:
        - generate the board 
        - assembles the enemy movement on the board 
        - checks for enemy/player collision
        - switches board to water (if time)
    '''

    def __init__(self, WIN):
        self.WIN = WIN  # pygame window
        self.WIDTH = self.WIN.get_width()
        self.HEIGHT = self.WIN.get_height()

        # load pygame images and fonts
        self.GRASS = pygame.image.load(os.path.join('Images', 'grass.png'))
        self.ROAD = pygame.image.load(os.path.join('Images', 'road.png'))
        self.HEDGE = pygame.image.load(os.path.join('Images', 'hedge.png'))
        self.LILLY = pygame.image.load(os.path.join('Images', 'lilly.png'))
        self.SCORE = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'lives.png')), (50,50))
        self.WATER = pygame.image.load(os.path.join('Images', 'water.png'))
        self.FONT = pygame.font.SysFont('futura', 30)

        self.num_roads = 4
        self.num_waters = 4
        self.enemies = []   # 2d list
        self.logs = []      # 2d list
        self.player = player.Player(WIN, vel=self.ROAD.get_height())

        # store the road objects 
        self.roads = [] # 2d list of roads
        for row in range(1, self.num_roads+1):
            r = []
            y = self.HEIGHT - self.GRASS.get_width() - row*self.ROAD.get_width()
            for x in range(0, self.WIDTH, self.ROAD.get_width()):
                rect = pygame.Rect(x, y, self.ROAD.get_width(), self.ROAD.get_height())
                r.append(rect)
            self.roads.append(r)

        # store the water widths 
        self.water = []
        y -= self.GRASS.get_height()
        for row in range(1, self.num_waters+1):
            r = []
            y -= self.WATER.get_height()
            for x in range(0, self.WIDTH, self.WATER.get_width()):
                rect = pygame.Rect(x, y, self.WATER.get_width(), self.WATER.get_height())
                r.append(rect)
            self.water.append(r)

        # store the top hedge widths
        self.top_hedge = []
        y -= self.GRASS.get_width()
        for x in range(0, self.WIDTH, self.HEDGE.get_width()):
            self.top_hedge.append(pygame.Rect(x, y, self.HEDGE.get_width(), 
                                              self.GRASS.get_height()))
            
        # store the (occupied) lilly pads as rectangle objects
        self.pads = []
        self.occupied_pads = []     # pads which are currently occupied by a frog
        for x in range(64, self.WIDTH - self.LILLY.get_width(), 128):
            pad = pygame.Rect(x, y, self.LILLY.get_width(), self.LILLY.get_height())
            self.pads.append(pad)

        
    def init_moveables(self):
        '''
        Initialize the enemy cars on the screen with random xs and ys
        '''
        self.enemies = []
        for r in range(len(self.roads)):
            y = self.roads[r][0].y 
            x = random.randint(-10, self.WIDTH/2)
            dir = 1 if r % 2 == 0 else -1
            e1 = enemy.Enemy(self.WIN, dir, y, x)
            e2 = enemy.Enemy(self.WIN, dir, y, x+e1.enemy.width+random.randint(100, 400))
            self.enemies.append([e1, e2])

        self.logs = []
        for r in range(len(self.water)):
            y = self.water[r][0].y 
            x = random.randint(-10, self.WIDTH/2)
            dir = 1 if r % 2 == 0 else -1
            l1 = log.Log(self.WIN, dir, y, x)
            l2 = log.Log(self.WIN, dir, y, x+l1.log.width+random.randint(100, 400))
            self.logs.append([l1, l2])


    def move_moveables(self):
        for r in range(len(self.enemies)):
            for e in range(len(self.enemies[r])):
                self.enemies[r][e].move()
                self.enemies[r][e].change_x()

        for r in range(len(self.logs)):
            for l in range(len(self.logs[r])):
                self.logs[r][l].move()
                self.logs[r][l].change_x()

    def draw_board(self):
        self.WIN.fill((255, 255, 255))
        # one initial layer of grass
        for x in range(0, self.WIDTH, self.GRASS.get_width()):
            self.WIN.blit(self.GRASS, (x,self.HEIGHT - self.GRASS.get_width()))

        # four layers of roads
        for row in self.roads:
            for rect in row:
                self.WIN.blit(self.ROAD, (rect.x, rect.y))

        # middle grass 
        for x in range(0, self.WIDTH, self.GRASS.get_width()):
            self.WIN.blit(self.GRASS, (x, self.roads[-1][0].y - self.GRASS.get_height()))

        # four water layers
        for row in self.water:
            for rect in row:
                self.WIN.blit(self.WATER, (rect.x, rect.y))
        
        # top hedge widths
        for rect in self.top_hedge:
            self.WIN.blit(self.HEDGE, (rect.x, rect.y))

        # lilly pads - store 
        for pad in self.pads:
            self.WIN.blit(self.LILLY, (pad.x, pad.y))

        # occupied pads 
        for pad in self.occupied_pads:
            self.WIN.blit(pygame.transform.rotate(self.player.FROG, 180), (pad.x + 10, pad.y + 15))

        # lives and score frogs
        y, x = 10, self.WIDTH - 10*self.player.num_lives - self.player.num_lives*self.SCORE.get_width()
        text = self.FONT.render("Lives: ", 1, (0,0,0))
        self.WIN.blit(text, (x-text.get_width(),y))
        for _ in range(self.player.get_lives()):
            self.WIN.blit(self.SCORE, (x, y))
            x += 5 + self.SCORE.get_width()

