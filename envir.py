import numpy
import math
import random

class envir:
    def __init__(self, taille_trou, diametre):
    	self.taille_trou = taille_trou
    	self.diametre = diametre

    	self.paroi_basse = [[diametre, 100], [diametre, 200], [diametre, 200+taille_trou], [diametre, 10000]]

    	self.trou = [[diametre,200], [diametre,200+taille_trou]]

    	self.compteur = 0

    

    def update_paroi(self, x_plaquette, y_plaquette, taille_plaquette):
    	self.paroi_basse.append([[x_plaquette,y_plaquette], [x_plaquette,y_plaquette+taille_plaquette]])

    	self.compteur += 1


a = envir(50,500)
print a.paroi_basse
a.update_paroi(100+a.diametre-1, 199, 30)
print a.paroi_basse