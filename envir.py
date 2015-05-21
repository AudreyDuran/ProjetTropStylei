import numpy
import math
import random

class envir:

    #taille trou : longueur du trou
    #position_trou: position x du trou (par rapport au debut du vaisseau)
    #diametre : diametre du vaisseau (longueur en y)
    #debut: indice x de debut du vaisseau (par rapport a la fenetre)
    #fin: indice x de fin du vaisseau (y-x=longueur du vaisseau)

    def __init__(self, taille_trou, position_trou, diametre, debut, fin):
    	self.taille_trou = taille_trou
        self.position_trou = position_trou

    	self.diametre = diametre
        self.debut=debut
    	self.fin = fin

    	self.compteur = 0


a = envir(50,500)
print a.paroi_basse
a.update_paroi(100+a.diametre-1, 199, 30)
print a.paroi_basse