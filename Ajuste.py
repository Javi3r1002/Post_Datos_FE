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

fig, ax = plt.subplots()
fig1, ax2 = plt.subplots()


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

		W = Frame(self.Can, height = 300, width = 750, bg = "#F0B27A")
		W.place(x = 20 , y = 520)

		SV = Scale(W, from_=0, to=1, resolution= .05, orient=HORIZONTAL, length=100, bg = '#F0B27A', bd = 0, highlightbackground = '#F0B27A', label = 'Factor')
		SV.set(0)
		SV.place(x = 10, y = 35)



		fontt = tkFont.Font(family = "Century Gothic", size = 10)

		CA = FigureCanvasTkAgg(fig, master=self.Can)
		CA.get_tk_widget().place(x = 25, y = 25)

		CA2 = FigureCanvasTkAgg(fig1, master=self.Can)
		CA2.get_tk_widget().place(x = 700, y = 25)


		data = pd.read_csv('sensorultrasonico8.csv',encoding='cp1252', sep  =',')

		Tiempo = data['Tiempo']
		D = data.iloc[:,1]

		Tiempo = Tiempo.astype(float)

		Data = pd.DataFrame(list(zip(Tiempo,D)), columns = ['Tiempo','Distancia'])
		Res = Data


		line2, = ax2.plot([], [])
		def onselect(xmin, xmax):
			print(xmin, xmax)
			indmin, indmax = np.searchsorted(Tiempo, (xmin, xmax))
			indmax = min(len(Tiempo) - 1, indmax)

			region_x = Tiempo[indmin:indmax]
			region_y = D[indmin:indmax]
			print(region_x)

			if len(region_x) >= 2:
			    line2.set_data(region_x, region_y)
			    ax2.set_xlim(region_x.min(), region_x.max())
			    ax2.set_ylim(region_y.min(), region_y.max())
			    fig1.canvas.draw_idle()

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


		mymodel = np.poly1d(np.polyfit(Data.iloc[:,0],Data.iloc[:,1], 2))
		print(mymodel)

		Sca = ax.scatter(Data.iloc[:,0], Data.iloc[:,1])
		#Mooo = ax.plot(Data.iloc[:,0], mymodel(Data.iloc[:,0]))

		def get_new():
			new_X = [X[-1]]
			new_y = [Y[-1]]

			return new_X, new_y


		def animate(i):
			#Se obtiene loa valores que se van a graficar

			OI = Out_L(SV.get())

			if len(OI) != 0:
				Data_coý = Data.copy()
				Data_coý.drop(OI, inplace=True)
				ax.clear()
				ax.scatter(Data_coý.iloc[:,0], Data_coý.iloc[:,1], c='#1f77b4')
			else:
				ax.clear()
				ax.scatter(Data.iloc[:,0], Data.iloc[:,1], c='#1f77b4')
				"""Nx, Ny = get_new()
				#Se añade a la lista de puntos 
				VX.extend(Nx)
				VY.extend(Ny)
				#Se grafican
				scatter.set_offsets(np.c_[VX,VY])
				"""


		span = SpanSelector(ax, onselect, "horizontal", useblit=True)
		# Set useblit=True on most backends for enhanced performance.
		



		ani = animation.FuncAnimation(fig, animate)

		



		#plt.show()







		self.master.mainloop()



def main():
    app = aplic()
    return(0)
        
if __name__ == '__main__':
    main()




