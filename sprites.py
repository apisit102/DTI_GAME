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
        self.image = pg.image.load('img/player/player.png').convert_alpha()
        self.images = {
    "idle_down": [pg.image.load('img/player/idle_down.png').convert_alpha()],
    "idle_up": [pg.image.load('img/player/idle_up.png').convert_alpha()],
    "idle_left": [pg.image.load('img/player/idle_left.png').convert_alpha()],
    "idle_right": [pg.image.load('img/player/idle_right.png').convert_alpha()],
    "walk_left": [
        pg.image.load('img/player/left_0.png').convert_alpha(),
        pg.image.load('img/player/left_1.png').convert_alpha(),
        pg.image.load('img/player/left_2.png').convert_alpha(),
        pg.image.load('img/player/left_3.png').convert_alpha(),
    ],
    "walk_right": [
        pg.image.load('img/player/right_0.png').convert_alpha(),
        pg.image.load('img/player/right_1.png').convert_alpha(),
        pg.image.load('img/player/right_2.png').convert_alpha(),
        pg.image.load('img/player/right_3.png').convert_alpha(),
    ],
    "walk_up": [
        pg.image.load('img/player/up_0.png').convert_alpha(),
        pg.image.load('img/player/up_1.png').convert_alpha(),
        pg.image.load('img/player/up_2.png').convert_alpha(),
        pg.image.load('img/player/up_3.png').convert_alpha(),
    ],
    "walk_down": [
        pg.image.load('img/player/down_0.png').convert_alpha(),
        pg.image.load('img/player/down_1.png').convert_alpha(),
        pg.image.load('img/player/down_2.png').convert_alpha(),
        pg.image.load('img/player/down_3.png').convert_alpha(),
    ],
}


        self.last_direction = "down"  # ตั้งค่าเริ่มต้นเป็นหันลง

        self.image = self.images["idle_down"][0]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.health = 100

        # Animation properties
        self.current_frame = 0
        self.last_update = 0
        self.frame_delay = 150  # Milliseconds between frames
        self.current_animation = "idle"

    def attack(self):
        # ตรวจสอบว่ากำลังโจมตีอยู่หรือไม่
        if "attack" in self.current_animation:
            return

        # กำหนดแอนิเมชันการโจมตี
        self.current_animation = f"attack_{self.last_direction}"
        self.current_frame = 0  # รีเซ็ตเฟรมของแอนิเมชัน

        # สร้างดาบใหม่
        sword = Sword(self.game, self)  # ใช้ last_direction เพื่อกำหนดทิศทาง
        self.game.all_sprites.add(sword)

        # ตรวจสอบการชนกับศัตรู
        for enemy in self.game.enemies:
            if sword.rect.colliderect(enemy.rect):
                enemy.health -= 10
                if enemy.health <= 0:
                    enemy.kill()

        # ตั้งเวลา cooldown
        self.last_attack_time = pg.time.get_ticks()

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                now = pg.time.get_ticks()
                if now - getattr(self, "last_attack_time", 0) > 500:  # Cooldown 500 ms
                    self.attack()

    def get_keys(self):
        keys = pg.key.get_pressed()

        if "attack" in self.current_animation:
            return  # หยุดตรวจสอบปุ่มเมื่ออยู่ในสถานะโจมตี

        self.vel = vec(0, 0)
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.last_direction = "left"
            self.current_animation = "walk_left"
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.last_direction = "right"
            self.current_animation = "walk_right"
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.last_direction = "up"
            self.current_animation = "walk_up"
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.last_direction = "down"
            self.current_animation = "walk_down"
        else:
            self.current_animation = f"idle_{self.last_direction}"  # ใช้ last_direction เมื่อยืนนิ่ง

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071  # ลดความเร็วในกรณีเคลื่อนที่แนวทแยง

    def update(self):
        # อัปเดตตำแหน่งของตัวละครจากการกดปุ่ม
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")

        # อัปเดตแอนิเมชัน
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images[self.current_animation])
            self.image = self.images[self.current_animation][self.current_frame]

        # ตรวจสอบการตาย
        if self.health <= 0:
            self.die()

        # ตรวจสอบการข้ามขอบแผนที่
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
        # เรียกใช้ดาบเพื่อโจมตี
        sword = Sword(self.game, self)  # สร้างดาบใหม่
        self.game.all_sprites.add(sword)  # เพิ่มดาบลงในกลุ่ม Sprite
        self.game.sword_sound.play()
        # ตรวจสอบการโจมตีศัตรู
        for enemy in self.game.enemies:
            if sword.rect.colliderect(enemy.rect):
                enemy.health -= 10  # ลดพลังชีวิตศัตรู
                if enemy.health <= 0:
                    enemy.kill()  # ลบศัตรูที่พลังชีวิตหมด

        # Cooldown สำหรับการโจมตี
        self.last_attack_time = pg.time.get_ticks()

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
        else:
            self.game.boss_hit_sound.play()



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
        self.frame_delay = 150  # เวลาในการเปลี่ยนเฟรม (มิลลิวินาที)

        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.topleft = self.pos
        self.text = text  # ข้อความที่ NPC พูด
        self.display_message = False  # ค่าเริ่มต้น: ไม่แสดงข้อความ

        self.direction = vec(0, 0)  # ทิศทางการเคลื่อนไหวของ NPC
        self.change_direction()  # สุ่มการเคลื่อนไหว

    def change_direction(self):
        """สุ่มทิศทางการเคลื่อนไหวของ NPC"""
        directions = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1), vec(0, 0)]  # รวมทิศทางที่ไม่เคลื่อนไหว
        self.direction = random.choice(directions)
        self.move_time = pg.time.get_ticks() + random.randint(2000, 5000)  # เปลี่ยนทิศทางทุก 2-5 วินาที

    def update_animation(self):
        """อัปเดตแอนิเมชันของ NPC"""
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

    def interact(self):
        """แสดงข้อความเมื่อผู้เล่นพูดคุยกับ NPC"""
        print(f"NPC: {self.text}")  # อาจเปลี่ยนให้แสดงบนหน้าจอแทนการแสดงในคอนโซล

    def update(self):
        """อัปเดตสถานะของ NPC"""
        # อัปเดตแอนิเมชัน
        self.update_animation()

        # อัปเดตการเคลื่อนไหว
        now = pg.time.get_ticks()
        if now > self.move_time:
            self.change_direction()  # เปลี่ยนทิศทางเมื่อครบเวลา

        if self.direction:
            self.pos += self.direction * 0.5  # ความเร็วของ NPC (ปรับได้ตามต้องการ)
            self.rect.topleft = self.pos

            # หากชนกับกำแพง ให้เปลี่ยนทิศทาง
            if pg.sprite.spritecollideany(self, self.game.walls):
                self.pos -= self.direction * 0.5
                self.change_direction()

        # ตรวจสอบว่าผู้เล่นอยู่ใกล้ NPC หรือไม่
        distance = vec(self.game.player.rect.center).distance_to(vec(self.rect.center))
        self.display_message = distance < 100  # แสดงข้อความหากผู้เล่นอยู่ใกล้




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

        # ลบศัตรูที่พลังชีวิต <= 0 และอัปเดตกลุ่ม enemies
        if self.health <= 0:
            self.kill()
            self.game.enemies.remove(self)  # ลบจากกลุ่ม enemies

