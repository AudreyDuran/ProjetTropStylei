import numpy
import math
import random

import os

class protein:
	def __init__(self, rayon, x, y):
		
		self.x = x
		self.y = y
		self.rayon = rayon

	def detection(self, a):

		d = math.sqrt((self.x-a.x)**2 + (self.y - a.y)**2)

		if d <= self.rayon:
			return True

		else:
			return False


	def move(self, dt, vitesse_lim, position_trou, taille_trou, debut, fin, diametre):

		self.x += dt * random.uniform(-1/16*vitesse_lim, vitesse_lim)
		self.y += dt * random.uniform(-vitesse_lim, vitesse_lim)

		if self.y < 0 :
			self.y = 0

		if self.x < 0:
			self.x = 0

		if self.y > diametre:
			if self.x < position_trou :
				if self.x > (position_trou+taille_trou) : 
					self.y = diametre

		if self.x > fin :
			self.x = debut
			self.y = random.uniform(0, diametre)







p = protein(20, random.random(), random.random())
a = protein(40, random.random(), random.random())


f = open("position.txt", "w")
for t in xrange(5000):
	p.move(0.1, 20, 10, 60, 0, 100, 100)
	a.move(0.1, 20, 10, 60, 0, 100, 100)

	f.write("%f %f %f %f\n" %(p.x, p.y, a.x, a.y))

f.close()

f = open("fichiergnuplot","w")
f.write('plot \"position.txt\" using 1:2 \n')
f.write('replot \"position.txt\" using 3:4\n')

f.close()
os.system("gnuplot fichiergnuplot --persist")