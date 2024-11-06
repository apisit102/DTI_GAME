import pygame 
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('code/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(0,-26)

		self.direction = pygame.math.Vector2()
		self.speed = 5

		self.obstacle_sprites = obstacle_sprites

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def move(self, speed):
		# ตรวจสอบและปรับการเคลื่อนที่ให้เป็นหน่วยเดียว
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		# อัปเดตตำแหน่งแนวนอน
		self.hitbox.x += self.direction.x * speed
		self.collision("horizontal")

		# อัปเดตตำแหน่งแนวตั้ง
		self.hitbox.y += self.direction.y * speed
		self.collision("vertical")
		self.rect.center = self.hitbox.center

	def collision(self, direction):
		if direction == "horizontal":
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:  # กำลังไปทางขวา
						self.hitbox.right = sprite.hitbox.left
					elif self.direction.x < 0:  # กำลังไปทางซ้าย
						self.hitbox.left = sprite.hitbox.right

		elif direction == "vertical":
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.hitbox):
					if self.direction.y > 0:  # กำลังไปข้างล่าง
						self.hitbox.bottom = sprite.rect.top
					elif self.direction.y < 0:  # กำลังไปข้างบน
						self.hitbox.top = sprite.rect.bottom

	def update(self):
		self.input()
		self.move(self.speed)
