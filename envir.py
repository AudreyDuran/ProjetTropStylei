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
	#nbReaction : compte le nombre de reactions qui ont eu lieu

	def __init__(self, taille_trou, position_trou, diametre, debut, fin, vitesse_max_flux):
		self.taille_trou = taille_trou
		self.position_trou = position_trou
		self.vitesse_max_flux = vitesse_max_flux
		self.longuer=fin-debut 
		self.diametre = diametre
		self.debut=debut
		self.fin = fin

		self.compteurFlux = 0
		self.dt = 0.1

		self.dicoProt={}
		self.dicoProt['VIIa']=[]#1 (cree a la blessure)
		self.dicoProt['TF']=[]#cree a la blessure(0 de base)
		self.dicoProt['X']=[]#1
		self.dicoProt['VIIa-TF']=[]#0 #au trou
		self.dicoProt['prothrombine']=[]#1
		self.dicoProt['Xa']=[]#0 
		self.dicoProt['V']=[]#1
		self.dicoProt['Va']=[]#0
		self.dicoProt['fibrinogene']=[]#1
		self.dicoProt['thrombine']=[]#0
		self.dicoProt['fibrine']=[]#0
		self.dicoProt['plaquette']=[]#11



		self.dicoRel={}

		#dernier attribut : move=True ou False (par rapport a la cle)
		self.dicoRel['VIIa']=(1,'TF','VIIa-TF','c',True)
		self.dicoRel['TF']=(1,'VIIa','VIIa-TF','c',False)
		self.dicoRel['X']=(1,'VIIa-TF','Xa','p',True)
		self.dicoRel['VIIa-TF']=(1,'X','VIIa-TF','p',False)
		self.dicoRel['prothrombine']=(1,'Xa','thrombine','p',True)
		#Xa + prothrombine = thrombine
		#Xa + V = Va
		self.dicoRel['Xa']=(2,('prothrombine','V'),('Xa','Xa'),'p',True)
		self.dicoRel['V']=(1,'Xa','Va','p',True)
		self.dicoRel['Va']=(1,'thrombine','Va','p',True)
		self.dicoRel['fibrinogene']=(1,'thrombine','fibrine','p',True)
		self.dicoRel['thrombine']=(1,'fibrinogene','thrombine','p',True)
		self.dicoRel['fibrine']=(0,'plaquette','fibrine','p',True)
		self.dicoRel['plaquette']=(0,'p',True)


		#dictionnaire contient les tailles de chaque type de prot
		#rempli au hasard pour le moment, a changer apres!!
		self.dicoTaille={}

		self.dicoTaille['VIIa']=7
		self.dicoTaille['TF']=8
		self.dicoTaille['X']=7
		self.dicoTaille['VIIa-TF']=8
		self.dicoTaille['prothrombine']=9
		self.dicoTaille['Xa']=7
		self.dicoTaille['V']=5
		self.dicoTaille['Va']=5
		self.dicoTaille['fibrinogene']=5
		self.dicoTaille['thrombine']=9
		self.dicoTaille['fibrine']=5
		self.dicoTaille['plaquette']=20


		#dictionnaire contient les couleurs dans lesquelles seront dessinees les proteines
		#couleur a mettre en tuple (r,g,b)
		self.dicoCouleur={}

		self.dicoCouleur['VIIa']=(0,0,255)
		self.dicoCouleur['TF']=(255,55,155)
		self.dicoCouleur['X']=(255,0,0)
		self.dicoCouleur['VIIa-TF']=(10,0,0)
		self.dicoCouleur['prothrombine']=(0,255,0)
		self.dicoCouleur['Xa']=(0,0,0)
		self.dicoCouleur['V']=(255,90,0)
		self.dicoCouleur['Va']=(255,0,90)
		self.dicoCouleur['fibrinogene']=(180,160,73)
		self.dicoCouleur['thrombine']=(184,134,11)
		self.dicoCouleur['fibrine']=(230,210,123)
		self.dicoCouleur['plaquette']=(155,155,155)

		self.blessure=False
		self.temps=0.0
		self.venin=int(sys.argv[1])
		self.vitesse_lim=30
		self.nbReaction=0

		self.listPlaquetteActivees=[]


		self.dicoProt['Venin']=[]
		self.dicoCouleur['Venin']=(19,60,19)
		self.dicoTaille['Venin']= 10

		if self.venin>0:
			if self.venin==1:
				self.dicoRel['V']=(2,('Xa','Venin'),('Va','Va'),'p',True)
				self.dicoRel['Venin']=(1,'Va','Venin','p',True)
			if self.venin==2:
				self.dicoRel['Xa']=(3,('prothrombine','V','Venin'),('thrombine','Va','X'),'p',True)
				self.dicoRel['Venin']=(1,'Xa','Venin','p',True)
				self.dicoCouleur['Venin']=(219,160,19)


	#----------------------------------------------------------------------------------------------------
	#										 prot
	#----------------------------------------------------------------------------------------------------

	#cree le nombre de proteines indique pour chaque type de proteine

	def prot(self,fibrine,Va,prothrombine,Xa,plaquette,fibrinogene,thrombine,VIIaTF,V,TF,X,VIIa):
		print self.dicoProt.keys()
		l=[fibrine,Va,0,prothrombine,Xa,plaquette,fibrinogene,thrombine,VIIaTF,V,TF,X,VIIa] #12 elements dans la liste
		for i,prot in enumerate(self.dicoProt.keys()): #pour chaque type de prot
			for j in xrange(l[i]): #pour le nb de prot voulu pour ce type de prot
				#on cree la prot et on l'ajoute dans la liste correspondante
				self.dicoProt[prot].append(protein(self.dicoTaille[prot], random.random()*self.fin, random.random()*self.fin))
		d=len(self.dicoProt["TF"]);q=0.5
		for i in self.dicoProt["TF"]:
			if d>0:
				i.x=self.position_trou+q*self.taille_trou/d
				i.y=self.diametre+5
				i.activation=True
				q=q+1

	#----------------------------------------------------------------------------------------------------
	#										      TF
	#----------------------------------------------------------------------------------------------------

