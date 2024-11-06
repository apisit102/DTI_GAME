import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type  # ใช้ค่า sprite_type
        self.image = pygame.image.load('code/rock.png').convert_alpha()  # กำหนดรูปภาพ
        self.rect = self.image.get_rect(topleft=pos)  # กำหนดตำแหน่ง
        self.hitbox = self.rect.inflate(0, -10)  # การปรับขนาด hitbox
