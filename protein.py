import numpy
import math
import random

import os

class protein:
	def __init__(self, rayon, x, y):
		
		self.x = x
		self.y = y
		self.rayon = rayon

		self.activation = False

		# pour les plaquettes
		self.compte = 0
		self.tps = 0

		self.denature = False




	def __repr__(self):
		return "(x=%lg, y=%lg, activation=%r, rayon=%lg)" %(self.x, self.y, self.activation, self.rayon)



	#renvoie la distance entre deux proteines
	def distance(self,a):
		return math.sqrt((self.x-a.x)**2 + (self.y - a.y)**2)


	#renvoie true si la prot peut detecter la prot a, false sinon 
	def detection(self, a):

		if self.distance(a) <= self.rayon:
			return True

		else:
			return False

	# detection pour la fibrine
	def detection_fibrine(self, a, b):

		if self.distance(a) <= self.rayon:
			if self.distance(b) <= self.rayon:
				return True

		return False


	


	# compte le nombre de tour pour les plaquettes si elle n ont pas de fibrine pour les liees
	def compte_temps(self, tps_lim, tps):
		self.compte += 1

		if self.compte > tps_lim:
			self.activation=False
			self.tps +=1

			if self.tps > tsp:
				self.compte=0
				self.tps=0



	# defini une vitesse supplementaire lorsque la proteine rentre dans le flux de sang qui part par la blessure
	def attraction(self, dt, position_trou, taille_trou, vitesse_max_flux, diametre):

		# debut du flux en x
		a = float(position_trou - taille_trou)


		# calcul la longueur de la base du petit triangle rectangle dont le gros est forme par le sommet du flux avec la paroi
		# haute du vaiseau puis prolongement orthogonal sur la paroi basse et revenir sur un des bouts de la blessure (theoreme
		# de thales)
		b = taille_trou*self.y/float(diametre)

		#print self.x, b+a
		# si la proteine est dans le parallelogramme defini par [debut trou, fin trou, haut du flux partant de la fin du trou,
		# haut du flux partant du debut du trou]
		if self.x > b + a:
			if self.x < b + position_trou:
				# distance entre l hypothenus et la proteine en x
				d_inter = self.x - b - a

				if self.y < diametre:
					# inverse de la distance entre proteine et l endroit ou elle toucherai la blessure si elle suivait la flux parallelement
					d = 1/math.sqrt((self.x - (position_trou + d_inter))**2 + (self.y-diametre)**2 )
					if d <= 1:
						# pour que la vitesse soit inversement proportionnel a d
						self.x += dt * ( (position_trou+d_inter) - self.x )*d *d * vitesse_max_flux
						self.y += dt * ( diametre - self.y )*d*d * vitesse_max_flux

					if d > 1:
						# pour ne pas que cela depasse la vitesse max
						self.x += dt * ( (position_trou+d_inter) - self.x )*d * vitesse_max_flux 
						self.y += dt * ( diametre - self.y )*d * vitesse_max_flux




				# quand la proteine est sortie du vaisseau
				else:
					# encore theoreme de thales
					c = taille_trou*(diametre+200)/float(diametre)
					d = 1/math.hypot( (self.x - (a+c+d_inter)), (self.y - (diametre+200)) )

					self.x += dt * ( (a+c+d_inter)-self.x )*d * vitesse_max_flux 
					self.y += dt * ( (diametre+200)-self.y )*d * vitesse_max_flux





	def move_avant(self, dt, vitesse_lim, debut, fin, diametre):
		
		self.x += dt * random.uniform(0, vitesse_lim)
		self.y += dt * random.uniform(-2*vitesse_lim, 2*vitesse_lim)


		# Pour eviter qu elle sorte du vaiseau par le haut
		if self.y < self.rayon :
			self.y = self.rayon

		# pour eviter que les proteine ne sortent par la gauche
		if self.x < debut:
			self.x = debut


		# Pour eviter qu elle sorte du vaiseau en bas
		if self.y >= diametre-self.rayon:
				self.y = diametre - self.rayon
				

		# Quand elle arrivent a la fin
		if self.x >= fin :
			self.x = debut
			self.y = random.uniform(self.rayon, diametre-self.rayon)
			
			

	# Pas le temps mais le mettre dans envir (sinon cela rame) 
	# sert a arreter le move et mettre move_avant si toutes le caillot est formé sur la blessure
	def fin_coagulation(self, l_pla, position_trou, taille_trou):

		if l_pla!=False:
			l = [[i.x-i.rayon, i.x+i.rayon] for i in l_pla]
			l.sort()
			
			i=0

			# Pour faire la liste avec les proteines activees un intervalle continue avec la surface que couvre les proteines en x
			while i < len(l)-1:
				if l[i][1]>l[i+1][0]:
					l[i]=[l[i][0], l[i+1][1]]
					l.pop(i+1)
				else:
					i+=1

			if len(l) == 1 and l[0][0]<position_trou and l[0][1]>taille_trou+position_trou:
				return True

			else: 
				return False



	# vitesse max flux est la vitesse du flux qui part vers la blessure
	def move(self, dt, vitesse_lim, position_trou, taille_trou, debut, fin, diametre, vitesse_max_flux, l_pla=False):
		
		if len(l_pla) >150:
			self.move_avant(dt, vitesse_lim, debut, fin, diametre)
			return 0



		self.x += dt * random.uniform(0, vitesse_lim)
		self.y += dt * random.uniform(-2*vitesse_lim, 2*vitesse_lim)


		# Pour eviter qu elle sorte du vaiseau par le haut
		if self.y < self.rayon :
			self.y = self.rayon

		# pour eviter que les proteine sortent par la gauche
		if self.x < debut:
			self.x = debut

		# Pour eviter qu elle sorte du vaiseau tant qu il n y a pas le trou (a gauche du trou)
		if self.y >= diametre-self.rayon and self.x < position_trou:
			self.y = diametre - self.rayon
				
		# Pour eviter qu elle sorte du vaiseau tant qu il n y a pas le trou (a droite du trou)
		if self.y > diametre-self.rayon and self.x > position_trou + taille_trou:
			self.y = diametre - self.rayon

		# Quand elle arrivent a la fin
		if self.x >= fin :
			self.x = debut
			self.y = random.uniform(self.rayon, diametre-self.rayon)
			self.denature = False





		# pour la proteine qui part dans le flux secondaire
		if self.x > position_trou - taille_trou and self.x < position_trou + taille_trou:
			self.attraction(dt, position_trou, taille_trou, vitesse_max_flux, diametre)





		# Quand elle sort par le trou, on considere a partir d un moment que elle ne soit plus en contact avec le reste lorsqu
		# elle sort d un certain perimetre ici on aurait un cercle de rayon taille_trou/2
		if self.y > diametre-self.rayon:
			if ((self.x - (position_trou+taille_trou/2.))**2+(self.y - diametre)**2) > (taille_trou/2)**2 and self.y>diametre:
				self.x = debut
				self.y = random.uniform(self.rayon, diametre-self.rayon)

				# Pour le comptage des proteine qui sont sortie du cercle
				return 1

			else:
				if l_pla != False:
					for i in l_pla:
						if i.detection(self)==True and self.y < i.y:
							# print 'aa'
							self.y = diametre-i.rayon





		# Pour le comptage des proteine qui ne sont pas sortie du cercle
		return 0
		

