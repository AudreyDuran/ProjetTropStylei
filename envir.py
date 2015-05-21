import numpy
import math
import random

class envir:

    #taille trou : longueur du trou
    #position_trou: position x du trou (par rapport au debut du vaisseau)
    #diametre : diametre du vaisseau (longueur en y)
    #debut: indice x de debut du vaisseau (par rapport a la fenetre)
    #fin: indice x de fin du vaisseau (y-x=longueur du vaisseau)
    #protPermanentes : liste des prot seront dans le sang a chaque essai et seront affichees
    #protTotales : liste de ttes  les proteines dans le sang
    #dicoRel : contient pour chaque prot ( (affinite,devient),(inhibe) )

    def __init__(self, taille_trou, position_trou, diametre, debut, fin):
    	self.taille_trou = taille_trou
        self.position_trou = position_trou

    	self.diametre = diametre
        self.debut=debut
    	self.fin = fin

    	self.compteur = 0

        self.protPermanentes=[]
        self.protTotales=[]

        self.dicoRel={}

        self.dicoRel['fVIIa']=('TF','VIIa-TF')
        self.dicoRel['TF']=('fVIIa','VIIa-TF')

        self.dicoRel['X']=('VIIa-TF','Xa')
        self.dicoRel['VIIa-TF']=('X','Xa')

        self.dicoRel['prothrombine']=('Xa','thrombine')
        self.dicoRel['Xa']=(('prothrombine','thrombine'),('V','Va'))
        self.dicoRel['V']=('Xa','Va')

        self.dicoRel['fibrinogene']=('thrombine','fibrine')
        self.dicoRel['thrombine']=('fibrinogene','fibrine')

        #on le met vraiment le cross linked fibrin clot ?
        self.dicoRel['XIIIa']=('fibrine','fibrinclot')
        self.dicoRel['fibrine']=('XIIIa','fibrinclot')

        self.venin=""



    def run(self):
        a=0




e=envir(20,40,80,0,100)
#e.dicoRel['Xa'][0]=0
print e.dicoRel['Xa'][1]