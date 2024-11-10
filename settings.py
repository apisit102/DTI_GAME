import pygame as pg
from pygame.math import Vector2 as vec

# สีต่างๆ (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1600   # 16 * 100 or 32 * 50 or 64 * 25
HEIGHT = 960  # 16 * 60 or 32 * 30 or 64 * 15
FPS = 60

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 500
PLAYER_IMG = "betty.png"