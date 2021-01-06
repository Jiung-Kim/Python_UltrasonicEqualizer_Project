## https://pythonprogramming.altervista.org/pygame-how-to-display-the-frame-rate-fps-on-the-screen/

## Pygame: how to display the frame rate (FPS) on the screen

## short version 
'''
This is a little less complicated version

We initialise pygame, create the screen, the clock and the font objects
in the while loop we
clear the screen (screen.fill((0,0,0))
call the update_fps() => it gets the clock fps and render it on the screen
update the screen
'''
import pygame
 
pygame.init()
screen = pygame.display.set_mode((1000,400))  # 화면 크기 
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
 
 
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text
 
 
loop = 1
while loop:
	screen.fill((0, 0, 0))
	screen.blit(update_fps(), (10,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop = 0
	clock.tick(60)
	pygame.display.update()
 
pygame.quit()