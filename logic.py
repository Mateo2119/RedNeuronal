from contextlib import nullcontext
from re import X
import tempfile
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
#Graficos
import matplotlib.pyplot as plt
import base64
from io import BytesIO
#analisis
import pingouin as pg
#Comprobación
import random as rn

class RedNeuronal:

    promedio = 0
    puntajeR = 0
    prediccion = 0
    correlacion = 0

    def __init__(self):
        print("Creando red neuronal")

    def iniciar(self):
        self.df = pd.read_csv("DATACSV.csv")
        self.promedio = self.df["Promedio"]
        self.puntaje = self.df["Puntaje"]
        self.X = self.promedio[:,np.newaxis]        
        self.correlacion = pg.corr(self.df['Promedio'], self.df['Puntaje'], method='pearson')

    def __grafica(self):
        fig, ax = plt.subplots(1, 1, figsize=(7,7))
        ax.scatter(x=self.promedio, y=self.puntaje, alpha= 0.9)
        ax.set_xlabel('Promedio')
        ax.set_ylabel('Puntaje')
        return fig        

    def graficar(self):       
        figura = self.__grafica()
        tmpfile = BytesIO()
        figura.savefig(tmpfile, format='png')
        tmpfile.seek(0)
        image_png = tmpfile.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        return f"<img src='data:image/png;base64,{graph}'/>"

    def entrenar(self):
        print("------------------ ENTRENANDO... -------------------")
        while True:
            X_train, X_test, y_train, y_test = train_test_split(self.X,self.puntaje)
            self.mlr = MLPRegressor(solver='lbfgs',alpha=1e-5,hidden_layer_sizes=(3,3),random_state=1)
            self.mlr.fit(X_train,y_train)  
            if (self.mlr.score(X_train,y_train)>0.70):
                break
        self.puntajeR = self.mlr.score(X_train,y_train)

    def predecir(self,m,p):
        print("------------------ PREDICIENDO... -------------------")
        num = (m+p)/2
        self.prediccion = self.mlr.predict(np.array([num]).reshape(1, 1))