#expose le TF
	def TF(self):
		if(self.blessure):
			for i in self.dicoProt["TF"]:
				i.y=self.diametre-i.rayon-10
				i.activation=True
			if self.venin:
				for i in xrange(40):# nombre completement aleatoire
					self.dicoProt['Venin'].append(protein(self.dicoTaille['Venin'], self.position_trou+random.random()*self.taille_trou, self.diametre-self.dicoTaille['Venin']-30))


	#----------------------------------------------------------------------------------------------------
	#										 printvaisseau
	#----------------------------------------------------------------------------------------------------
	# dessine le vaisseau et le trou

	def printvaisseau(self,surface):
		pygame.draw.rect(surface,(200,40,40),((0,10),(self.longuer,10)),0)
		pygame.draw.rect(surface,(200,40,40),((0,self.diametre+10),(self.longuer,10)),0)
		if self.blessure:
			pygame.draw.rect(surface,(255,55,155),((self.position_trou,self.diametre+10),(self.taille_trou,15)),0)
	#----------------------------------------------------------------------------------------------------
	#										 printallprotein
	#----------------------------------------------------------------------------------------------------
	#dessine toutes les proteines dans la liste prot total


	def printallprotein(self,surface,font1,font2):#dessine toutes les proteines dans la liste prot total
		i=0
		surface.blit(font1.render("Nb actuel /Nb initial ", 1, (0,0,0)), (10,self.diametre+30))			
		for z in self.dicoProt.keys():#on parcourt toutes les prot
			pygame.draw.circle(surface,self.dicoCouleur[z],(100*i+20,self.diametre+60), 15,0)
			surface.blit(font2.render(z, 1, (0,0,0)), (100*i+20,self.diametre+80))
			surface.blit(font1.render("%d / %d"%(len(self.dicoProt[z]),self.linit[i]), 1, (0,0,0)), (100*i+20,self.diametre+90))
			i=i+1
			for y in self.dicoProt[z]:
				pygame.draw.circle(surface,self.dicoCouleur[z],(int(y.x),int(y.y+20)), y.rayon,1-y.activation)
				#surface.blit(font1.render(z, 1, self.dicoCouleur[z]), (int(y.x),int(y.y+20)))


	#----------------------------------------------------------------------------------------------------
	#									  moveAll_avant
	#----------------------------------------------------------------------------------------------------
	#mouvement de toutes les proteines avant qu'il n'y ait la breche

	def moveAll_avant(self):
		for typeProt,l in self.dicoProt.items(): #on parcourt chaque liste de prot (l=liste d'un type de prot)
			if typeProt=='TF':
				a=0
			else:
				for i in xrange(len(l)):
					l[i].move_avant(self.dt, self.vitesse_lim, self.debut, self.fin, self.diametre)
		
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

			#traitement special des plaquettes qui doivent pas sortir par le trou mais y rester
			if typeProt=='plaquette':
				for i in xrange(len(l)): # pour chaque facteur tissulaire
					if l[i].activation==False: #si pas deja activee
						if l[i].x>self.position_trou and l[i].x < self.position_trou + self.taille_trou : #si plaquette dans intervalle du trou +- le rayon
							if l[i].y > self.diametre - l[i].rayon - 50 and self.blessure: #si proche du trou en y (-10= aleatoire, a modifier apres)
								#alors va se fixer et rester la
								l[i].y=self.diametre#sur le trou (on garde le meme x)
								l[i].activation=True #alors plaquette active
								self.listPlaquetteActivees.append(l[i])

					if l[i].activation== False: #si tjrs pas activee
						#pas de compteur pour les plaquettes ! :))) car sortent pas
						l[i].move(self.dt, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre,self.vitesse_max_flux,self.listPlaquetteActivees)


			else: #si pas des plaquettes
				for i in xrange(len(l)): #on regarde chaque prot de cette liste  (l[i]=une prot de cette liste d'un type)

					if l[i].activation==False: #si est pas deja activee (auquel cas ne peut pas bouger)
						move = True #de base peut bouger, sauf si rencontre une prot ac qui peut reagir
						prot = 0 #proteine avec qui va reagir 
						distance = self.fin*self.diametre  #distance entre les 2 prot initialisee tres grande

						if self.dicoRel[typeProt][0]==0:
							self.compteurFlux+=l[i].move(self.dt, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre,self.vitesse_max_flux,self.listPlaquetteActivees)


						if self.dicoRel[typeProt][0]==1: #si peut reagir qu'avec un type de proteine
							for j in self.dicoProt[self.dicoRel[typeProt][1]]: #pour chaque prot de liste des prot avec qui peut reagir (j=type prot)
								if l[i].detection(j)== True:  #si detecte une des prot avec qui peut reagir
									if l[i].distance(j)<distance: #pour que reagisse seulement avec la prot la plus proche
										move = False
										prot=j
										distance=l[i].distance(j)

							if move == True: #si va bouger, a rencontre aucune prot ac qui peut reagir (regarder apres fin boucle for)

								self.compteurFlux+=l[i].move(self.dt, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre,self.vitesse_max_flux,self.listPlaquetteActivees)

							if move == False: #si a rencontre une prot donc va reagir
								#l[i].activation=True #on active les 2 prot
								#prot.activation=True 
								if not prot in lmemoire[2]:
									lmemoire[0].append(typeProt)
									lmemoire[1].append(l[i])
									lmemoire[2].append(prot)


						if self.dicoRel[typeProt][0]>1: #si peut reagir avec 2 types de prot
							for reactif in self.dicoRel[typeProt][1]: #pour chacun des reactifs ac qui peut reagir
								for j in self.dicoProt[reactif]:
									if l[i].detection(j)==True:
										if l[i].distance(j)<distance:
											move=False
											prot=j
											distance=l[i].distance(j)
							if move == True:
								self.compteurFlux+=l[i].move(self.dt, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre, self.vitesse_max_flux,self.listPlaquetteActivees)
							
							if move == False:
								#l[i].activation=True #on active les 2 prot
								#prot.activation=True

								#on verifie qu'une autre proteine de la meme liste n'a pas deja reagi avec cette prot j
								if not prot in lmemoire[2]:
									lmemoire[0].append(typeProt)
									lmemoire[1].append(l[i])
									lmemoire[2].append(prot)



				map(self.reaction,lmemoire[0],lmemoire[1],lmemoire[2])



	#si rencontre pls prot ac qui peut reagir !!

	#----------------------------------------------------------------------------------------------------
	#									  reaction
	#----------------------------------------------------------------------------------------------------
	#cree les nouvelles prot ou complexes
	#enleve les proteines qui ont reagit de leur liste de prot
	#typeProt=type d'une des prot qui reagit (en string)
	#prot et prot 2 = objets proteines qui reagissent
	#(prot est une proteine de type typeProt)

	#rq : finalement pas de disctinction entre complexe et proteine car posait pb d'avoir un tuple de 2 prot et non une prot dans la liste des 
	#proteines complexees (notamment pour prot.x, un tuple a pas d'attribut x)
	#il faudra, dans la methode d'affichage, faire 2 boules quand c'est un complexe

	def reaction(self,typeProt,prot,prot2):
		self.nbReaction+=1
