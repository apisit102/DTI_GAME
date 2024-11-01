import pygame as pg
from settings import *

# Player Class 
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # กำหนดกลุ่มสไปร์ทที่ผู้เล่นจะถูกเพิ่มเข้าไป
        self.groups = game.all_sprites
        # เพิ่มตัว Player เข้ากลุ่มสไปร์ท
        pg.sprite.Sprite.__init__(self, self.groups)  
        self.game = game  
        self.image = pg.Surface((TILESIZE, TILESIZE))  
        self.image.fill(YELLOW)  
        # สร้างสี่เหลี่ยมล้อมรอบพื้นผิว
        self.rect = self.image.get_rect() 
        self.x = x  # ตำแหน่ง X ของผู้เล่นในกริด
        self.y = y  # ตำแหน่ง Y ของผู้เล่นในกริด

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            
        # ฟังก์ชันเคลื่อนที่ตามค่าที่ส่งเข้ามา
            self.x += dx
            self.y += dy
    
    def collide_with_walls(self, dx = 0, dy =0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
    
    def update(self):
        # อัปเดตตำแหน่งของผู้เล่นในกริดไปยังตำแหน่งจริงในพิกเซล
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


# Wall Class 
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        # กำหนดกลุ่มสไปร์ทที่กำแพงจะถูกเพิ่มเข้าไป (ทั้ง all_sprites และ walls)
        self.groups = game.all_sprites, game.walls

        pg.sprite.Sprite.__init__(self, self.groups)    

        self.game = game    # เก็บข้อมูลอ้างอิงถึงอ็อบเจกต์เกมหลัก
        # สร้างพื้นผิวสี่เหลี่ยมขนาด 32 * 32 สำหรับกำแพง
        self.image = pg.Surface((TILESIZE, TILESIZE))   
        self.image.fill(RED)                       
        # สร้างสี่เหลี่ยมล้อมรอบพื้นผิวเพื่อใช้งานหลายอย่างเช่น การตรวจจับการชนของวัตถุ
        self.rect = self.image.get_rect() 
        self.x = x  # ตำแหน่ง X ของกำแพงในกริด
        self.y = y  # ตำแหน่ง Y ของกำแพงในกริด

        # อัปเดตตำแหน่งกำแพงในพิกเซลโดยคูณตำแหน่งในกริดด้วยขนาด TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
