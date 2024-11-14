import pygame as pg
import random
from settings import *
vec = pg.math.Vector2

# ----------------------------- Player Class -----------------------------
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('img/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.health = 100

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
        if keys[pg.K_SPACE]:  # กด Space เพื่อโจมตี
            self.attack()
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")

        # ตรวจสอบการตาย
        if self.health <= 0:
            self.die()

        # การตรวจสอบการข้ามขอบของแผนที่
        if self.rect.right >= self.game.map.width:
            self.game.load_map_in_direction("right")
            self.pos = vec(0, self.pos.y)
        elif self.rect.left <= 0:
            self.game.load_map_in_direction("left")
            self.pos = vec(self.game.map.width - self.rect.width, self.pos.y)
        elif self.rect.top <= 0:
            self.game.load_map_in_direction("up")
            self.pos = vec(self.pos.x, self.game.map.height - self.rect.height)
        elif self.rect.bottom >= self.game.map.height:
            self.game.load_map_in_direction("down")
            self.pos = vec(self.pos.x, 0)

    def collide_with_walls(self, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
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

    def attack(self):
        # ตรวจสอบการโจมตีด้วยระยะใกล้ (เช่น 50 พิกเซล)
        attack_range = 50
        for enemy in self.game.enemies:
            distance = self.pos.distance_to(enemy.pos)
            if distance <= attack_range:
                enemy.health -= 10  # ลดพลังชีวิตศัตรู
                if enemy.health <= 0:
                    enemy.kill()  # กำจัดศัตรูถ้าพลังชีวิตหมด

    def die(self):
        print("Player has died!")
        self.game.show_main_menu()  # กลับไปยังเมนูหลัก หรือแสดงฉากจบ
        self.kill()  # ลบ Player ออกจาก Sprite

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
            
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()  # เรียกใช้ฟังก์ชัน die() เมื่อพลังชีวิตเหลือ 0



# ------------------------------ Wall Class ------------------------------
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)
        #self.image.fill((0, 255, 0, 128))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# ------------------------------ NPC Class ------------------------------
class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, image_paths, text):
        self._layer = 1
        self.groups = game.all_sprites, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.images = [pg.image.load(image_path).convert_alpha() for image_path in image_paths]
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_delay = 150  # ความหน่วงระหว่างเฟรม

        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.topleft = self.pos
        self.text = text  # ข้อความที่ NPC พูด
        self.display_message = False  # กำหนดค่าเริ่มต้นว่าข้อความไม่แสดง
        self.direction = vec(0, 0)  # ทิศทางการเคลื่อนไหวของ NPC
        self.change_direction()



    def change_direction(self):
        directions = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1), vec(0, 0)]
        self.direction = random.choice(directions)
        self.move_time = pg.time.get_ticks() + random.randint(1000, 3000)

    def update(self):
        # อัปเดตเอนิเมชัน
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

        # อัปเดตการเคลื่อนไหว
        if now > self.move_time:
            self.change_direction()
        if self.direction:
            self.pos += self.direction
            self.rect.topleft = self.pos
            if pg.sprite.spritecollideany(self, self.game.walls):
                self.pos -= self.direction
                self.change_direction()

        # ตรวจสอบระยะห่างสำหรับการแสดงข้อความ
        # ใน sprites.py ในคลาส NPC ในเมธอด update
        distance = vec(self.game.player.rect.center).distance_to(vec(self.rect.center))

        self.display_message = distance < 100
        
        

# ------------------------------ Enemy Class ------------------------------
class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('img/mona.png').convert_alpha()  # ใช้รูปมอนสเตอร์
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.topleft = self.pos
        self.health = 50  # กำหนดพลังชีวิตของมอนสเตอร์
        self.speed = 20  # กำหนดความเร็ว

    def update(self):
        # ติดตามผู้เล่น
        player_pos = self.game.player.pos
        direction = (player_pos - self.pos).normalize() if player_pos != self.pos else vec(0, 0)
        self.pos += direction * self.speed * self.game.dt
        self.rect.topleft = self.pos

        # ตรวจสอบการชนกับกำแพง
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.pos -= direction * self.speed * self.game.dt
            self.rect.topleft = self.pos

        # ตรวจสอบการโจมตีผู้เล่น
        if self.rect.colliderect(self.game.player.rect):
            self.game.player.take_damage(0.1)  # ลดพลังชีวิตของผู้เล่น

