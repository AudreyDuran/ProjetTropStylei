import wx
import math
import numpy as np
import random


class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title,pos,size):
        wx.Frame.__init__(self, parent, ID, title,pos,size)
        self.SetAutoLayout (True)



        self.cb = wx.CheckBox(self,-1,'venin',(200,200))
        self.Bind(wx.EVT_CHECKBOX, self.imprimer_b1 , self.cb)
        
        tx = wx.TextCtrl( self, -1, 'text', (100,0))
        self.Bind(wx.EVT_CHECKBOX, self.imprimer_b1 , self.cb)

        self.boutton = []
        self.compteur = 0
        self.compteur1 = 0
        
        
        
    def bouton(self, label):
        for i,v in enumerate(label):
        	b = wx.Button(self, i, (0, i*35), (80, 33))
        	self.boutton.append(b)



    def bind_bouton(self, fonction):
    	for i,v in enumerate(self.boutton):
    		self.Bind(wx.EVT_BUTTON, fonction[i], v)


    def imprimer_b0(self,event):
    	print self.boutton[0].GetLabel()

    def imprimer_b1(self,event):
    	print self.boutton[1].GetLabel()
    	self.Destroy()

    def imprimer_b2(self,event):
    	self.compteur += 1
    	print self.compteur

    def imprimer_b3(self,event):
    	self.compteur1 += 1
    	print self.boutton[3].GetLabel()
    	if self.compteur1 >= 5:
    		self.Destroy()





    # Bouton
	def bouton(self, label):
		for i,v in enumerate(label):
			b = wx.Button(self, i, v, (0, i*35), (80, 33))
			self.boutton.append(b)

	def bind_bouton(self, fonction):
		for i,v in enumerate(self.boutton):
			self.Bind(wx.EVT_BUTTON, fonction[i], v)




   	# Texte
	def text(self, label):
		for i,v in enumerate(label):
			txt = wx.TextCtrl( self, i, v, (90, i*35))
			self.texte.append(txt)

	def bind_texte(self, fonction):
		for i,v in enumerate(self.texte):
			self.Bind(wx.EVT_TEXT_ENTER, fonction[i], v)



    # fonction
	def imprimer(self,event):
		self.compteur += 1
		print self.compteur



class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, -1, "coagulation",(40,40),(400,400))

		label = ['1', '2', '3', '4']
	
        # bouton
		frame.bouton(label)
		frame.bind_bouton([frame.imprimer_b0,frame.imprimer_b1,frame.imprimer_b2,frame.imprimer_b3])


        # texte
		frame.text(label)
		# frame.bind_texte(bind)

		frame.Show(True)
		self.SetTopWindow(frame)
		return True


app = MyApp(0)

app.MainLoop()
