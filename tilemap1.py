import pygame as pg
from settings import *
import os

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())
    
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # ปรับตำแหน่งของเอนทิตีตามกล้อง
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        # ปรับตำแหน่งของสี่เหลี่ยมตามกล้อง
        return rect.move(self.camera.topleft)

    def update(self, target):
        # คำนวณตำแหน่ง x และ y ของกล้อง โดยให้ตัวละครอยู่ตรงกลาง
        x = -target.rect.centerx + WIDTH // 2
        y = -target.rect.centery + HEIGHT // 2

        # จำกัดการเลื่อนกล้องไม่ให้ออกนอกขอบแผนที่
        x = min(0, x)  # ขอบซ้าย
        y = min(0, y)  # ขอบบน
        x = max(-(self.width - WIDTH), x)  # ขอบขวา
        y = max(-(self.height - HEIGHT), y)  # ขอบล่าง

        # อัปเดตตำแหน่งของกล้อง
        self.camera = pg.Rect(x, y, self.width, self.height)