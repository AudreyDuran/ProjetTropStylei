import numpy
import math
import sys
import pygame
import random as r
from protein import *

class envir:


	#----------------------------------------------------------------------------------------------------
	#										Constructeur
	#----------------------------------------------------------------------------------------------------

	#taille trou : longueur du trou
	#position_trou: position x du trou (par rapport au debut du vaisseau)
	#diametre : diametre du vaisseau (longueur en y)
	#debut: indice x de debut du vaisseau (par rapport a la fenetre)
	#fin: indice x de fin du vaisseau (y-x=longueur du vaisseau)
	#protPermanentes : liste des prot seront dans le sang a chaque essai et seront affichees
	#protTotales : liste de ttes  les proteines dans le sang
	#dicoRel : contient pour chaque prot ( avec cb de prot reagit, (affinite,devient), 'c' si forme cplexe 'p' si forme prot)
	#dicoProt : dico contient toutes les proteines (avec en cle leur nom en string)

	def __init__(self, taille_trou, position_trou, diametre, debut, fin, vitesse_max_flux):
		self.taille_trou = taille_trou
		self.position_trou = position_trou
		self.vitesse_max_flux = vitesse_max_flux
		self.longueur=fin-debut
		self.diametre = diametre
		self.debut=debut
		self.fin = fin

		self.compteur = 0
		self.dt = 0.1

		self.dicoProt={}

		self.dicoProt['fVIIa']=[]
		self.dicoProt['TF']=[]
		self.dicoProt['X']=[]
		self.dicoProt['VIIa-TF']=[]
		self.dicoProt['prothrombine']=[]
		self.dicoProt['Xa']=[]
		self.dicoProt['V']=[]
		self.dicoProt['fibrinogene']=[]
		self.dicoProt['thrombine']=[]
		self.dicoProt['fibrine']=[]
		self.dicoProt['plaquette']=[]



		self.dicoRel={}

		self.dicoRel['fVIIa']=(1,'TF','VIIa-TF','c')
		self.dicoRel['TF']=(1,'fVIIa','VIIa-TF','c')
		self.dicoRel['X']=(1,'VIIa-TF','Xa','p')
		self.dicoRel['VIIa-TF']=(1,'X','Xa','p')
		self.dicoRel['prothrombine']=(1,'Xa','thrombine','p')
		#Xa + prothrombine = thrombine
		#Xa + V = Va
		self.dicoRel['Xa']=(2,('prothrombine','V'),('thrombine','Va'),'p')
		self.dicoRel['V']=(1,'Xa','Va','p')
		self.dicoRel['fibrinogene']=(1,'thrombine','fibrine','p')
		self.dicoRel['thrombine']=(1,'fibrinogene','fibrine','p')
