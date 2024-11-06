import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug


class Level:
    def __init__(self):
        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        #for row_index, row in enumerate(WORLD_MAP):
        #    for col_index, col in enumerate(row):
        #       x = col_index * TILESIZE
        #      y = row_index * TILESIZE
        #     if col == 'x':
        #            Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
        #       if col == 'p':
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()  # ใช้ super() เพื่อเรียกใช้ฟังก์ชันของ pygame.sprite.Group
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2  # ใช้ get_width() และ get_height()
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.Vector2()  # ใช้ pygame.Vector2() แทน pygame.math.Vector2()
        
        # แก้ไขการโหลดภาพพื้น
        self.floor_surf = pygame.image.load("code/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))  # ใช้ get_rect()

    def custom_draw(self, player):
        # คำนวณ offset โดยใช้ตำแหน่งของ player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        # เลื่อนพื้น (floor) ให้เหมาะสมกับตำแหน่ง
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)  # แก้ไขการพิมพ์ผิด

        # จัดเรียงสไปรท์ตามตำแหน่ง Y (จากเล็กไปใหญ่)
        sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)
        
        # วาดสไปรท์ที่เรียงแล้ว
        for sprite in sorted_sprites:
            # บวกตำแหน่ง offset ไปยังตำแหน่งเดิมของ sprite
            offset_rect = pygame.Vector2(sprite.rect.topleft) - self.offset  # แปลงเป็น pygame.Vector2()
            
            # วาดสไปรท์ที่มีการเลื่อนตำแหน่ง
            self.display_surface.blit(sprite.image, offset_rect)

            self.display_surface.blit(sprite.image, offset_rect)
            self.display_surface.blit(sprite.image, offset_rect)