#		print self.nbReaction, typeProt
		if self.dicoRel[typeProt][0]==1: #si peut reagir qu'avec un type de proteine
			#print "1"
			#on cree la nouvelle proteine qui aura comme cord la moyenne des coords des 2 autres prot
			p = protein(self.dicoTaille[self.dicoRel[typeProt][1]], (prot.x+prot2.x)/2, (prot.y+prot2.y)/2)

			#print typeProt,self.dicoRel[typeProt][1]
			#print "dicoRel",self.dicoRel[self.dicoRel[typeProt][2]]
			if self.dicoRel[self.dicoRel[typeProt][2]][-1]==False:
				p.activation=True

			self.dicoProt[self.dicoRel[typeProt][2]].append(p) #on ajoute la nouvelle prot creee a son tableau 

			self.dicoProt[typeProt].remove(prot) #on enleve du tableau la proteine qui se transforme 
			#print typeProt,"reagit avec", self.dicoRel[typeProt][1] #X
			#print "dicoPb",self.dicoProt[self.dicoRel[typeProt][1]]
			
		if self.dicoRel[typeProt][0]>1: #si peut reagir ac plus d'une proteine
			#print "2"
			if prot2 in self.dicoProt[self.dicoRel[typeProt][1][0]]: #on cherche si prot ac qui reagit est son premier ou deuxieme reactif
				p = protein(self.dicoTaille[self.dicoRel[typeProt][1][0]], (prot.x+prot2.x)/2, (prot.y+prot2.y)/2)

				if self.dicoRel[self.dicoRel[typeProt][2][0]][-1]==False:
					p.activation=True

				self.dicoProt[self.dicoRel[typeProt][2][0]].append(p) #on ajoute la nouvelle prot au bon tableau

				
			if prot2 in self.dicoProt[self.dicoRel[typeProt][1][1]]:
				p = protein(self.dicoTaille[self.dicoRel[typeProt][1][1]], (prot.x+prot2.x)/2, (prot.y+prot2.y)/2)


				if self.dicoRel[self.dicoRel[typeProt][2][1]][-1]==False:
					p.activation=True
				self.dicoProt[self.dicoRel[typeProt][2][1]].append(p)  #on ajoute la nouvelle prot au bon tableau
			self.dicoProt[typeProt].remove(prot) 
