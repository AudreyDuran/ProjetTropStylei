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

class protein():#proteine type
	def __init__(self,r,x,y,i,a):
		self.x=x#position
		self.y=y
		self.rayon=r
		self.id=i #oui, un identifiant! Desole, mais c'est plus simple pour moi.
		self.activ=a	#Alors, pour dessiner les cercles, on peut choisir 0(plein) ou 1(vide)
		self.fonction=1
#Plein, comme inactive, vide comme active.
#Ce que je propose, on a 3 types de proteines: activee, inactivee et "detruit" par le venim
#Pour "detruit", on utilise cet attribut fonction. S'il devient zero, la proteine est toujours inactive.

once=0
def deactivate(t,listp,once):	# deactive toutes les proteines(comme un venim) apres 5 seconds
	if t<5 and once==0:	#juste un test
		for i in listp:
			i.fonction=0
		once=1

width=900; heigth=a.diametre+40 #l'hauteur est 40 a plus car je veut donner espessure 10 a chaque paroi + 10 de vide
color=[(255,255,255),(255,255,0),(200,0,128),(0,255,255),(0,255,0)]#vecteur de couleurs pour chaque couleur
temps=0.0

#liste de proteines aleatoires
listprot=[]
for i in xrange(10):
	listprot.append(protein(r.randint(1,20),r.randint(0,639),r.randint(0,a.diametre),r.randint(0,4),r.randint(0,1)))


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
		pygame.draw.circle(screen,color[protein.id],(protein.x,protein.y+20),protein.rayon,protein.activ*protein.fonction)


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
	printallprotein(screen,listprot)
	deactivate(temps,listprot,once)
	pygame.display.set_caption(text)
	pygame.display.flip()
	

# Fermer Pygame.  
pygame.quit()
