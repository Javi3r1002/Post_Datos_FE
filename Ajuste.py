#import Arduino as Ad
from scipy.optimize import curve_fit as CT
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date, time, timedelta
from sklearn.neighbors import LocalOutlierFactor
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from math import pi
from matplotlib.widgets import SpanSelector
import os
import pathlib

fig, ax = plt.subplots()
fig1, ax2 = plt.subplots()
data = pd.read_csv('sensorultrasonico8.csv',encoding='cp1252', sep  =',')

Tiempo = data['Tiempo']
D = data.iloc[:,1]
TF = Tiempo
AAAAAA = False
opt = ['Lineal', 'Cuadrática']
DF = D 
Tiempo = Tiempo.astype(float)

"""
CURR_DIR = os.getcwd()
print(CURR_DIR)
directorio = pathlib.Path(CURR_DIR)
Archivos = os.listdir(directorio)

for i in Archivos:
	if i.split('.')[-1] != 'csv':
		Archivo = Archivos.remove(i)
print(Archivos)
#data.to_csv('example.csv', sep =';', index = False)
"""


class aplic():
	def __init__(self):
		self.master = Tk()
		self.master.geometry("1x1")
		self.master.withdraw()
		self.root = tk.Toplevel()
		#Se definen las dimensiones de la ventana a la que tiene acceso el usuario
		w,h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
		self.root.geometry("%dx%d+0+0" % (w, h))
		self.root.resizable(False,False)

		self.Can = Canvas(self.root, bg = 'white', height = h, width = w)
		self.Can.pack()
		fontt = tkFont.Font(family = "Times New Roman", size = 10)

		W = Frame(self.Can, height = 300, width = 750, bg = "#F0B27A")
		W.place(x = 20 , y = 520)

		SV = Scale(W, from_=0, to=1, resolution= .05, orient=HORIZONTAL, length=110, bg = '#F0B27A', bd = 0, highlightbackground = '#F0B27A', label = 'Factor de correción')
		SV.set(0)
		SV.place(x = 10, y = 35)

		des = StringVar()

		L = Label(W, text = "Regresiones", font = fontt, bg = '#F0B27A')
		L.place(x = 200, y = 35)

		drop = OptionMenu(W, des, *opt)
		drop.place(x = 200, y = 60)

		lL = Label(self.Can, text = "Javier Mejía Alecio (20304)", font = fontt, bg = 'white')
		lL.place(x = 50, y = 5)

		global LR
		LR = Label(W, text = "", font = fontt, bg = '#F0B27A')
		LR.place(x = 325, y = 55)

		LRG = Label(W, text = 'polinomio de la regresión:', font = fontt, bg = '#F0B27A')
		LRG.place(x = 325, y = 35)


		CA = FigureCanvasTkAgg(fig, master=self.Can)
		CA.get_tk_widget().place(x = 25, y = 25)

		CA2 = FigureCanvasTkAgg(fig1, master=self.Can)
		CA2.get_tk_widget().place(x = 700, y = 25)



		Data = pd.DataFrame(list(zip(Tiempo,D)), columns = ['Tiempo','Distancia'])
		Res = Data


		def Out_L(fac):
			Data = Res
			clf = LocalOutlierFactor()
			y_pred = clf.fit_predict(Data)

			x_score = clf.negative_outlier_factor_
			outlier_score = pd.DataFrame()
			outlier_score["score"] = x_score

			threshold = np.quantile(x_score , fac)                                            
			filtre = outlier_score["score"] < threshold
			outlier_index = outlier_score[filtre].index.tolist()
			return outlier_index

		def R2(X,Y,P):
			print(len(X))
			mymodel = np.poly1d(np.polyfit(X,Y, P))
			return mymodel


		Sca = ax.scatter(Data.iloc[:,0], Data.iloc[:,1])
		#Mooo = ax.plot(Data.iloc[:,0], mymodel(Data.iloc[:,0]))

		def get_new():
			new_X = [X[-1]]
			new_y = [Y[-1]]

			return new_X, new_y


		def animate(i):
			#Se obtiene loa valores que se van a graficar
			global TF 
			global DF
			global AAAAAA
			#print(len(TF))

			OI = Out_L(SV.get())

			if len(OI) != 0:
				Data_cop = Data.copy()
				Data_cop.drop(OI, inplace=True)
				TF = Data_cop.iloc[:,0]
				DF = Data_cop.iloc[:,1]


				ax.clear()
				ax.scatter(TF, DF, c='#1f77b4')
			else:
				ax.clear()
				ax.scatter(Data.iloc[:,0], Data.iloc[:,1], c='#1f77b4')
				TF = Data.iloc[:,0]
				DF = Data.iloc[:,1]
				"""Nx, Ny = get_new()
				#Se añade a la lista de puntos 
				VX.extend(Nx)
				VY.extend(Ny)
				#Se grafican
				scatter.set_offsets(np.c_[VX,VY])
				"""


		
		# Set useblit=True on most backends for enhanced performance.
		
		line2, = ax2.plot([], [])
		Regeee, = ax2.plot([],[], 'r')
		def onselect(xmin, xmax):
			#ax2.clear()
			global AAAAAA
			AAAAAA = True
			indmin, indmax = np.searchsorted(TF, (xmin, xmax))
			indmax = min(len(TF) - 1, indmax)

			region_x = TF[indmin:indmax]
			region_y = DF[indmin:indmax]

			if len(region_x) >= 2:
			    line2.set_data(region_x, region_y)
			    ax2.set_xlim(region_x.min()-10, region_x.max()+10)
			    ax2.set_ylim(region_y.min()-10, region_y.max()+10)
			    fig1.canvas.draw_idle()
			    V = des.get()
			    if( V == ''):
			    	print()
			    elif (V == 'Lineal'):
			    	Model = R2(region_x, region_y, 1)
			    	LR.config(text = str(Model))
			    	Regeee.set_data(region_x,Model(region_x))
			    elif (V == 'Cuadrática'):
			    	Model = R2(region_x, region_y, 2)
			    	LR.config(text = str(Model))
			    	Regeee.set_data(region_x,Model(region_x))
			    elif (V == 'Sinusoidal'):
			    	print()

			    

		span = SpanSelector(ax, onselect, "horizontal", useblit=True)


		ani = animation.FuncAnimation(fig, animate)
		

		



		#plt.show()







		self.master.mainloop()



def main():
    app = aplic()
    return(0)
        
if __name__ == '__main__':
    main()