#		self.dicoRel['V']=(1,'Xa','Va','p',True)
#		self.dicoRel['plaquette']=(0,'p',True)
#		self.dicoRel['Xa']=(2,('prothrombine','V'),('thrombine','Va'),'p',True)

	#----------------------------------------------------------------------------------------------------
	#										 run
	#----------------------------------------------------------------------------------------------------

	def run(self):
		self.linit=[]
		for z in self.dicoProt.keys():
			self.linit.append(len(self.dicoProt[z]))
		once=False
	# Initialize Pygame.
		pygame.init()
	# Set size of pygame window. width=a.longuer; heigth=a.diametre+40
		screen=pygame.display.set_mode((self.longuer,self.diametre+120))
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
		pygame.font.init()
		deffont = pygame.font.SysFont(pygame.font.get_default_font(),20)
		font2 = pygame.font.SysFont(pygame.font.get_default_font(),15)
		loop=True
		ent=-1
		f=open("fibrine0.txt","w")
		f.write("t\tsort\n")
		while loop: #loop= mantenir ouverte la fenetre
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					loop = False 
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						loop = False # ESC
			screen.fill((255,255,255))		#
			self.temps += clock.tick(60) / 1000.0 	#implementation du cronometre
			text = "Playtime:%d\tReactions:%d\tProteines sortant:%d"%(self.temps,self.nbReaction,self.compteurFlux)		#
			if self.temps>5 and not once:
				self.blessure=True
				self.TF()
				once=True
			self.printvaisseau(screen)
			self.printallprotein(screen,deffont,font2) #on dessine chaque prot selon le type de prot
			if ent!=int(self.temps):
				ent=int(self.temps)
				f.write("%d\t%d\n"%(ent,len(self.dicoProt['fibrine'])))
			pygame.display.set_caption(text)
			pygame.display.flip()
			if not self.blessure:
				self.moveAll_avant() #on fait bouger toutes les prot
			else:
				self.moveAll()
			if self.temps>60:
				f.close()
				loop=False
			#print len(self.dicoProt['TF'])
