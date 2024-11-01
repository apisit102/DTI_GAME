import pygame
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("DTI-ADVENTURE")

while  True:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			quit()
			FPS = 60 

