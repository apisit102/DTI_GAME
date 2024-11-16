import pygame as pg # pg ย่อมาจาก pygame
import sys
from os import path
# import file
from sprites import *
from settings import *
from tilemap1 import *
from sprites import NPC  # นำเข้า NPC จากไฟล์ sprites.py
from npc_data import NPC_DATA

# สร้างคลาสเกม
class Game:
    # default constructor
    def __init__(self):
        # เริ่มต้น pygame
        pg.init()

        # หน้าต่างแสดงผลให้มีขนาด = 1600 * 960
        self.scr_display = pg.display.set_mode((WIDTH, HEIGHT))

        # ชื่อเกม
        pg.display.set_caption("Good knight")

        # ตัวแปรเวลา
        self.clock = pg.time.Clock()

        # ตรวจการกดปุ่มค้างไว้
        pg.key.set_repeat(200, 200)

        # self.quests = []  # รายการเควสในเกม
        self.collected_items = 0
        self.current_quest = None
        
        

        self.backgrounds = {
    "map1.txt": "img/map1.png",
    "map2.txt": "img/map2.png",
    "map3.txt": "img/map3.png",
    "map4.txt": "img/map4.png",
    "map5.txt": "img/map5.png",
    
}

        # กำหนดแผนที่แต่ละทิศทาง
        self.map_files = {
            "map1.txt": {"up": None, "down": "map2.txt", "left": None, "right": None},
            "map2.txt": {"up": None, "down": "map3.txt", "left": None, "right": None},
            "map3.txt": {"up": "map2.txt", "down": "map4.txt", "left": None, "right": None},
            "map4.txt": {"up": None, "down": None, "left": None, "right": "map5.txt"},
            "map5.txt": {"up": "map6.txt", "down": None, "left": None, "right": None}
        }

        # กำหนดแมพเริ่มต้น
        self.current_map = "map1.txt"

        # โหลดข้อมูลแมพ
        self.load_data()
        

    # -----------------------------------------------------------------------------------

    # โหลดข้อมูลพื้นฐานก่อนเริ่มเกม
    def load_data(self):

        background_file = self.backgrounds.get(self.current_map)
        if background_file:
            self.background_image = pg.image.load(background_file).convert_alpha()

        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.map = Map(path.join(game_folder, self.current_map))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

    def show_main_menu(self):
        # โหลดภาพพื้นหลัง
        background_image = pg.image.load("img/menubg2.png").convert()

        ### ปุ่ม ###
        font = pg.font.Font(None, 50)   # ขนาดตัวอักษร
        # สี r g b
        button_color = (255, 255, 255)  # สีข้อความในปุ่ม
        hover_color = (235, 230, 150)   # สีพื้นหลังของปุ่ม
        animate_scale = 1.1 # สัดส่วนการขยายเมื่อเมาส์วางบนปุ่ม

        # ตำแหน่ง x,y ขนาด x,y ของปุ่ม
        start_button = pg.Rect(300, 125, 250, 70)   # ปุ่ม Start
        option_button = pg.Rect(300, 240, 250, 70)  # ปุ่ม Option
        exit_button = pg.Rect(300, 355, 250, 70)    # ปุ่ม Exit

        while True:
            # วาดภาพพื้นหลัง มุมซ้ายตำแหน่ง 0 0
            self.scr_display.blit(background_image, (0, 0))

            # ตรวจสอบตำแหน่งของเมาส์
            mouse_pos = pg.mouse.get_pos()

            # แอนิเมชั่นปุ่ม Start: ขยายขนาดเมื่อเมาส์วางบนปุ่ม
            if start_button.collidepoint(mouse_pos):
                animated_start_button = start_button.inflate(int(start_button.width * (animate_scale - 1)), int(start_button.height * (animate_scale - 1)))
                pg.draw.rect(self.scr_display, hover_color, animated_start_button)
            else:
                pg.draw.rect(self.scr_display, button_color, start_button)

            # ปุ่ม Option และ Exit
            pg.draw.rect(self.scr_display, button_color if not option_button.collidepoint(mouse_pos) else hover_color, option_button)
            pg.draw.rect(self.scr_display, button_color if not exit_button.collidepoint(mouse_pos) else hover_color, exit_button)

            # วาดข้อความในปุ่ม
            self.draw_text("Start", font, (0, 0, 0), start_button.centerx, start_button.centery)
            self.draw_text("Option", font, (0, 0, 0), option_button.centerx, option_button.centery)
            self.draw_text("Exit", font, (0, 0, 0), exit_button.centerx, exit_button.centery)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.new()  # เริ่มเกมใหม่
                        return
                    elif exit_button.collidepoint(event.pos):
                        self.quit()


            # update จอ
            pg.display.flip()
            self.clock.tick(FPS)


    def quit(self):
        pg.quit()
        sys.exit()

    def new(self):
        # รีเซ็ตกลุ่ม Sprite
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.npcs = pg.sprite.Group()

        # เพิ่ม NPC จาก NPC_DATA
        if self.current_map in NPC_DATA:
            for npc_info in NPC_DATA[self.current_map]:
                npc = NPC(self, npc_info["x"], npc_info["y"], npc_info["image_paths"], npc_info["text"])
                self.all_sprites.add(npc)
                self.npcs.add(npc)

        # เพิ่มกำแพง ผู้เล่น ศัตรู และมอนสเตอร์จากข้อมูล map.txt
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == "E":
                    enemy = Enemy(self, col, row)
                    self.all_sprites.add(enemy)
                    self.enemies.add(enemy)
                if tile == "M":
                    monster = Enemy(self, col, row)  # ใช้คลาส Enemy สำหรับมอนสเตอร์
                    self.all_sprites.add(monster)
                    self.enemies.add(monster)

        # ตั้งค่ากล้อง
        self.camera = Camera(self.map.width, self.map.height)
        self.camera.update(self.player)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.kill()  # ลบตัวละครออกเมื่อสุขภาพเหลือ 0

    def draw_health(self):
        # กำหนดขนาดของหลอดเลือดให้เล็กลงเพื่อให้เหมาะกับขนาดตัวละคร
        bar_length = 64  # ความยาวหลอดเลือดที่เล็กลง
        bar_height = 8   # ความสูงหลอดเลือดที่เล็กลง

        # ตำแหน่งของตัวละครที่ปรับตามกล้อง
        player_pos = self.camera.apply(self.player).topleft

        # คำนวณตำแหน่งของหลอดเลือดให้อยู่เหนือหัวของตัวละคร
        x = player_pos[0]
        y = player_pos[1] - 10  # ปรับตำแหน่ง y ให้เหมาะสมให้อยู่เหนือศีรษะ

        # คำนวณความยาวของหลอดเลือดตามค่าเลือดที่เหลืออยู่
        health_ratio = self.player.health / 100  # สมมติให้ค่าเลือดสูงสุดเป็น 100
        health_bar_length = int(bar_length * health_ratio)

        # วาดพื้นหลังของหลอดเลือด (สีแดง)
        pg.draw.rect(self.scr_display, (255, 0, 0), (x, y, bar_length, bar_height))
        # วาดหลอดเลือดตามค่าเลือดที่เหลือ (สีเขียว)
        pg.draw.rect(self.scr_display, (0, 255, 0), (x, y, health_bar_length, bar_height))

    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.scr_display.blit(text_obj, text_rect)

    def is_level_complete(self):
        # เงื่อนไข: ไม่มีศัตรูเหลืออยู่ในด่าน
        if not any(enemy in self.all_sprites for enemy in self.enemies):
            # ตรวจสอบว่าศัตรูเหลืออยู่หรือไม่
            return not self.enemies
        # เงื่อนไข: ผู้เล่นถึงจุดหมาย
        # if self.player.rect.colliderect(self.goal_rect):
        #     return True
        return False

    def show_ending_scene(self):
        # โหลดภาพพื้นหลังสำหรับฉากจบ
        background_image = pg.image.load("img/end.png").convert()

        # ข้อความสำหรับฉากจบเป็นภาษาไทย
        ending_texts = [
            u"ท่านผู้กล้า ท่านช่างกล้าหาญยิ่งนัก.",
            u"ความสงบสุขได้กลับมาสู่อาณาจักร ด้วยฝีมือของท่าน.",
            u"พระราชาและประชาชนทุกคนต่างสำนึกในบุญคุณของท่าน.",
            u"การผจญภัยได้สิ้นสุดลงแล้ว แต่ตำนานของท่านจะคงอยู่.",
            u"ขอบคุณที่ร่วมเล่นเกมนี้!"
        ]

        # กำหนดฟอนต์ภาษาไทย
        font_path = path.join("font", "THSarabunNew.ttf")  # ระบุที่อยู่ของฟอนต์ภาษาไทย
        font = pg.font.Font(font_path, 40)  # ใช้ฟอนต์ภาษาไทย ขนาด 40

        current_text_index = 0  # ตำแหน่งข้อความปัจจุบัน
        text_to_display = ""    # ข้อความที่แสดงบนหน้าจอ
        char_index = 0          # ตำแหน่งตัวอักษรสำหรับเอฟเฟกต์การพิมพ์
        self.showing_ending = True  # ตัวแปรควบคุมการแสดงฉากจบ
        delay_after_sentence = 2000  # หน่วงเวลา 2 วินาทีหลังจากแสดงประโยคครบ
        sentence_complete_time = None  # เวลาที่แสดงประโยคครบทุกตัวอักษร
        typing_speed = 50  # ความเร็วการแสดงผล (มิลลิวินาทีระหว่างตัวอักษร)
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
            text_surface = font.render(text_to_display, True, (0, 0, 0))
            text_rect = text_surface.get_rect(midbottom=(WIDTH // 2, HEIGHT - 45))  # จุดแสดงผลของข้อความ
            self.scr_display.blit(text_surface, text_rect)

            
            # ตรวจจับเหตุการณ์
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    # หากกด Enter ให้ข้ามไปหน้าเมนู
                    self.reset_game()  # รีเซ็ตสถานะเกมหลังจบคัทซีน
                    self.show_main_menu()
                    return
                
            pg.display.flip()  # อัปเดตหน้าจอ
            self.clock.tick(FPS)  # ปรับความเร็วในการแสดงผลเฟรม

    def load_next_map(self): 
        # เช็คว่ามีแมพต่อไปหรือไม่
        if self.current_map_index < len(self.map_files) - 1:
            self.current_map_index += 1  # เปลี่ยนไปที่แมพถัดไป
            self.load_data()  # โหลดข้อมูลของแมพใหม่
            self.new()  # เรียกใช้งาน method เพื่อรีเซ็ตกลุ่ม sprite สำหรับแมพใหม่

    def load_map_in_direction(self, direction):
    # ตรวจสอบว่าทิศทางนี้มีแผนที่หรือไม่
        next_map = self.map_files[self.current_map].get(direction)
        if next_map:
            self.current_map = next_map  # เปลี่ยนแผนที่ปัจจุบันเป็นแผนที่ถัดไปในทิศทางที่ระบุ
            self.load_data()
            self.new()  # รีเซ็ตกลุ่ม sprite สำหรับแผนที่ใหม่

    def draw_npc_text(self):
        font_path = path.join("font", "THSarabunNew.ttf")  # ฟอนต์ภาษาไทย
        font = pg.font.Font(font_path, 30)

        for npc in self.npcs:
            if npc.display_message:  # NPC กำลังแสดงข้อความ
                text_surface = font.render(npc.text, True, (0, 0, 0))
                # ตำแหน่งข้อความสัมพันธ์กับกล้อง
                npc_screen_pos = self.camera.apply(npc)
                text_rect = text_surface.get_rect(midbottom=(npc_screen_pos.centerx, npc_screen_pos.top - 10))

                # วาดพื้นหลังข้อความ
                padding = 10
                bg_rect = pg.Rect(
                    text_rect.left - padding,
                    text_rect.top - padding,
                    text_rect.width + padding * 2,
                    text_rect.height + padding * 2
                )
                pg.draw.rect(self.scr_display, (255, 255, 255), bg_rect)
                pg.draw.rect(self.scr_display, (0, 0, 0), bg_rect, 2)

                # วาดข้อความ
                self.scr_display.blit(text_surface, text_rect)

    # method แสดงผล
    def draw(self):
        # แสดงผล background และ sprite อื่นๆ
        if self.background_image:
            self.scr_display.blit(self.background_image, self.camera.apply_rect(self.background_image.get_rect()))

        self.draw_npc_text()    # แสดงข้อความของ NPC เมื่อผู้เล่นเข้าใกล้

        for sprite in self.all_sprites:
            self.scr_display.blit(sprite.image, self.camera.apply(sprite))  # แสดง sprite ทั้งหมด

        self.draw_health()  # แสดงค่าเลือดของตัวละครหลัก
        pg.display.flip()  # อัปเดตหน้าจอให้แสดงผล

    # method อัพเดทตำแหน่งของสไปร์ท
    def update(self):

        self.all_sprites.update()
        self.camera.update(self.player)  # อัปเดตตำแหน่งของกล้องตามผู้เล่น

        # หากจบเกมในด่านสุดท้าย ให้กลับไปหน้าเมนูและรีเซ็ตแผนที่ใหม่
        if self.current_map == "map5.txt" and self.is_level_complete():
            self.show_ending_scene()
            self.reset_game()
            self.show_main_menu()
            return


    def reset_game(self):
        
        self.current_map = "map1.txt"  # กำหนดแผนที่เริ่มต้นใหม่
        # self.collected_items = 0  # รีเซ็ตจำนวนไอเทมที่เก็บ
        # self.current_quest = None  # รีเซ็ตเควส
        if hasattr(self, "player"):  # ตรวจสอบว่ามีผู้เล่นในเกม
            self.player.health = 100  # รีเซ็ตค่าพลังชีวิตของผู้เล่น
        self.load_data()  # โหลดข้อมูลแผนที่ใหม่


        # method อีเวนท์ต่างๆ
    def events(self): 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                self.player.handle_events(event)  # เรียกใช้อีเวนต์ของผู้เล่น

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
                return  # กลับไปหน้าเมนูหลังฉากจบ

    # ----------------------------------------------------------------------

    def load_map_in_direction(self, direction):
        # ตรวจสอบว่าทิศทางนี้มีแผนที่หรือไม่
        next_map = self.map_files[self.current_map].get(direction)
        if next_map:
            self.current_map = next_map  # เปลี่ยนแผนที่ปัจจุบันเป็นแผนที่ถัดไปในทิศทางที่ระบุ
            self.load_data()  # โหลดข้อมูลแผนที่ใหม่
            self.new()  # เรียกใช้งาน method new เพื่อรีเซ็ตกลุ่ม sprite สำหรับแผนที่ใหม่

# -----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    game = Game()
    game.show_main_menu()
    game.new()
    game.run()  