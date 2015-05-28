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
        self.fVIIa=[]
        self.TF=[]
        self.X=[]
        self.VIIa-TF=[]
        self.prothrombine=[]
        self.Xa=[]
        self.V=[]
        self.fibrinogene=[]
        self.thrombine=[]

        self.dicoRel={}

        self.dicoRel['fVIIa']=('TF','VIIa-TF')
        self.dicoRel['TF']=('fVIIa','VIIa-TF')

        self.dicoRel['X']=('VIIa-TF','Xa')
        self.dicoRel['VIIa-TF']=('X','Xa')

        self.dicoRel['prothrombine']=('Xa','thrombine')
        #Xa + prothrombine = thrombine
        #Xa + V = Va
        self.dicoRel['Xa']=(('prothrombine','V'),('thrombine','Va'))
        self.dicoRel['V']=('Xa','Va')

        self.dicoRel['fibrinogene']=('thrombine','fibrine')
        self.dicoRel['thrombine']=('fibrinogene','fibrine')

        #on le met vraiment le cross linked fibrin clot ?
        self.dicoRel['XIIIa']=('fibrine','fibrinclot')
        self.dicoRel['fibrine']=('XIIIa','fibrinclot')

        #METTRE LE NOM DES LISTES A LA PLACE DES NOMS DE PROT DANS LE DICO
        #pas possible, cles peuvent pas etre des types listes.. types prot ?

        #pb=besoin des prot pour appeler les fonctions, donc dans le dico je dois avoir des prot... 
        #ou un truc7

        #solution = un dico ou un type de facteur en cle et toutes les prot en valeur
        #du coup : plus besoin de liste des prot totales, on parcourt tout le dico
        #pr chaque prot d'un type, on fait dicoRel[cle][1] detection

        #et si cle=string et valeurs = les listes? comment on a la string ?

        self.venin=""
        self.vitesse_lim=20


    #calcule la nouvelle position de toutes les proteines
    def moveAll(self):
        for l in self.protTotales: #on parcourt chaque liste de prot (l=liste d'un type de prot)
            for i in xrange(len(l)): #on regarde chaque prot de cette liste  (l[i]=une prot de cette liste d'un type)

                if l[i].activation==False: #si est pas deja activee (auquel cas ne peut pas bouger)

                    if len(self.dicoRel[l[i][0]])==1: #si peut reagir qu'avec un type de proteine

                        #faire une boucle for chaque prot de la liste des prot avec qui reagit
                        if l[i].detection(self.dicoRel[l[i][0]])== False:  #si detecte pas une des prot avec qui peut reagir
                            l[i].move(self.compteur, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre)

                        else: #si detecte une prot avec qui reagit
                            l[i].activation=True





    def run(self):
        a=0




e=envir(20,40,80,0,100)
print e.dicoRel['Xa'][0]
print len(e.dicoRel['Xa'][0])