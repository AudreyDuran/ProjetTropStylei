import numpy
import math
import os
import pygame
import random as r

class envir():#environnement type
	def __init__(self):
		self.taille_trou=60
		self.position_trou=100
		self.diametre=700
		self.debut=380
		self.longuer=150
a=envir()

class protein:
	def __init__(self, rayon, x, y,i):
		
		self.x = x
		self.y = y
		self.rayon = rayon
		self.id=i
		self.activation = 0
		

	def detection(self, a):

		d = math.sqrt((self.x-a.x)**2 + (self.y - a.y)**2)

		if d <= self.rayon:
			a.activation=True
			return True

		else:
			return False


	def move(self, dt, vitesse_lim, position_trou, taille_trou, debut, fin, diametre):
		if self.activation == False :
			self.x += dt * r.uniform(-1/16*vitesse_lim, vitesse_lim)
			self.y += dt * r.uniform(-vitesse_lim, vitesse_lim)
			# Pour eviter qu elle sorte du vaiseau par le haut
			if self.y < 0 :
				self.y = 0.
			# Pour eviter qu elle sorte par le cote gauche
			if self.x < 0:
				self.x = 0.
			# Pour eviter qu elle sorte du vaiseau tant qu il n y a pas le trou
			if self.y > diametre:
				if self.x < position_trou:
					if self.x > position_trou+taille_trou:
						self.y = diametre
			# Quand elle arrivent a la fin
			if self.x > fin :
				self.x = debut
				self.y = r.uniform(0, diametre)
			# Quand elle sort par le trou, on considere a partir d un moment que elle ne soit plus en contact avec le reste lorsqu
			# elle sort d un certain perimetre ici on aurait un cercle de rayon 150
			centre_trou = [position_trou+taille_trou/2, diametre]
			if self.y > diametre:
				if math.sqrt((self.x - centre_trou[0])**2 + (self.y - centre_trou[1])**2) > math.sqrt(150):
					self.x = debut
					self.y = r.uniform(0, diametre)
					# Pour le comptage des proteine qui sont sortie du cercle
					return 1
			# Pour le comptage des proteine qui ne sont pas sortie du cercle
			return 0

width=900; heigth=a.diametre+40 #l'hauteur est 40 a plus car je veut donner espessure 10 a chaque paroi + 10 de vide
color=[(0,0,255),(255,255,0)]#vecteur de couleurs pour chaque couleur
temps=0.0

#liste de proteines aleatoires
listprot=[]
listprot.append(protein(20,r.randint(0,639),r.randint(0,a.diametre),0))
listprot.append(protein(20,r.randint(0,639),r.randint(0,a.diametre),1))

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

def printvaisseau(surface,envir):# dessine le vaisseau et le trou
	pygame.draw.rect(screen,(200,40,40),((0,10),(width,10)),0)
	pygame.draw.rect(screen,(200,40,40),((0,envir.diametre+10),(width,10)),0)
	pygame.draw.rect(screen,(255,55,155),((a.debut,envir.diametre+10),(a.longuer,15)),0)

def printallprotein(surface,listpr):#dessine toutes les proteines dans la liste prot total
	for protein in listpr:
		pygame.draw.circle(screen,color[protein.id],(int(protein.x),int(protein.y+20)),protein.rayon,protein.activation)


loop=True

while loop: #loop= mantenir ouverte la fenetre
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			loop = False 
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				loop = False # ESC
	screen.fill((255,255,255))		#
	temps += clock.tick(60) / 1000.0 	#implementation du cronometre
	text = "Playtime:%d"%temps		#
	printvaisseau(screen,a)
	for z in listprot:
		z.move(0.1, 10, 10, 60, 0, width, a.diametre)
	printallprotein(screen,listprot)
	pygame.display.set_caption(text)
	pygame.display.flip()
	

# Fermer Pygame.  
pygame.quit()
