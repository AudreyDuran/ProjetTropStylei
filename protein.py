import numpy
import math
import random
from envir import *

envire = envir(20,500)

class protein:
	def __init__(self, rayon, x = (envire.fin - envire.debut)*random.random() - envire.fin, y = envire.diametre*random.random()):
		
		self.x = x
		self.y = y
		self.rayon = rayon

		self.diametre = envire.diametre
		self.position_trou = envire.position_trou
		self.taille_trou = envire.position_trou

		self.debut = envire.debut
		self.fin = envire.fin

	def detection(self, a):

		d = math.sqrt((self.x-a.x)**2 + (self.y - a.y)**2)

		if d <= self.rayon:
			return True

		else:
			return False


	def move(self, dt, vitesse_lim):

		self.x += dt * vitesse_lim * ( 5/4 * random.random() - 1 ) # 5/4 pour dire que la proteine peut revenir
		self.y += dt * vitesse_lim * ( 2 * random.random() - 1 ) # 2 pour que la proteine monte ou desend

		if self.y < 0 :
			self.y = 0

		if self.y > self.diametre & (self.x < self.position_trou | self.x > (self.position_trou+self.taille_trou) : 
			self.y = self.diametre

		if self.x > self.fin :
			self.x = self.debut
			self.y = self.diametre*random.random()


p = protein(200)
a = protein(400)

print p.x
