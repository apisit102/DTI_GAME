import pygame as pg
from settings import *
vec = pg.math.Vector2

# ----------------------------- Player Class -----------------------------
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # กำหนดกลุ่มสไปร์ทที่ผู้เล่นจะถูกเพิ่มเข้าไป
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)  # เพิ่มตัว Player เข้ากลุ่มสไปร์ท
        self.game = game  # เก็บข้อมูลอ้างอิงถึงอ็อบเจกต์เกมหลัก
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load('img/player.png').convert_alpha()    # เพิ่มรูปตัวละคร
        self.rect = self.image.get_rect()  # สร้างสี่เหลี่ยมล้อมรอบพื้นผิว
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.game = game
        self.health = 100  # กำหนดค่าเลือดเริ่มต้นเป็น 100

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def move(self, dx=0, dy=0):
        # ฟังก์ชันเคลื่อนที่ตามค่าที่ส่งเข้ามา ถ้าไม่ชนกับกำแพง
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x <0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x

        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.kill()  # ลบตัวละครออกเมื่อสุขภาพเหลือ 0

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        # อัปเดตตำแหน่งของผู้เล่นในกริดไปยังตำแหน่งจริงในพิกเซล
        self.rect.x = self.pos.x
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")


        # ตรวจสอบว่าผู้เล่นถึงขอบของแมพในแต่ละทิศหรือไม่
        if self.rect.right >= self.game.map.width:
            self.game.load_map_in_direction("right")  # โหลดแมพทางขวา
            self.pos = vec(0, self.pos.y)  # รีเซ็ตตำแหน่งผู้เล่นไปที่ขอบซ้ายของแมพใหม่
        elif self.rect.left <= 0:
            self.game.load_map_in_direction("left")  # โหลดแมพทางซ้าย
            self.pos = vec(self.game.map.width - self.rect.width, self.pos.y)
        elif self.rect.top <= 0:
            self.game.load_map_in_direction("up")  # โหลดแมพทางบน
            self.pos = vec(self.pos.x, self.game.map.height - self.rect.height)
        elif self.rect.bottom >= self.game.map.height:
            self.game.load_map_in_direction("down")  # โหลดแมพทางล่าง
            self.pos = vec(self.pos.x, 0)

# ------------------------------------------------------------------------

# ------------------------------ Wall Class ------------------------------
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        # กำหนดกลุ่มสไปร์ทที่กำแพงจะถูกเพิ่มเข้าไป (ทั้ง all_sprites และ walls)
        self.groups = game.all_sprites, game.walls

        pg.sprite.Sprite.__init__(self, self.groups)    # เพิ่มตัว Wall เข้ากลุ่มสไปร์ท

        self.game = game    # เก็บข้อมูลอ้างอิงถึงอ็อบเจกต์เกมหลัก

        self.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)   # สร้างพื้นผิวสี่เหลี่ยมขนาด 64 * 64 สำหรับกำแพง และทำให้จาง
        #.image = pg.image.load('img/rock.png').convert_alpha() # ลงสีกำแพงล่องหนเป็นก้อนหิน
        self.image.fill((0, 255, 0, 128))   # ลงสีให้กำแพงล่องหน ใส่ # เพื่อเอาออก
        self.rect = self.image.get_rect()   # สร้างสี่เหลี่ยมล้อมรอบพื้นผิวเพื่อใช้งานหลายอย่างเช่น การตรวจจับการชนของวัตถุ

        self.x = x  # ตำแหน่ง X ของกำแพงในกริด
        self.y = y  # ตำแหน่ง Y ของกำแพงในกริด

        # อัปเดตตำแหน่งกำแพงในพิกเซลโดยคูณตำแหน่งในกริดด้วยขนาด TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
# ------------------------------------------------------------------------