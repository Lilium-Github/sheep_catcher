import pygame
import random
from constants import *

class Sheep:
    def __init__(self, x, y, image, direction):
        self.xpos = x
        self.ypos = y
        self.image = image

        self.dir = direction
        self.caught = False

    def move(self, timer):
        if timer % 50 == 0: #only change direction every 50 game loops
            self.dir = random.randrange(0, 4) #set random direction
        if self.dir == LEFT and self.xpos > 40:
            self.xpos-=2 #move left
        elif self.dir == RIGHT and self.xpos < 760:
            self.xpos += 2 #move right
        elif self.dir == UP and self.ypos > 40:
            self.ypos -=2 #move up
        elif self.ypos < 760:
            self.ypos +=2 #move down
    
    def collide(self, PlayerX, PlayerY, score):
        if PlayerX+40 > self.xpos:
            if PlayerX < self.xpos+40:
                if PlayerY+40 > self.ypos:
                    if PlayerY < self.ypos+40:
                        if self.caught == False: #only catch uncaught sheeps!
                            self.caught = True #catch da sheepies!
                            return score + 1
        return score

    def draw(self, surf):
        if not self.caught:
            surf.blit(self.image, (self.xpos, self.ypos))
