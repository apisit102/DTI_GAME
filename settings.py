import pygame as pg
from pygame.math import Vector2 as vec

# สีต่างๆ (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1600   # 16 * 100 or 32 * 50 or 64 * 25
HEIGHT = 960  # 16 * 60 or 32 * 30 or 64 * 15
FPS = 60

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 500
PLAYER_IMG = "betty.png"

# ข้อมูล npc และตำแหน่ง npc
NPC_DATA = {
    "map1.txt": [
        {"x": 10, "y": 7, "image": "img/npcsoldier2.png", "text": "Hello from NPC in map1"},
        {"x": 14, "y": 7, "image": "img/npcsoldier2.png", "text": "I'm NPC 2 in map1"}
    ],
    "map2.txt": [
        {"x": 14, "y": 7, "image": "img/npcsoldier2.png", "text": "Take sword"}
    ],
    "map3.txt": [
        {"x": 20, "y": 15, "image": "img/npcsoldier2.png", "text": "Greetings from NPC in map3"},
        {"x": 21, "y": 18, "image": "img/npcsoldier2.png", "text": "Greetings from NPC in map3"},
        {"x": 20, "y": 20, "image": "img/npcsoldier2.png", "text": "Greetings from NPC in map3"},
        {"x": 25, "y": 15, "image": "img/npcsoldier2.png", "text": "Greetings from NPC in map3"},
        {"x": 30, "y": 18, "image": "img/npcsoldier2.png", "text": "Greetings from NPC in map3"},
        {"x": 20, "y": 15, "image": "img/npcsoldier2.png", "text": "Greetings from NPC in map3"},
        {"x": 20, "y": 15, "image": "img/npcsoldier2.png", "text": "Greetings from NPC in map3"}
    ]
    # เพิ่มข้อมูล NPC สำหรับแผนที่อื่น ๆ ที่ต้องการ
}