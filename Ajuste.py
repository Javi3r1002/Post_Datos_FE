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

		self.graph = Canvas(self.Can, bg = 'black', height = 750, width = 635)
		self.graph.place(x = 650, y = 40)

		fontt = tkFont.Font(family = "Century Gothic", size = 10)


		data = pd.read_csv('sensorultrasonico8.csv',encoding='cp1252', sep  =',')
		
		print(data['Tiempo'].dtype)
		print(data['Distancia'].dtype)
		Tiempo = data['Tiempo']
		D = data.iloc[:,1]

		Tiempo = Tiempo.astype(float)

		Data = pd.DataFrame(list(zip(Tiempo,D)), columns = ['Tiempo','Distancia'])

		clf = LocalOutlierFactor()
		y_pred = clf.fit_predict(Data)

		x_score = clf.negative_outlier_factor_
		outlier_score = pd.DataFrame()
		outlier_score["score"] = x_score

		threshold = np.quantile(x_score , .05)                                            
		filtre = outlier_score["score"] < threshold
		outlier_index = outlier_score[filtre].index.tolist()

		Data.drop(outlier_index, inplace=True)

		#D = D.between(D.quantile(.05), D.quantile(.95))


		mymodel = np.poly1d(np.polyfit(Data.iloc[:,0],Data.iloc[:,1], 2))
		print(mymodel)

		plt.scatter(Data.iloc[:,0], Data.iloc[:,1])
		#plt.scatter(Tiempo, D)
		plt.plot(Data.iloc[:,0], mymodel(Data.iloc[:,0]))
		plt.show()



def main():
    app = aplic()
    return(0)
        
if __name__ == '__main__':
    main()




