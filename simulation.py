import numpy
import math
import sys
import pygame
import gtk
import random as r
from protein import *
from envir import *

#taille_trou, position_trou, diametre, debut, fin,vitesse_max_flux
e=envir(100,200,924, 0,gtk.gdk.screen_width(),10^-10)
# gtk.gdk.screen_height()-100


# #dico normaux 
# print e.dicoRel['V']
# print e.dicoRel['V'][0]   #donne la proteine avec qui reagit


# #cas special ou reagit avec 2 prot differentes
# print e.dicoRel['Xa']  #donne premier tuple du tuple (deux trucs ac lesquels reagit)
# print e.dicoRel['Xa'][1]  #donne 2 trucs avec lesquels peut reagir
# print e.dicoRel['Xa'][1][0]
# print len(e.dicoRel['Xa'])  #taille 2 aussi (car 2 tuples)


# print 'debut : fVIIa',e.dicoProt['fVIIa']
# print 'debut : TF',e.dicoProt['TF']
# print 'debut : Xa',e.dicoProt['Xa']
# e.moveAll()
# print 'fin : fVIIa',e.dicoProt['fVIIa']
# print 'fin : TF',e.dicoProt['TF']
# print 'fin : Xa',e.dicoProt['Xa']

# #reaction(self,typeProt,prot,prot2)
# #e.reaction('fVIIa',e.dicoProt['fVIIa'][0],e.dicoProt['TF'][0])
# print e.dicoProt['fVIIa']
# print e.dicoProt['TF']
# print e.dicoProt[e.dicoRel['TF'][1]]

#prot(fibrine,Va,prothrombine,Xa,plaquette,fibrinogene,thrombine,VIIaTF,V,TF,X,VIIa)

e.prot(10,0,3,0,50,10,0,0,0,10,11,0)

e.run()

for i in e.dicoProt.keys():
	print len(e.dicoProt[i])