p = protein(1, 5,6)
e = protein(1,6, 9)
f = protein(1,4,3)
g = protein(1,9, 5)


print p.fin_coagulation([p,e,f])

# dt, position_trou, taille_trou, vitesse_max_flux, diametre

# p = protein(0.1, 10, 5)
# p.attraction(0.1, 10, 10, 40, 10)

# e = protein(10, 30, 100)

# p = protein(10, 35, 105)
# p.move(0.1,10,10,50,0,100,100,50, [e])
# print p


# # move(self, dt, vitesse_lim, position_trou, taille_trou, debut, fin, diametre, vitesse_max_flux):

# p = protein(20, random.random(), random.random())
# a = protein(40, random.random(), random.random())

# f = open("position.txt", "w")
# for t in xrange(5000):
# 	p.move(0.1, 20, 100, 60, 0, 1000, 100, 200)
# 	# a.move(0.1, 20, 10, 60, 0, 1000, 100, 20)

# 	# f.write("%f %f %f %f\n" %(p.x, p.y, a.x, a.y))

# f.close()

# f = open("fichiergnuplot","w")
# f.write('plot \"position.txt\" using 1:2 \n')
# f.write('replot \"position.txt\" using 3:4\n')

# f.close()
# # os.system("gnuplot fichiergnuplot --persist")
