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
    #dicoRel : contient pour chaque prot ( avec cb de prot reagit, (affinite,devient), 'c' si forme cplexe 'p' si forme prot)
    #dicoProt : dico contient toutes les proteines (avec en cle leur nom en string)

    def __init__(self, taille_trou, position_trou, diametre, debut, fin, vitesse_max_flux):
    	self.taille_trou = taille_trou
        self.position_trou = position_trou
        self.vitesse_max_flux = vitesse_max_flux

    	self.diametre = diametre
        self.debut=debut
    	self.fin = fin

        self.compteur = 0
    	self.dt = 1

        p1 = protein(20, random.random()*fin, random.random()*fin)
        p2 = protein(40, random.random()*fin, random.random()*fin)
        p3 = protein(30, random.random()*fin, random.random()*fin)
        p4 = protein(44, random.random()*fin, random.random()*fin)

        self.dicoProt={}

        self.dicoProt['fVIIa']=[p1]
        self.dicoProt['TF']=[p2]
        self.dicoProt['X']=[]
        #on fait une liste pour les complexes ? ou on met juste attribut active ?
        self.dicoProt['prothrombine']=[p4]
        self.dicoProt['Xa']=[p3]
        self.dicoProt['V']=[]
        self.dicoProt['fibrinogene']=[]
        self.dicoProt['thrombine']=[]
        self.dicoProt['fibrine']=[]
        self.dicoProt['plaquettes']=[]


        self.dicoRel={}

        self.dicoRel['fVIIa']=(1,'TF','VIIa-TF','c')
        self.dicoRel['TF']=(1,'fVIIa','VIIa-TF','c')
        self.dicoRel['X']=(1,'VIIa-TF','Xa','p')
        self.dicoRel['VIIa-TF']=(1,'X','Xa','p')
        self.dicoRel['prothrombine']=(1,'Xa','thrombine','p')
        #Xa + prothrombine = thrombine
        #Xa + V = Va
        self.dicoRel['Xa']=(2,('prothrombine','V'),('thrombine','Va'),'p')
        self.dicoRel['V']=(1,'Xa','Va','p')
        self.dicoRel['fibrinogene']=(1,'thrombine','fibrine','p')
        self.dicoRel['thrombine']=(1,'fibrinogene','fibrine','p')

        #dictionnaire contient les tailles de chaque type de prot
        #rempli au hasard pour le moment, a changer apres!!
        self.dicoTaille={}

        self.dicoTaille['fVIIa']=[10]
        self.dicoTaille['TF']=[10]
        self.dicoTaille['X']=[10]
        self.dicoTaille['prothrombine']=[10]
        self.dicoTaille['Xa']=[10]
        self.dicoTaille['V']=[10]
        self.dicoTaille['fibrinogene']=[10]
        self.dicoTaille['thrombine']=[10]
        self.dicoTaille['fibrine']=[10]
        self.dicoTaille['plaquettes']=[10]

        #dictionnaire contient les couleurs dans lesquelles seront dessinees les proteines
        #couleur a mettre en tuple (r,g,b)
        self.dicoCouleur={}

        self.dicoCouleur['fVIIa']=[]
        self.dicoCouleur['TF']=[]
        self.dicoCouleur['X']=[]
        self.dicoCouleur['prothrombine']=[]
        self.dicoCouleur['Xa']=[]
        self.dicoCouleur['V']=[]
        self.dicoCouleur['fibrinogene']=[]
        self.dicoCouleur['thrombine']=[]
        self.dicoCouleur['fibrine']=[]
        self.dicoCouleur['plaquettes']=[]



        self.venin=""
        self.vitesse_lim=20

    #----------------------------------------------------------------------------------------------------
    #                                      moveAll
    #----------------------------------------------------------------------------------------------------

    #calcule la nouvelle position de toutes les proteines
    def moveAll(self):
        for typeProt,l in self.dicoProt.items(): #on parcourt chaque liste de prot (l=liste d'un type de prot)

            for i in xrange(len(l)): #on regarde chaque prot de cette liste  (l[i]=une prot de cette liste d'un type)
                print "l[i]",l[i]

                if l[i].activation==False: #si est pas deja activee (auquel cas ne peut pas bouger)
                    move = True #de base peut bouger, sauf si rencontre une prot ac qui peut reagir
                    prot = 0 #proteine avec qui va reagir 
                    distance = self.fin*self.diametre  #distance entre les 2 prot initialisee tres grande

                    if self.dicoRel[typeProt][0]==1: #si peut reagir qu'avec un type de proteine
                        for j in self.dicoProt[self.dicoRel[typeProt][1]]: #pour chaque prot de liste des prot avec qui peut reagir (j=type prot)
                            if l[i].detection(j)== True:  #si detecte une des prot avec qui peut reagir
                                if l[i].distance(j)<distance: #pour que reagisse seulement avec la prot la plus proche
                                    move = False
                                    prot=j
                                    distance=l[i].distance(j)

                        if move == True: #si va bouger, a rencontre aucune prot ac qui peut reagir (regarder apres fin boucle for)

                            l[i].move(self.dt, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre,self.vitesse_max_flux)

                        if move == False: #si a rencontre une prot donc va reagir
                            l[i].activation=True #on active les 2 prot
                            prot.activation=True
                            self.reaction(typeProt,l[i],prot)  


                    if self.dicoRel[typeProt][0]>1: #si peut reagir avec 2 types de prot
                        for reactif in self.dicoRel[typeProt][1]: #pour chacun des reactifs ac qui peut reagir
                            for j in self.dicoProt[reactif]:
                                if l[i].detection(j)==True:
                                    if l[i].distance(j)<distance:
                                        move=False
                                        prot=j
                                        distance=l[i].distance(j)
                        if move == True:
                            l[i].move(self.dt, self.vitesse_lim, self.position_trou, self.taille_trou, self.debut, self.fin, self.diametre, self.vitesse_max_flux)
                        
                        if move == False:
                            l[i].activation=True #on active les 2 prot
                            prot.activation=True
                            self.reaction(typeProt,l[i],prot)



    #si rencontre pls prot ac qui peut reagir !!

    #----------------------------------------------------------------------------------------------------
    #                                      reaction
    #----------------------------------------------------------------------------------------------------
    #cree les nouvelles prot ou complexes
    #enleve les proteines qui ont reagit de leur liste de prot
    #typeProt=type d'une des prot qui reagit (en string)
    #prot et prot 2 = objets proteines qui reagissent

    #rq : finalement pas de disctinction entre complexe et proteine car posait pb d'avoir un tuple de 2 prot et non une prot dans la liste des 
    #proteines complexees (notamment pour prot.x, un tuple a pas d'attribut x)
    #il faudra, dans la methode d'affichage, faire 2 boules quand c'est un complexe

    def reaction(self,typeProt,prot,prot2):
        #on cree la nouvelle proteine qui aura comme cord la moyenne des coords des 2 autres prot
        p = protein(self.dicoTaille[self.dicoRel[typeProt][1]], (prot.x+prot2.x)/2, (prot.y+prot2.y)/2)

        self.dicoProt[typeProt].remove(prot) #on enleve du tableau la proteine qui se transforme 
        self.dicoProt[self.dicoRel[typeProt][1]].remove(prot2)  #on enleve l'autre prot qui reagit du tableau

            

    #methode cree prot def prot(self,fact1,fact2)..
    #----------------------------------------------------------------------------------------------------
    #                                         run
    #----------------------------------------------------------------------------------------------------

    def run(self):

        #creation de la premiere fenetre (Thiago ?)
        #recuperer la case cochee par l'utilisateur (parse event en c++)
        #creer toutes les proteines qu'il faut (de base mettre des attributs de classe avec la compo de chaque venin?)


        continu = True
        #boucle infinie
        while continu==True:
            #on actualise fenetre en la redessinant vide (rect blanc ac la breche)
            for typeProt,l in self.dicoProt.items(): #on parcourt toutes les prot
                #on dessine chaque prot selon le type de prot
                #-> faire un dico ou couleur de chaque type de prot ecrit?
                a=0
            self.moveAll() #on fait bouger toutes les prot

            continu = False #temporaire, juste mis pour pas que boucle infinie

        #+q : quand est ce qu'on arrete le programme ?






#taille_trou, position_trou, diametre, debut, fin,vitesse_max_flux
e=envir(20,40,80,0,100,10)
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

#reaction(self,typeProt,prot,prot2)
#e.reaction('fVIIa',e.dicoProt['fVIIa'][0],e.dicoProt['TF'][0])
print e.dicoProt['fVIIa']
print e.dicoProt['TF']
print e.dicoProt[e.dicoRel['TF'][1]]

e.run()