# Pygame template - skeleton for a new pygame project

import pygame as pg
import random
import sys
from settings import *
import os

# setup assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Player(pg.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "p1_jump.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.y_speed = 5
    
    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT -400:
            self.y_speed = -5
        if self.rect.top < 400:
            self.y_speed = 5
        if self.rect.left > WIDTH:
            self.rect.right = 0