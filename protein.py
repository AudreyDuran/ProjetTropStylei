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






	def __repr__(self):
		return "(x=%lg, y=%lg, activation=%r, rayon=%lg)" %(self.x, self.y, self.activation, self.rayon)






	#renvoie true si la prot peut detecter la prot a, false sinon 
	def detection(self, a):

		d = distance(self,a)

		if d <= self.rayon:
			a.activation=True
			self.activation = True
			return True

		else:
			return False


	#renvoie la distance entre deux proteines
	def distance(sef,a):
		return math.sqrt((self.x-a.x)**2 + (self.y - a.y)**2)







	# defini une vitesse supplementaire lorsque la proteine rentre dans le flux de sang qui part par la blessure
	def attraction(self, dt, position_trou, taille_trou, vitesse_max_flux, diametre):

		# definition de variable qu on utilisera plus tard
		a = position_trou - taille_trou



		# calcul la longueur de la base du petit triangle rectangle dont le gros est forme par le sommet du flux avec la paroi
		# haute du vaiseau puis prolongement orthogonal sur la paroi basse et revenir sur un des bouts de la blessure (theoreme
		# de thales)
		b = taille_trou*self.y/diametre


		# si la proteine est dans le parallelogramme defini par [debut trou, fin trou, haut du flux partant de la fin du trou,
		# haut du flux partant du debut du trou]
		if self.x > b + a:
			if self.x < b + position_trou:
				# distance entre l hypothenus et la proteine en x
				d_inter = self.x - b - a

				if self.y < diametre:
					# inverse de la distance entre proteine et l endroit ou elle toucherai la blessure si elle suivait la flux parallelement
					d = 1/math.hypot( (self.x - (position_trou + d_inter)), (self.y-diametre) )
					if d <= 1:
						# pour que la vitesse soit inversement proportionnel a d
						self.x += dt * ( (position_trou+d_inter) - self.x )*d * d * vitesse_max_flux
						self.y += dt * ( diametre - self.y )*d * d * vitesse_max_flux

					if d > 1:
						# pour ne pas que cela depasse la vitesse max
						self.x += dt * ( (position_trou+d_inter) - self.x )*d * vitesse_max_flux 
						self.y += dt * ( diametre - self.y )*d * vitesse_max_flux




				# quand la proteine est sortie du vaisseau
				else:
					c = taille_trou*(diametre+200)/diametre
					d = 1/math.hypot( (self.x - (a+c+d_inter)), (self.y - (diametre+200)) )

					self.x += dt * ( (a+c+d_inter)-self.x )*d * vitesse_max_flux 
					self.y += dt * ( (diametre+200)-self.y )*d * vitesse_max_flux









	# vitesse max flux et la vitesse du flux qui part vers la blessure
	def move(self, dt, vitesse_lim, position_trou, taille_trou, debut, fin, diametre, vitesse_max_flux):

		if self.activation == False :

			self.x += dt * random.uniform(-1/16*vitesse_lim, vitesse_lim)
			self.y += dt * random.uniform(-vitesse_lim, vitesse_lim)


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
				self.y = random.uniform(0, diametre)



			# Quand elle sort par le trou, on considere a partir d un moment que elle ne soit plus en contact avec le reste lorsqu
			# elle sort d un certain perimetre ici on aurait un cercle de rayon 150
			if self.y > diametre:
				if math.sqrt((self.x - position_trou+taille_trou/2)**2 + (self.y - diametre)**2) > math.sqrt(150):
					self.x = debut
					self.y = random.uniform(0, diametre)


					# Pour le comptage des proteine qui sont sortie du cercle
					return 1


			# pour la proteine qui part dans le flux secondaire
			if self.x > position_trou - taille_trou:
				if self.x < position_trou + taille_trou:
					self.attraction(dt, position_trou, taille_trou, vitesse_max_flux, diametre)


			# Pour le comptage des proteine qui ne sont pas sortie du cercle
			return 0







		




# move(self, dt, vitesse_lim, position_trou, taille_trou, debut, fin, diametre, vitesse_max_flux):

p = protein(20, random.random(), random.random())
a = protein(40, random.random(), random.random())

f = open("position.txt", "w")
for t in xrange(5000):
	p.move(0.1, 20, 100, 60, 0, 1000, 100, 200)
	# a.move(0.1, 20, 10, 60, 0, 1000, 100, 20)

	# f.write("%f %f %f %f\n" %(p.x, p.y, a.x, a.y))

f.close()

f = open("fichiergnuplot","w")
f.write('plot \"position.txt\" using 1:2 \n')
f.write('replot \"position.txt\" using 3:4\n')

f.close()
# os.system("gnuplot fichiergnuplot --persist")