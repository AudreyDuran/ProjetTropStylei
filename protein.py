import numpy
import math
import random
from envir import *

envire = envir(20,500)

class protein:
	def __init__(self, rayon, x = envire.diametre*random.random(), y = envire.diametre*random.random()):
		
		self.x = x
		self.y = y
		self.rayon = rayon

	def detection(self, a):

		d = (self.x-a.x)**2 + (self.y - a.y)**2

		if d <= self.rayon:
			return True

		else:
			return False


p = protein(200)
a = protein(400)

print p.x
