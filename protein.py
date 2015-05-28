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







	def detection(self, a):

		d = math.sqrt((self.x-a.x)**2 + (self.y - a.y)**2)

		if d <= self.rayon:
			a.activation=True
			self.activation = True
			return True

		else:
			return False







	# defini une vitesse supplementaire lorsque la proteine rentre dans le flux de sang qui part par la blessure
	def attraction(self, dt, position_trou, taille_trou, vitesse_max_flux, diametre):
		# definition de variable qu on utilisera plus tard
		angle = math.cos(math.atan(taille_trou/float(diametre)))
		a = position_trou - taille_trou
		b = position_trou+taille_trou/2

		print self.y/angle, self.y


		# si la proteine est dans le parallelogramme defini par [debut trou, fin trou, ]
		if self.x > self.y/angle + a:
			if self.x < self.y/angle + position_trou:
				if self.y > diametre:

					d = math.sqrt((self.x-b)**2 + (self.y-diametre)**2)

					if d >= 1:
						self.x += (b-self.x)/d * 1/d * vitesse_max_flux   # pour que la vitesse soit inversement proportionnel a d
						self.y += (diametre-self.y)/d * 1/d * vitesse_max_flux

					elif d>0:
						self.x += (b-self.x)/d * vitesse_max_flux #pour ne pas que cela depasse la vitesse max
						self.y += (diametre-self.y)/d * vitesse_max_flux









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
	p.move(0.1, 20, 100, 60, 0, 1000, 100, 20)
	# a.move(0.1, 20, 10, 60, 0, 1000, 100, 20)

	# f.write("%f %f %f %f\n" %(p.x, p.y, a.x, a.y))

f.close()

f = open("fichiergnuplot","w")
f.write('plot \"position.txt\" using 1:2 \n')
f.write('replot \"position.txt\" using 3:4\n')

f.close()
# os.system("gnuplot fichiergnuplot --persist")