#
		self.dicoRel['fibrine']=(0,'p')
		self.dicoRel['plaquette']=(0,'p')


		#dictionnaire contient les tailles de chaque type de prot
		#rempli au hasard pour le moment, a changer apres!!
		self.dicoTaille={}

		self.dicoTaille['fVIIa']=[7]
		self.dicoTaille['TF']=[8]
		self.dicoTaille['X']=[7]
		self.dicoTaille['VIIa-TF']=[8]
		self.dicoTaille['prothrombine']=[9]
		self.dicoTaille['Xa']=[7]
		self.dicoTaille['V']=[5]
		self.dicoTaille['fibrinogene']=[5]
		self.dicoTaille['thrombine']=[9]
		self.dicoTaille['fibrine']=[5]
		self.dicoTaille['plaquette']=[20]

		#dictionnaire contient les couleurs dans lesquelles seront dessinees les proteines
		#couleur a mettre en tuple (r,g,b)
		self.dicoCouleur={}

		self.dicoCouleur['fVIIa']=(0,0,255)
		self.dicoCouleur['TF']=(255,255,0)
		self.dicoCouleur['X']=(255,0,0)
		self.dicoCouleur['VIIa-TF']=(10,0,0)
		self.dicoCouleur['prothrombine']=(0,255,0)
		self.dicoCouleur['Xa']=(0,0,0)
		self.dicoCouleur['V']=(0,0,0)
		self.dicoCouleur['fibrinogene']=(0,0,0)
		self.dicoCouleur['thrombine']=(0,0,0)
		self.dicoCouleur['fibrine']=(0,0,0)
		self.dicoCouleur['plaquette']=(155,155,155)


		self.temps=0.0
		self.venin=sys.argv[1]
		self.vitesse_lim=20
		
	#----------------------------------------------------------------------------------------------------
	#										 prot
	#----------------------------------------------------------------------------------------------------

	#cree le nombre de proteines indique pour chaque type de proteine

	def prot(self,fVIIa,TF,X,VIIaTF,prothrombine,Xa,V,fibrinogene,thrombine,fibrine,plaquette):
		l=[fVIIa,TF,X,VIIaTF,prothrombine,Xa,V,fibrinogene,thrombine,fibrine,plaquette] #11 elements dans la liste
		for i,prot in enumerate(self.dicoProt.keys()): #pour chaqye type de prot
			for j in xrange(l[i]): #pour le nb de prot voulu pour ce type de prot
				#on cree la prot et on l'ajoute dans la liste correspondante
				self.dicoProt[prot].append(protein(self.dicoTaille[prot][0], random.random()*self.fin, random.random()*self.fin))

	#----------------------------------------------------------------------------------------------------
	#										 printvaisseau
	#----------------------------------------------------------------------------------------------------

	def printvaisseau(self,surface):# dessine le vaisseau et le trou
		pygame.draw.rect(surface,(200,40,40),((0,10),(self.longueur,10)),0)
		pygame.draw.rect(surface,(200,40,40),((0,self.diametre+10),(self.longueur,10)),0)
		pygame.draw.rect(surface,(255,55,155),((self.position_trou,self.diametre+10),(self.taille_trou,15)),0)

	#----------------------------------------------------------------------------------------------------
	#										 printallprotein
	#----------------------------------------------------------------------------------------------------


	def printallprotein(self,surface):#dessine toutes les proteines dans la liste prot total
		for z in self.dicoProt.keys():#on parcourt toutes les prot
			for y in self.dicoProt[z]:
				pygame.draw.circle(surface,self.dicoCouleur[z],(int(y.x),int(y.y+20)), y.rayon,y.activation)



	#----------------------------------------------------------------------------------------------------
	#									  moveAll
	#----------------------------------------------------------------------------------------------------

	#calcule la nouvelle position de toutes les proteines
	def moveAll(self):
		for typeProt,l in self.dicoProt.items(): #on parcourt chaque liste de prot (l=liste d'un type de prot)

			lmemoire=[]  #liste memoire cree pour pas supprimer des proteine pdt qu'on les parcourt dans le for
			lmemoire.append([])
			lmemoire.append([])
			lmemoire.append([])

			for i in xrange(len(l)): #on regarde chaque prot de cette liste  (l[i]=une prot de cette liste d'un type)
				print typeProt,l[i]

				if l[i].activation==False: #si est pas deja activee (auquel cas ne peut pas bouger)
					move = True #de base peut bouger, sauf si rencontre une prot ac qui peut reagir
					prot = 0 #proteine avec qui va reagir 
					distance = self.fin*self.diametre  #distance entre les 2 prot initialisee tres grande

					if self.dicoRel[typeProt][0]==1: #si peut reagir qu'avec un type de proteine
						for j in self.dicoProt[self.dicoRel[typeProt][1]]: #pour chaque prot de liste des prot avec qui peut reagir (j=type prot)
							if l[i].detection(j)== True:  #si detecte une des prot avec qui peut reagir
								if l[i].distance(j)<distance: #pour que reagisse seulement avec la prot la plus proche
									move = False
									prot=j
									distance=l[i].distance(j)

						if move == True: #si va bouger, a rencontre aucune prot ac qui peut reagir (regarder apres fin boucle for)

							l[i].move(self.dt, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre,self.vitesse_max_flux)

						if move == False: #si a rencontre une prot donc va reagir
							l[i].activation=True #on active les 2 prot
							prot.activation=True
							#self.reaction(typeProt,l[i],prot)  
							lmemoire.append((typeProt,l[i],prot))


					if self.dicoRel[typeProt][0]>1: #si peut reagir avec 2 types de prot
						for reactif in self.dicoRel[typeProt][1]: #pour chacun des reactifs ac qui peut reagir
							for j in self.dicoProt[reactif]:
								if l[i].detection(j)==True:
									if l[i].distance(j)<distance:
										move=False
										prot=j
										distance=l[i].distance(j)
						if move == True:
							l[i].move(self.dt, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre, self.vitesse_max_flux)
						
						if move == False:
							l[i].activation=True #on active les 2 prot
							prot.activation=True
							lmemoire[0].append(typeProt)
							lmemoire[1].append(l[i])
							lmemoire[2].append(prot)


							#self.reaction(typeProt,l[i],prot)


			print lmemoire
			map(self.reaction,lmemoire[0],lmemoire[1],lmemoire[2])



	#si rencontre pls prot ac qui peut reagir !!

	#----------------------------------------------------------------------------------------------------
	#									  reaction
	#----------------------------------------------------------------------------------------------------
	#cree les nouvelles prot ou complexes
	#enleve les proteines qui ont reagit de leur liste de prot
	#typeProt=type d'une des prot qui reagit (en string)
	#prot et prot 2 = objets proteines qui reagissent

	#rq : finalement pas de disctinction entre complexe et proteine car posait pb d'avoir un tuple de 2 prot et non une prot dans la liste des 
	#proteines complexees (notamment pour prot.x, un tuple a pas d'attribut x)
	#il faudra, dans la methode d'affichage, faire 2 boules quand c'est un complexe

	def reaction(self,typeProt,prot,prot2):
		#on cree la nouvelle proteine qui aura comme cord la moyenne des coords des 2 autres prot
		p = protein(self.dicoTaille[self.dicoRel[typeProt][1]], (prot.x+prot2.x)/2, (prot.y+prot2.y)/2)

		self.dicoProt[typeProt].remove(prot) #on enleve du tableau la proteine qui se transforme 
		self.dicoProt[self.dicoRel[typeProt][1]].remove(prot2)  #on enleve l'autre prot qui reagit du tableau



	#----------------------------------------------------------------------------------------------------
	#										 run
	#----------------------------------------------------------------------------------------------------

	def run(self):
	# Initialize Pygame.
		pygame.init()
	# Set size of pygame window. width=a.longueur; heigth=a.diametre+40
		screen=pygame.display.set_mode((self.longueur,self.diametre+40))
	# Create empty pygame surface.
		background = pygame.Surface(screen.get_size())
	# Fill the background white color.
		background.fill((255, 255, 255))
	# Convert Surface object to make blitting faster.
		background = background.convert()
	# Copy background to screen (position (0, 0) is upper left corner).
		screen.blit(background, (0,0))
		clock = pygame.time.Clock()
		#recuperer la case cochee par l'utilisateur (parse event en c++)
		#creer toutes les proteines qu'il faut (de base mettre des attributs de classe avec la compo de chaque venin?)


		loop=True
		while loop: #loop= mantenir ouverte la fenetre
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					loop = False 
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						loop = False # ESC
			screen.fill((255,255,255))		#
			self.temps += clock.tick(60) / 1000.0 	#implementation du cronometre
			text = "Playtime:%d"%self.temps		#
			self.printvaisseau(screen)
			for z in self.dicoProt.keys():#on parcourt toutes les prot
				for y in self.dicoProt[z]:
# move(self, dt, vitesse_lim, position_trou, taille_trou, debut, fin, diametre, vitesse_max_flux):
					y.move(0.1, 10, self.position_trou, self.taille_trou, self.debut,self.fin, self.longueur, self.diametre)
			self.printallprotein(screen)#on dessine chaque prot selon le type de prot
			pygame.display.set_caption(text)
			pygame.display.flip()
			self.moveAll() #on fait bouger toutes les prot