class Sword(pg.sprite.Sprite):
    def __init__(self, game, owner):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.owner = owner

        # โหลดภาพดาบในแต่ละทิศทาง
        self.images = {
            "left": pg.image.load('img/left.png').convert_alpha(),
            "right": pg.image.load('img/right.png').convert_alpha(),
            "up": pg.image.load('img/up.png').convert_alpha(),
            "down": pg.image.load('img/down.png').convert_alpha(),
        }

        # กำหนดภาพดาบตามทิศทางเริ่มต้น
        self.image = self.images["down"]
        self.rect = self.image.get_rect()

        # ระยะเวลาที่ดาบจะคงอยู่
        self.attack_time = pg.time.get_ticks()
        self.attack_duration = 300  # ระยะเวลาโจมตี (300 มิลลิวินาที)

        # เพิ่มตัวแปรเพื่อเก็บศัตรูที่ถูกโจมตีแล้ว
        self.attacked_enemies = []  # ตัวแปรนี้จะเก็บรายชื่อศัตรูที่ดาบได้โจมตีไปแล้ว

        # อัปเดตตำแหน่งดาบ
        self.update_position()

    def update_position(self):
        # ปรับตำแหน่งและภาพดาบตามทิศทางของผู้เล่น
        direction = self.owner.last_direction
        self.image = self.images[direction]

        # ตั้ง offset สำหรับปรับตำแหน่งดาบให้เหมาะสม
        offset_x = 0
        offset_y = 0

        if direction == "left":
            self.rect.midright = self.owner.rect.midleft
            offset_x = -10
        elif direction == "right":
            self.rect.midleft = self.owner.rect.midright
            offset_x = 10
        elif direction == "up":
            self.rect.midbottom = self.owner.rect.midtop
            offset_y = -10
        elif direction == "down":
            self.rect.midtop = self.owner.rect.midbottom
            offset_y = 10

        self.rect.x += offset_x
        self.rect.y += offset_y

    def update(self):
        # อัปเดตตำแหน่งดาบทุกเฟรม
        self.update_position()

        # ตรวจสอบการชนกับศัตรู
        for enemy in self.game.enemies:
            if enemy not in self.attacked_enemies and self.rect.colliderect(enemy.rect):
                self.attacked_enemies.append(enemy)  # เพิ่มศัตรูที่ถูกโจมตีในลิสต์
                enemy.health -= 10  # ลดพลังชีวิตศัตรู
                if enemy.health <= 0:
                    enemy.kill()  # ลบศัตรูออกจากเกม

        # ลบดาบเมื่อระยะเวลาโจมตีสิ้นสุด
        if pg.time.get_ticks() - self.attack_time > self.attack_duration:
            self.kill()

