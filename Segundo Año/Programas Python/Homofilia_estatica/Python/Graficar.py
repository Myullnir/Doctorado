#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 16 14:21:12 2022

@author: favio
"""


import pandas as pd
import time
import os
import funciones as func
from pathlib import Path

# Importo todas las librerías que voy a usar en el programa. Estas son las que
# uso en los tres programas, por lo que no debería necesitar nada más.

t0 = time.time()

T=2 # Defino el número de tópicos
Etapa = Path("Homofilia_estatica") # Defino el nombre de la etapa del trabajo en la que estoy

# Defino las carpetas que voy a recorrer. Tiene más sentido definir esto a mano.
Carpetas = ["2D"]

for carp in Carpetas:
    
    # Transformo estas cosas en paths. Espero que acostumbrarme a esto valga la pena
    Direccion = Path("../{}".format(carp))
    carpeta = Path(carp)
    
    # Recorro las carpetas con datos
    CarpCheck=[[root,files] for root,dirs,files in os.walk(Direccion)]
    
    # Me armo una lista con los nombres de todos los archivos con datos.
    # Coloco al inicio de la lista el path de la carpeta en la que se encuentran los datos
    
    Archivos_Datos = [nombre for nombre in CarpCheck[0][1]]
    
    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre:
    # "Opiniones_N=$_kappa=$_beta=$_Iter=$.file" y "Testigos_N=$_kappa=$_beta=$_Iter=$.file"
    # En la carpeta 1D
    
    # En cambio, en la carpeta 2D llevan por nombre:
    # "Opiniones_N=$_kappa=$_beta=$_cosd=$_Iter=$.file" y "Testigos_N=$_kappa=$_beta=$_cosd=$_Iter=$.file"
    
    Df_archivos = pd.DataFrame({"nombre": Archivos_Datos})
    
    # Hecho mi dataframe, voy a armar columnas con los parámetros que varían en los nombres de mis archivos
    Df_archivos["tipo"] = Df_archivos["nombre"].apply(lambda x: x.split("_")[0])
    Df_archivos["n"] = Df_archivos["nombre"].apply(lambda x: float(x.split("_")[1].split("=")[1]))
    Df_archivos["parametro_1"] = Df_archivos["nombre"].apply(lambda x: float(x.split("_")[2].split("=")[1]))
    Df_archivos["parametro_2"] = Df_archivos["nombre"].apply(lambda x: float(x.split("_")[3].split("=")[1]))
    Df_archivos["parametro_3"] = Df_archivos["nombre"].apply(lambda x: float(x.split("_")[4].split("=")[1]))
    Df_archivos["iteracion"] = Df_archivos["nombre"].apply(lambda x: float(x.split("_")[5].split("=")[1].strip(".file")))
    
    #----------------------------------------------------------------------------------------------

    # Por un lado necesito los nombres que pasaré a los títulos de los archivos
    
    nombre_parametro_1 = "kappa"
    nombre_parametro_2 = "beta"
    nombre_parametro_3 = "cosd"
    
    
    # Lo otro que necesito es el nombre que pasaré a los ejes de los gráficos de las funciones
    
    titulo_parametro_1 = r"\kappa"
    titulo_parametro_2 = r"\beta"
<<<<<<< Updated upstream
    titulo_parametro_3 = r"cos(\delta)"
=======
    titulo_parametro_2 = r"cos(\delta)"
>>>>>>> Stashed changes
    
    #----------------------------------------------------------------------------------------------
    
    func.Mapa_Colores_Promedio_opiniones(Df_archivos, Direccion, Etapa/carpeta,
                                         titulo_parametro_2, titulo_parametro_3,
                                         titulo_parametro_1,nombre_parametro_1)
    
    #----------------------------------------------------------------------------------------------
    
<<<<<<< Updated upstream
    func.Mapa_Colores_Entropia_opiniones(Df_archivos, Direccion, Etapa/carpeta,
                                         titulo_parametro_2, titulo_parametro_3,
                                         titulo_parametro_1,nombre_parametro_1)
    
    #----------------------------------------------------------------------------------------------
    
    func.Mapa_Colores_Tiempo_convergencia(Df_archivos, Direccion, Etapa/carpeta,
                                         titulo_parametro_2, titulo_parametro_3,
                                         nombre_parametro_1)

    #----------------------------------------------------------------------------------------------
    
=======
>>>>>>> Stashed changes
    func.Graf_trayectorias_opiniones(Df_archivos, Direccion, Etapa/carpeta,
                                     nombre_parametro_1, nombre_parametro_2, nombre_parametro_3)


func.Tiempo(t0)