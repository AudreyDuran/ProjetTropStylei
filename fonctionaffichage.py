import pygame

class envir():
	def __init__(self):
		self.taille_trou=60
		self.position_trou=100
		self.diametre=400
		self.debut=380
		self.longuer=70
a=envir()
print a.diametre

width=640; heigth=a.diametre+40
temps=0.0
# Initialize Pygame.
pygame.init()
# Set size of pygame window.
screen=pygame.display.set_mode((width,heigth))
# Create empty pygame surface.
background = pygame.Surface(screen.get_size())
# Fill the background white color.
background.fill((255, 255, 255))
# Convert Surface object to make blitting faster.
background = background.convert()
# Copy background to screen (position (0, 0) is upper left corner).
screen.blit(background, (0,0))
clock = pygame.time.Clock()

def vaisseau(surface,envir):# dessine le vaisseau et le trou
	pygame.draw.rect(screen,(200,40,40),((0,10),(width,10)),0)
	pygame.draw.rect(screen,(200,40,40),((0,envir.diametre+10),(width,10)),0)
	pygame.draw.rect(screen,(255,200,200),((a.debut,envir.diametre+10),(a.longuer,15)),0)

loop=True

while loop:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			loop = False 
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				loop = False # user pressed ESC
	screen.fill((255,255,255))
	temps += clock.tick(60) / 1000.0 
	text = "Playtime:%d"%temps
	vaisseau(screen,a)
	pygame.display.set_caption(text)
	pygame.display.flip()


# Finish Pygame.  
pygame.quit()
