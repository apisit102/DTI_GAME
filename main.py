import pygame as p  # เรียกใช้ pygame และย่อเป็น p
import sys 
from os import path  # ใช้เพื่อจัดการไฟล์และโฟลเดอร์
# import ไฟล์ที่มีคลาส Sprite และการตั้งค่าของเกม
from sprites import * 
from settings import *

class Game:
    # ฟังก์ชันเริ่มต้นของเกม
    def __init__(self):
        p.init() 

        # ตั้งค่าหน้าจอของเกมตาม WIDTH และ HEIGHT ที่ตั้งไว้ใน settings.py
        self.screen_display = p.display.set_mode((WIDTH, HEIGHT))

        # ตั้งชื่อหน้าต่างเกม
        p.display.set_caption("Sweet teacher")

        # ตั้งค่านาฬิกาของเกม
        self.clock = p.time.Clock()

        # ตั้งค่าการกดคีย์ซ้ำเมื่อกดปุ่มค้างไว้ (200 ms)
        p.key.set_repeat(200, 200)

        # โหลดข้อมูลที่จำเป็น
        self.load_data()
        
    # ฟังก์ชันออกจากเกม
    def quit(self):
        p.quit()
        sys.exit()

    # ฟังก์ชันแสดงหน้าจอเริ่มต้น
    def show_start_screen(self):
        pass

    # ฟังก์ชันแสดงหน้าจอเกมโอเวอร์
    def show_go_screen(self):
        pass

    # ฟังก์ชันโหลดข้อมูล เช่น แผนที่เกม
    def load_data(self):
        # ระบุตำแหน่งโฟลเดอร์ของไฟล์เกม
        game_folder = path.dirname(__file__)
        self.map_data = []
        # เปิดไฟล์ map.txt เพื่อโหลดข้อมูลแผนที่
        with open(path.join(game_folder, "map.txt"), "rt") as f:
            for line in f:
                self.map_data.append(line)

    # ฟังก์ชันวาดตารางกริด
    def draw_grid(self):
        # วาดเส้นแนวตั้งบนหน้าจอ
        for x in range(0, WIDTH, TILESIZE):
            p.draw.line(self.screen_display, LIGHTGREY, (x, 0), (x, HEIGHT))
        # วาดเส้นแนวนอนบนหน้าจอ
        for y in range(0, HEIGHT, TILESIZE):
            p.draw.line(self.screen_display, LIGHTGREY, (0, y), (WIDTH, y))

    # ฟังก์ชันแสดงผลหน้าจอเกม
    def draw(self):
        # ตั้งสีพื้นหลังของหน้าจอเป็นสีดำ
        self.screen_display.fill("BLACK")
        # เรียกใช้ฟังก์ชันวาดตารางกริด
        self.draw_grid()
        # วาด sprites ทั้งหมดบนหน้าจอ
        self.all_sprites.draw(self.screen_display)
        # อัพเดทหน้าจอแสดงผล
        p.display.flip()

    # ฟังก์ชันอัพเดทตำแหน่งของสไปรต์
    def update(self):
        self.all_sprites.update()

    # ฟังก์ชันจัดการเหตุการณ์ต่าง ๆ
    def events(self):
        # ตรวจสอบเหตุการณ์ที่เกิดขึ้น
        for event in p.event.get():
            # ถ้าเหตุการณ์เป็นการกดปุ่มปิดเกม
            if event.type == p.QUIT:
                self.quit()  # เรียกใช้ฟังก์ชันออกจากเกม

            # เมื่อมีการกดปุ่มคีย์บอร์ด
            if event.type == p.KEYDOWN:
                # กดปุ่ม ESC เพื่อออกจากเกม
                if event.key == p.K_ESCAPE:
                    self.quit()

                # การควบคุมการเดินของตัวละครหลัก
                if event.key == p.K_a:
                    self.player.move(dx=-1)  # เดินไปทางซ้าย
                if event.key == p.K_d:
                    self.player.move(dx=1)   # เดินไปทางขวา
                if event.key == p.K_w:
                    self.player.move(dy=-1)  # เดินไปข้างบน
                if event.key == p.K_s:
                    self.player.move(dy=1)   # เดินไปข้างล่าง

    # ฟังก์ชันรันเกม
    def run(self):
        # ตั้งค่าให้เกมทำงานต่อไปขณะที่ self.playing = True
        self.playing = True
        while self.playing:
            # ตั้งค่า FPS และเวลาแต่ละเฟรม
            self.dt = self.clock.tick(FPS) / 1000
            self.events()  # เรียกใช้ฟังก์ชันเหตุการณ์
            self.update()  # อัพเดทตำแหน่งสไปรต์
            self.draw()    # วาดผลลัพธ์บนหน้าจอ

    # ฟังก์ชันสร้างเกมใหม่
    def new(self):
        # สร้างกลุ่มสไปรต์และกำแพง
        self.all_sprites = p.sprite.Group()
        self.walls = p.sprite.Group()

        # สร้างตัวละครหลักที่ตำแหน่งเริ่มต้น (10, 10)
        self.player = Player(self, 10, 10)

        # โหลดแผนที่จากไฟล์และสร้างสไปรต์ตามข้อมูลแผนที่
        for row, tile in enumerate(self.map_data):
            for col, tile in enumerate(tile):
                if tile == "1":
                    Wall(self, col, row)

# เมื่อรันโปรแกรม จะสร้างเกมใหม่และเริ่มทำงาน
if __name__ == '__main__':
    game = Game()
    game.new()
    game.run()