class FinalBoss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('img/monster102x.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.health = 350
        self.attack_cooldown = 2000  # ระยะเวลาระหว่างการเริ่มโจมตีครั้งถัดไป
        self.last_attack_time = pg.time.get_ticks()
        self.attack_delay = 3000  # ดีเลย์ 3 วิก่อนโจมตี
        self.attack_ready = False
        self.pending_attack = None  # เก็บข้อมูลพื้นที่โจมตีที่เตรียมไว้

    def update(self):
        now = pg.time.get_ticks()
        # ตรวจสอบว่าถึงเวลาเริ่มโจมตีใหม่หรือยัง
        if not self.attack_ready and now - self.last_attack_time > self.attack_cooldown:
            self.prepare_attack()  # เตรียมพื้นที่โจมตี
            self.attack_ready = True  # สถานะพร้อมโจมตี
            self.attack_start_time = now  # บันทึกเวลาที่เริ่มเตรียมโจมตี
        
        # หากเตรียมโจมตีแล้ว ให้รอครบดีเลย์เพื่อทำการโจมตีจริง
        if self.attack_ready and now - self.attack_start_time > self.attack_delay:
            self.execute_attack()  # ทำการโจมตี
            self.last_attack_time = now  # บันทึกเวลาที่โจมตีเสร็จ
            self.attack_ready = False  # รีเซ็ตสถานะโจมตี

    def prepare_attack(self):
        # สุ่มตำแหน่งพื้นที่โจมตีรอบ ๆ ผู้เล่น
        player_rect = self.game.player.rect
        attack_area_size = 150
        attack_x = random.randint(player_rect.left - attack_area_size, player_rect.right)
        attack_y = random.randint(player_rect.top - attack_area_size, player_rect.bottom)
        attack_rect = pg.Rect(attack_x, attack_y, attack_area_size, attack_area_size)
        
        # แสดงเอฟเฟกต์เตือนล่วงหน้า (สีเหลืองโปร่งใส)
        warning_effect = WarningEffect(self.game, attack_rect.center, attack_area_size)
        self.game.all_sprites.add(warning_effect)
        self.pending_attack = attack_rect  # เก็บตำแหน่งพื้นที่โจมตีที่เตรียมไว้

    def execute_attack(self):
        # สร้างพื้นที่โจมตีจริง (สีแดง) จากตำแหน่งที่เตรียมไว้
        if self.pending_attack:
            explosion = Explosion(self.game, self.pending_attack.center)
            self.game.all_sprites.add(explosion)
            # ตรวจสอบว่าผู้เล่นอยู่ในพื้นที่โจมตีหรือไม่
            if self.game.player.rect.colliderect(self.pending_attack):
                self.game.player.take_damage(20)  # ลดพลังชีวิตผู้เล่น
            self.pending_attack = None  # ลบข้อมูลพื้นที่โจมตีที่ใช้ไปแล้ว

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.die()

    def die(self):
        self.kill()

class WarningEffect(pg.sprite.Sprite):
    def __init__(self, game, center, size):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((size, size), pg.SRCALPHA)
        pg.draw.circle(self.image, (255, 255, 0, 128), (size // 2, size // 2), size // 2)  # วาดวงกลมสีเหลืองโปร่งใส
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        # ลบพื้นที่เตือนหลังจากดีเลย์โจมตี (3 วินาที)
        if pg.time.get_ticks() - self.spawn_time > 700:
            self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, game, center):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((100, 100), pg.SRCALPHA)  # พื้นที่โจมตี
        pg.draw.circle(self.image, (255, 0, 0, 128), (50, 50), 50)  # วงกลมสีแดงโปร่งใส
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        # ลบพื้นที่โจมตีหลังจาก 500 มิลลิวินาที
        if pg.time.get_ticks() - self.spawn_time > 500:
            self.kill()


