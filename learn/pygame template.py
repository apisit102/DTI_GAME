# Pygame template - skeleton for a new pygame project

import pygame as pg
import random
import sys
from settings import *
from sprites import *

class Game:
    def __init__(self):

        # Initialize Pygame
        pg.init()
        # Initialize Sound
        pg.mixer.init()

        # Create window
        self.scr_display = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My game")

        # Game attributes
        self.clock = pg.time.Clock()
        self.player = Player()
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
    # Game loop
    def run(self):
        self.playing = True
        while self.playing:

            # Maintain frame rate
            self.clock.tick(FPS)

            # Process input (events)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

            # Draw / render
            self.scr_display.fill(BLUE)
            self.all_sprites.draw(self.scr_display)

            # Update
            self.all_sprites.update()
            
            # After drawing everything, flip the display
            pg.display.flip()
    
    # Exit
    def quit(self):
        pg.quit()
        sys.exit()

game = Game()
game.run()