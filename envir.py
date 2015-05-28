import numpy
import math
from protein import *


class envir:


    #----------------------------------------------------------------------------------------------------
    #                                        Constructeur
    #----------------------------------------------------------------------------------------------------

    #taille trou : longueur du trou
    #position_trou: position x du trou (par rapport au debut du vaisseau)
    #diametre : diametre du vaisseau (longueur en y)
    #debut: indice x de debut du vaisseau (par rapport a la fenetre)
    #fin: indice x de fin du vaisseau (y-x=longueur du vaisseau)
    #protPermanentes : liste des prot seront dans le sang a chaque essai et seront affichees
    #protTotales : liste de ttes  les proteines dans le sang
    #dicoRel : contient pour chaque prot ( avec cb de prot reagit, (affinite,devient),(inhibe) )
    #dicoProt : dico contient toutes les proteines (avec en cle leur nom en string)

    def __init__(self, taille_trou, position_trou, diametre, debut, fin):
    	self.taille_trou = taille_trou
        self.position_trou = position_trou

    	self.diametre = diametre
        self.debut=debut
    	self.fin = fin

        self.compteur = 0
    	self.dt = 1

        p1 = protein(20, random.random()*fin, random.random()*fin)
        p2 = protein(40, random.random()*fin, random.random()*fin)
        p3 = protein(30, random.random()*fin, random.random()*fin)

        self.dicoProt={}

        self.dicoProt['fVIIa']=[p1]
        self.dicoProt['TF']=[p2]
        self.dicoProt['X']=[]
        #on fait une liste pour les complexes ? ou on met juste attribut active ?
        self.dicoProt['prothrombine']=[]
        self.dicoProt['Xa']=[p3]
        self.dicoProt['V']=[]
        self.dicoProt['fibrinogene']=[]
        self.dicoProt['thrombine']=[]
        self.dicoProt['fibrine']=[]
        self.dicoProt['plaquettes']=[]


        self.dicoRel={}

        self.dicoRel['fVIIa']=(1,'TF','VIIa-TF')
        self.dicoRel['TF']=(1,'fVIIa','VIIa-TF')
        self.dicoRel['X']=(1,'VIIa-TF','Xa')
        self.dicoRel['VIIa-TF']=(1,'X','Xa')
        self.dicoRel['prothrombine']=(1,'Xa','thrombine')
        #Xa + prothrombine = thrombine
        #Xa + V = Va
        self.dicoRel['Xa']=(2,('prothrombine','V'),('thrombine','Va'))
        self.dicoRel['V']=(1,'Xa','Va')
        self.dicoRel['fibrinogene']=(1,'thrombine','fibrine')
        self.dicoRel['thrombine']=(1,'fibrinogene','fibrine')






        #METTRE LE NOM DES LISTES A LA PLACE DES NOMS DE PROT DANS LE DICO
        #pas possible, cles peuvent pas etre des types listes.. types prot ?

        #pb=besoin des prot pour appeler les fonctions, donc dans le dico je dois avoir des prot... 

        #solution = un dico ou un type de facteur en cle et toutes les prot en valeur
        #du coup : plus besoin de liste des prot totales, on parcourt tout le dico
        #pr chaque prot d'un type, on fait dicoRel[cle][1] detection

        #et si cle=string et valeurs = les listes? comment on a la string ?

        self.venin=""
        self.vitesse_lim=20

    #----------------------------------------------------------------------------------------------------
    #                                      moveAll
    #----------------------------------------------------------------------------------------------------

    #calcule la nouvelle position de toutes les proteines
    def moveAll(self):
        for typeProt,l in self.dicoProt.items(): #on parcourt chaque liste de prot (l=liste d'un type de prot)

            if len(l)!=0: #si liste de ce type de prot n'est pas vide
                for i in xrange(len(l)): #on regarde chaque prot de cette liste  (l[i]=une prot de cette liste d'un type)

                    if l[i].activation==False: #si est pas deja activee (auquel cas ne peut pas bouger)

                        if self.dicoRel[typeProt][0]==1: #si peut reagir qu'avec un type de proteine
                            move=True  #de base peut bouger, sauf si rencontre une prot ac qui peut reagir

                            for j in self.dicoProt[self.dicoRel[typeProt][1]]: #pour chaque prot de liste des prot avec qui peut reagir (j=type prot)
                                if l[i].detection(j)== True:  #si detecte une des prot avec qui peut reagir
                                    move = False

                            if move == True: #si va bouger, a rencontre aucune prot ac qui peut reagir (regarder apres fin boucle for)
                                print typeProt
                                l[i].move(self.dt, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre)
                                print l[i].x
                                #+ les faire se transformer !
                        if self.dicoRel[typeProt][0]>1: #si peut reagir avec 2 types de prot
                            move=True

                            for reactif in self.dicoRel[typeProt][1]: #pour chacun des reactifs ac qui peut reagir
                                for j in self.dicoProt[reactif]:
                                    if l[i].detection(j)==True:
                                        move=False
                            if move == True:
                                l[i].move(self.dt, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre)






            



    #----------------------------------------------------------------------------------------------------
    #                                         run
    #----------------------------------------------------------------------------------------------------

    def run(self):
        a=0



#taille_trou, position_trou, diametre, debut, fin
e=envir(20,40,80,0,100)
# #dico normaux 
# print e.dicoRel['V']
# print e.dicoRel['V'][0]   #donne la proteine avec qui reagit


# #cas special ou reagit avec 2 prot differentes
# print e.dicoRel['Xa']  #donne premier tuple du tuple (deux trucs ac lesquels reagit)
# print e.dicoRel['Xa'][1]  #donne 2 trucs avec lesquels peut reagir
# print e.dicoRel['Xa'][1][0]
# print len(e.dicoRel['Xa'])  #taille 2 aussi (car 2 tuples)


print 'debut : fVIIa',e.dicoProt['fVIIa']
print 'debut : TF',e.dicoProt['TF']
print 'debut : Xa',e.dicoProt['Xa']
e.moveAll()
print 'fin : fVIIa',e.dicoProt['fVIIa']
print 'fin : TF',e.dicoProt['TF']
print 'fin : Xa',e.dicoProt['Xa']
