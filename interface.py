import wx
import os

class GUI(wx.Frame):
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id,"Venin" , size=(250, 170))
#		self.panel = wx.Panel(self, -1)
		self.cb = wx.CheckBox(self, -1, 'Venin', (10, 10))
		wx.EVT_CHECKBOX(self, self.cb.GetId(), self.Options)
		self.Run=wx.Button(self,1,"Run",(100,10))
		self.Bind(wx.EVT_BUTTON, self.OnRun, self.Run)
		self.Show()
		self.Centre()
		self.v=0

	def Options(self, event):
		if self.cb.GetValue():
			self.V1=wx.CheckBox(self,-1,'Venin1',(30,50))
			self.V2=wx.CheckBox(self,-1,'Venin2',(30,70))
			self.V3=wx.CheckBox(self,-1,'Venin3',(30,90))
			self.V4=wx.CheckBox(self,-1,'Venin4',(30,110))

		if not self.cb.GetValue(): 
			self.V1.Show(False)
			self.V2.Show(False)
			self.V3.Show(False)
			self.V4.Show(False)
			if self.txt:
				self.txt.Show(False)

	def OnRun(self,event):
		if self.cb.GetValue():
			if sum((self.V1.GetValue(),self.V2.GetValue(),self.V3.GetValue(),self.V4.GetValue()))>1:
				self.txt=wx.StaticText(self,-1, "Choisissez juste un venin",(50,140))
			else:
				self.v=(self.V1.GetValue(),self.V2.GetValue(),self.V3.GetValue(),self.V4.GetValue()).index(1)+1
				os.system("python "+"simulation.py %d"%self.v)
				self.Close()
		else:
			os.system("python "+"simulation.py 0")
			self.Close()

app = wx.App(0)
GUI(None, -1)
app.MainLoop()
