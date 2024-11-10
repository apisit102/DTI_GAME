import pygame as pg # pg ย่อมาจาก pygame
import sys
from os import path
# import file
from sprites import *
from settings import *
from tilemap1 import *

# change for re upload
# ------------------------------------ สร้าง class Game ขึ้น ------------------------------------
class Game:
    # ------------------------------- default constructor -------------------------------
    def __init__(self):
        # เริ่มต้น pygame
        pg.init()

        # หน้าต่างแสดงผลให้มีขนาด = WIDTH, HEIGHT
        self.scr_display = pg.display.set_mode((WIDTH, HEIGHT))
        
        # ตั้งค่าชื่อของหน้าต่างเกม ซึ่งจะแสดงที่แถบด้านบนของหน้าต่าง
        pg.display.set_caption("Sweet teacher")

        # ใช้สำหรับควบคุมความเร็วในการอัปเดตและการแสดงผลของเกม
        self.clock = pg.time.Clock()

        # ใช้สำหรับการตั้งค่าการทำซ้ำของการกดปุ่มคีย์บอร์ด เมื่อผู้ใช้กดปุ่มค้างไว้
        pg.key.set_repeat(200, 200)  # (เวลารอตรวจจับกดปุ่มซ้ำหลังจากกดปุ่มค้างไว้, ตรวจจับว่ากดซ้ำเรื่อยๆในอีก...ตราบใดที่ยังกด)

        self.backgrounds = {
    "map1.txt": "img/map1.png",
    "map2.txt": "img/map2.png",
    "map3.txt": "img/map3.png",
    "map4.txt": "img/map4.png",
    "map5.txt": "img/map5.png",
    "map6.txt": "img/map6.png"
}

        # กำหนดแผนที่แต่ละทิศทาง
        self.map_files = {
            "map1.txt": {"up": None, "down": "map2.txt", "left": None, "right": None},
            "map2.txt": {"up": None, "down": "map3.txt", "left": None, "right": None},
            "map3.txt": {"up": "map2.txt", "down": "map4.txt", "left": None, "right": None},
            "map4.txt": {"up": None, "down": None, "left": None, "right": "map5.txt"},
            "map5.txt": {"up": "map6.txt", "down": None, "left": None, "right": None},
            "map6.txt": {"up": None, "down": None, "left": None, "right": None}
        }
        
        self.current_map = "map1.txt"  # กำหนดแมพเริ่มต้น
        self.load_data()  # โหลดข้อมูลแมพ
    # -----------------------------------------------------------------------------------

        
        
    # Exit
    def quit(self):
        pg.quit()
        sys.exit()

    def show_start_screen(self):
        pass

    def is_level_complete(self):
        # ตัวอย่างเงื่อนไข: ไม่มีศัตรูเหลืออยู่ในด่าน
        if not any(enemy in self.all_sprites for enemy in self.enemies):
            # ตรวจสอบว่าศัตรูเหลืออยู่หรือไม่
            return not self.enemies
        # ตัวอย่างเงื่อนไข: ผู้เล่นถึงจุดหมาย
        # if self.player.rect.colliderect(self.goal_rect):
        #     return True
        return False

    def show_ending_scene(self):
        # โหลดภาพพื้นหลังสำหรับฉากจบ
        background_image = pg.image.load("img/end.png").convert()

        # ข้อความสำหรับฉากจบและตัวแปรสำหรับเอฟเฟกต์การพิมพ์
        ending_texts = [
            "ท่านผู้กล้า ท่านช่างกล้าหาญยิ่งนัก.",
            "Peace has returned to the kingdom, thanks to you.",
            "The king and all the citizens are forever grateful.",
            "The adventure is over, but your legacy will live on.",
            "Thank you for playing!"
        ]
        current_text_index = 0  # ตำแหน่งข้อความปัจจุบัน
        text_to_display = ""    # ข้อความที่แสดงบนหน้าจอ
        char_index = 0          # ตำแหน่งตัวอักษรสำหรับเอฟเฟกต์การพิมพ์
        self.showing_ending = True  # ตัวแปรควบคุมการแสดงฉากจบ
        delay_after_sentence = 2000  # หน่วงเวลา 2 วินาทีหลังจากแสดงประโยคครบ
        sentence_complete_time = None  # เวลาที่แสดงประโยคครบทุกตัวอักษร
        typing_speed = 75  # ความเร็วการแสดงผล (มิลลิวินาทีระหว่างตัวอักษร)
        last_char_time = 0  # เก็บเวลาตัวอักษรก่อนหน้า

        while self.showing_ending:
            self.scr_display.blit(background_image, (0, 0))  # วาดภาพพื้นหลัง

            # แสดงข้อความแบบทีละตัวอักษรด้วยการหน่วงเวลา
            if char_index < len(ending_texts[current_text_index]):
                if pg.time.get_ticks() - last_char_time > typing_speed:
                    text_to_display += ending_texts[current_text_index][char_index]
                    char_index += 1
                    last_char_time = pg.time.get_ticks()  # อัปเดตเวลาของตัวอักษรล่าสุด
            else:
                # ตั้งเวลาเมื่อประโยคแสดงครบและรอ 2 วินาทีก่อนขึ้นประโยคถัดไป
                if sentence_complete_time is None:
                    sentence_complete_time = pg.time.get_ticks()
                elif pg.time.get_ticks() - sentence_complete_time > delay_after_sentence:
                    # ไปยังประโยคถัดไปหรือจบการแสดงผลถ้าครบทุกประโยคแล้ว
                    current_text_index += 1
                    if current_text_index < len(ending_texts):
                        text_to_display = ""     # รีเซ็ตข้อความ
                        char_index = 0           # รีเซ็ตตำแหน่งตัวอักษร
                        sentence_complete_time = None  # รีเซ็ตเวลาหลังจากเปลี่ยนประโยค
                    else:
                        self.showing_ending = False  # จบการแสดงฉากจบ

            # วาดกล่องข้อความและข้อความ โดยขยับขึ้น 15 พิกเซล
            font = pg.font.Font(None, 40)  # ตั้งค่าแบบอักษรและขนาด
            text_surface = font.render(text_to_display, True, (0, 0, 0))
            text_rect = text_surface.get_rect(midbottom=(WIDTH // 2, HEIGHT - 60))  # จุดแสดงผลของข้อความ
            self.scr_display.blit(text_surface, text_rect)

            pg.display.flip()  # อัปเดตหน้าจอ
            self.clock.tick(30)  # ปรับความเร็วในการแสดงผลเฟรม




    
    def load_next_map(self):
        # เช็คว่ามีแมพต่อไปหรือไม่
        if self.current_map_index < len(self.map_files) - 1:
            self.current_map_index += 1  # เปลี่ยนไปที่แมพถัดไป
            self.load_data()  # โหลดข้อมูลของแมพใหม่
            self.new()  # เรียกใช้งาน method เพื่อรีเซ็ตกลุ่ม sprite สำหรับแมพใหม่
            
    def load_data(self):
        
        background_file = self.backgrounds.get(self.current_map)
        if background_file:
            self.background_image = pg.image.load(background_file).convert_alpha()

        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.map = Map(path.join(game_folder, self.current_map))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        
        
    def load_map_in_direction(self, direction):
        # ตรวจสอบว่าทิศทางนี้มีแมพหรือไม่
        next_map = self.map_files[self.current_map].get(direction)
        if next_map:
            self.current_map = next_map  # เปลี่ยนแมพปัจจุบันเป็นแมพถัดไปในทิศทางที่ระบุ
            self.load_data()
            self.new()  # รีเซ็ตกลุ่ม sprite สำหรับแมพใหม่
            
            
    # method วาดตารางกริด
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.scr_display, LIGHTGREY, (x,0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.scr_display, LIGHTGREY, (0,y), (WIDTH, y))

    # method แสดงผล
    def draw(self):
        # แสดงผล background โดยให้ตำแหน่งสัมพันธ์กับตำแหน่งของกล้อง
        if self.background_image:
            self.scr_display.blit(self.background_image, self.camera.apply_rect(self.background_image.get_rect()))
        
        self.draw_grid() 
        for sprite in self.all_sprites:
            self.scr_display.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()
        
    # method อัพเดทตำแหน่งของสไปร์ท
    def update(self):
        
        self.all_sprites.update()
        self.camera.update(self.player)  # อัปเดตตำแหน่งของกล้องตามผู้เล่น

        # เพิ่มเงื่อนไขการจบด่าน 6
        if self.current_map == "map6.txt" and self.is_level_complete():
            self.show_ending_scene()
            self.quit()


    # method อีเวนท์ต่างๆ
    def events(self):

        # กดกาที่แถบด้านบนของหน้าต่างเพื่อออกเกม
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit() # เรียกใช้งาน method ออกเกม

            # เมื่อกดปุ่มอะไรบางอย่างจะเริ่มทำงาน
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:    # กด Esc เพื่อออกเกม
                    self.quit()                 # เรียกใช้งาน method ออกเกม

    # --------------------- สร้าง method run สำหรับรันเกม  ---------------------
    def run(self):
        
        # ตราบใดที่ self.playing = True เกมก็จะยังทำงาน
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

            # ตรวจสอบว่าผู้เล่นผ่านด่านที่ 6 แล้วหรือไม่
            if self.current_map == "map6.txt" and not any(self.all_sprites):
                self.show_ending_scene()
                self.quit()  # ออกจากเกมหลังจากแสดงฉากจบเสร็จ


    # ----------------------------------------------------------------------

    def new(self):
        # initialize all variables and do all the setup for a new game

        # สร้างกลุ่มของสไปร์ททั้งหมด จะเก็บวัตถุที่เป็นสไปร์ททั้งหมดที่เราต้องการ
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()  # เริ่มต้นกลุ่มศัตรู

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P": # ตำแหน่งเกิดผู้เล่น
                    self.player = Player(self, col, row)
                if tile == "E":  # ตำแหน่งของศัตรู
                    enemy = Enemy(self, col, row)
                    self.all_sprites.add(enemy)
                    self.enemies.add(enemy)
                    
        self.camera = Camera(self.map.width, self.map.height)
        
        
# -----------------------------------------------------------------------------------------------

# ------------------ ส่วนของการรันเกม ------------------
# เช็คว่าชื่อโมดูลปัจจุบัน (__name__) มีค่าเป็น '__main__' หรือไม่
# ถ้าใช่ แสดงว่าไฟล์นี้ถูกเรียกใช้โดยตรง
if __name__ == '__main__':
    game = Game()   # สร้าง object game จาก class Game
    game.new()
    game.run()
# ----------------------------------------------------


