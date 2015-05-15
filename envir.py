import numpy
import math
import random

class envir:
    def __init__(self, taille_trou, diametre, position_trou, debut, fin):
    	self.taille_trou = taille_trou
    	self.diametre = diametre

    	self.debut = debut
    	self.fin = fin

    	self.position_trou = position_trou

    	self.paroi_basse = [[diametre, debut], [diametre, position_trou], [diametre, position_trou+taille_trou], [diametre, fin]]

    	self.trou = [[diametre,position_trou], [diametre,position_trou+taille_trou]]

    	self.compteur = 0

    

    def update_paroi(self, x_plaquette, y_plaquette, taille_plaquette):
    	self.paroi_basse.append([[x_plaquette,y_plaquette], [x_plaquette,y_plaquette+taille_plaquette]])

    	self.compteur += 1


a = envir(50,500)
print a.paroi_basse
a.update_paroi(100+a.diametre-1, 199, 30)
print a.paroi_basse