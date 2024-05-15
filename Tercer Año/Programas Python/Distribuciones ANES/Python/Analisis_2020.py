#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 15:37:42 2024

@author: favio
"""

#############################################################################################
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import pandas as pd
import seaborn as sns
import numpy as np
from pathlib import Path
import time
from scipy.optimize import curve_fit
from scipy.odr import ODR, Model, Data, RealData
from scipy.spatial.distance import jensenshannon

import warnings
warnings.filterwarnings('ignore')
#############################################################################################

def data_processor(x):
    if(isinstance(x, int)):
        return x
    elif(isinstance(x, float)):
        return int(x)
    elif(isinstance(x, str)):
        return int(x[0]) if(x[0]!="-" and int(x[0])<9) else 0
    elif(x.isnan()):
        return 0
    else:
        print("Error, no se ha identificado el tipo: {}".format(type(x)))
        
#--------------------------------------------------------------------------------
        
# Esto va al final de un código, simplemente printea cuánto tiempo pasó desde la última
# vez que escribí el inicio del cronómetro t0=time.time()
def Tiempo(t0):
    t1=time.time()
    print("Esto tardó {} segundos".format(t1-t0))

t0 = time.time()

#############################################################################################

# Cargo el archivo de datos total

filename = "../Anes_2020/anes_timeseries_2020.dta"
df_raw_data = pd.read_stata(filename)

#############################################################################################

# Brief description of the codes
dict_labels = {'V201200':'Liberal-Conservative self Placement', 'V201225x':'Voting as duty or choice','V201231x':'Party Identity',
               'V201246':'Spending & Services', 'V201249':'Defense Spending', 'V201252':'Gov-private Medical Insurance',
               'V201255':'Guaranteed job Income', 'V201258':'Gov Assistance to Blacks', 'V201262':'Environment-Business Tradeoff',
               'V201342x':'Abortion Rights Supreme Court', 'V201345x':'Death Penalty','V201356x':'Vote by mail',
               'V201362x':'Allowing Felons to vote', 'V201372x':'Helpful-Harmful if Pres didnt have to worry about Congress',
               'V201375x':'Restricting Journalist access', 'V201382x':'Corruption increased or decreased since Trump',
               'V201386x':'House impeachment decision', 'V201405x':'Require employers to offer paid leave to parents',
               'V201408x':'Allow to refuse service to same sex couples', 'V201411x':'Transgender Policy', 'V201420x':'Birthright Citizenship',
               'V201423x':'Should children brought illegally be sent back','V201426x':'Wall on border with Mexico',
               'V201429':'Best way to deal with Urban Unrest','V201605x':'Political Violence compared to 4 years ago',
               'V202236x':'Allowing refugees to come to US','V202239x':'Effect of Illegal inmigration on crime rate',
               'V202242x':'Providing path to citizenship','V202245x':'Returning unauthorized immigrants to native country',
               'V202248x':'Separating children from detained immigrants','V202255x':'Less or more Government',
               'V202256':'Good for society to have more government regulation',
               'V202259x':'Government trying to reduce income inequality','V202276x':'People in rural areas get more/less from Govt.',
               'V202279x':'People in rural areas have too much/too little influence','V202282x':'People in rural areas get too much/too little respect',
               'V202286x':'Easier/Harder for working mother to bond with child','V202290x':'Better/Worse if man works and woman takes care of home',
               'V202320x':'Economic Mobility compared to 20 years ago','V202328x':'Obamacare','V202331x':'Vaccines in Schools',
               'V202336x':'Regulation on Greenhouse Emissions','V202341x':'Background checks for guns purchases',
               'V202344x':'Banning "Assault-style" Rifles','V202347x':'Government buy back of "Assault-Style" Rifles',
               'V202350x':'Government action about opiod drug addiction','V202361x':'Free trade agreements with other countries',
               'V202376x':'Federal program giving 12K a year to citizens','V202380x':'Government spending to help pay for health care',
               'V202383x':'Health benefits of vaccination outweigh risks','V202390x':'Trasgender people serve in military',
               'V202490x':'Government treats whites or blacks better','V202493x':'Police treats whites or blacks better',
               'V202542':'Use Facebook','V202544':'Use Twitter'}

labels = list(dict_labels.keys())

labels_pre = list()
labels_post = list()

for label in labels:
    if label[3] == "1":
        labels_pre.append(label)
    elif label[3] == "2":
        labels_post.append(label)


# labels_politicos = ['V201200','V201231x','V201342x','V201345x','V201372x','V201382x','V201386x','V201408x','V201411x',
#                     'V201420x','V201426x','V201605x','V202255x','V202256','V202259x','V202328x','V202336x','V202390x']

# labels_apoliticos = ['V201405x','V201423x','V201429','V202236x','V202239x','V202276x','V202279x','V202282x','V202286x',
#                      'V202290x','V202320x','V202331x','V202341x','V202344x','V202347x','V202350x','V202361x','V202376x',
#                      'V202383x','V202542','V202544']

# labels_dudosos = ['V201225x','V201246','V201249','V201252','V201255','V201258','V201262','V201356x','V201362x','V201375x',
#                   'V202242x','V202245x','V202248x','V202380x','V202490x','V202493x']

# Primer Filtro

labels_politicos = ['V201200','V201231x','V201372x','V201386x','V201408x',
                    'V201411x','V201420x','V201426x','V202255x','V202328x','V202336x']

labels_apoliticos = ['V201429','V202320x','V202331x','V202341x','V202344x',
                     'V202350x','V202383x']

labels_dudosos = ['V201225x','V201246','V201249','V201252','V201255','V201258',
                  'V201262','V202242x','V202248x']

labels_filtrados = labels_politicos + labels_apoliticos + labels_dudosos

#############################################################################################

df_data_aux = df_raw_data[labels]
df_data = pd.DataFrame()

for code in labels_filtrados:
    df_data[code] = df_data_aux[code].apply(data_processor)
    
df_data[['V200010a','V200010b']] = df_raw_data[['V200010a','V200010b']]

#############################################################################################

# Gráfico de dos preguntas simultáneas con distribuciones individuales en los ejes
"""
weights = 'V200010b'

for i,code_1 in enumerate(labels_politicos):
    for code_2 in labels_politicos[i+1::]:
        
        df_aux = df_data.loc[(df_data[code_1]>0) & (df_data[code_2]>0)]
        
        plt.rcParams.update({'font.size': 28})
        # plt.figure(figsize=(40,21))
        sns.jointplot(df_aux, x=code_1, y=code_2, kind="hist", vmin=0, cmap='inferno', height = 15,
                      joint_kws={'discrete': True, 'weights': df_aux[weights]}, 
                      marginal_kws={'discrete': True, 'weights': df_aux[weights]})
        plt.xlabel(dict_labels[code_1])
        plt.ylabel(dict_labels[code_2])
        plt.gca().invert_yaxis()
        direccion_guardado = Path("../../../Imagenes/Distribucion_ANES/2020/Politicos/{}vs{}.png".format(code_1,code_2))
        plt.savefig(direccion_guardado ,bbox_inches = "tight")
        plt.close()
        

for i,code_1 in enumerate(labels_apoliticos):
    for code_2 in labels_apoliticos[i+1::]:
        
        df_aux = df_data.loc[(df_data[code_1]>0) & (df_data[code_2]>0)]
        
        plt.rcParams.update({'font.size': 28})
        # plt.figure(figsize=(40,21))
        sns.jointplot(df_aux, x=code_1, y=code_2, kind="hist", vmin=0, cmap='inferno', height = 15,
                      joint_kws={'discrete': True, 'weights': df_aux[weights]}, 
                      marginal_kws={'discrete': True, 'weights': df_aux[weights]})
        plt.xlabel(dict_labels[code_1])
        plt.ylabel(dict_labels[code_2])
        # plt.gca().invert_yaxis()
        direccion_guardado = Path("../../../Imagenes/Distribucion_ANES/2020/No Politicos/{}vs{}.png".format(code_1,code_2))
        plt.savefig(direccion_guardado ,bbox_inches = "tight")
        plt.close()


for i,code_1 in enumerate(labels_dudosos):
    for code_2 in labels_dudosos[i+1::]:
        
        df_aux = df_data.loc[(df_data[code_1]>0) & (df_data[code_2]>0)]
        
        plt.rcParams.update({'font.size': 28})
        # plt.figure(figsize=(40,21))
        sns.jointplot(df_aux, x=code_1, y=code_2, kind="hist", vmin=0, cmap='inferno', height = 15,
                      joint_kws={'discrete': True, 'weights': df_aux[weights]}, 
                      marginal_kws={'discrete': True, 'weights': df_aux[weights]})
        plt.xlabel(dict_labels[code_1])
        plt.ylabel(dict_labels[code_2])
        # plt.gca().invert_yaxis()
        direccion_guardado = Path("../../../Imagenes/Distribucion_ANES/2020/Dudosos/{}vs{}.png".format(code_1,code_2))
        plt.savefig(direccion_guardado ,bbox_inches = "tight")
        plt.close()


#############################################################################################


plt.rcParams.update({'font.size': 28})

for code in labels_politicos:
    
    if code[3] == '1':
        weights = 'V200010a'
    elif code[3] == '2':
        weights = 'V200010b'
    
    # Set the figure size
    plt.figure(figsize=(20, 15))  # Adjust width and height as needed
    sns.histplot(df_data.loc[df_data[code]>0], x=code, weights=weights, discrete=True)
    plt.xlabel(dict_labels[code])
    direccion_guardado = Path("../../../Imagenes/Distribucion_ANES/2020/Politicos/Histograma {}.png".format(code))
    plt.savefig(direccion_guardado ,bbox_inches = "tight")
    plt.close()
    
    
for code in labels_apoliticos:
    
    if code[3] == '1':
        weights = 'V200010a'
    elif code[3] == '2':
        weights = 'V200010b'
    
    # Set the figure size
    plt.figure(figsize=(20, 15))  # Adjust width and height as needed
    sns.histplot(df_data.loc[df_data[code]>0], x=code, weights=weights, discrete=True)
    plt.xlabel(dict_labels[code])
    direccion_guardado = Path("../../../Imagenes/Distribucion_ANES/2020/No Politicos/Histograma {}.png".format(code))
    plt.savefig(direccion_guardado ,bbox_inches = "tight")
    plt.close()
    

for code in labels_dudosos:
    
    if code[3] == '1':
        weights = 'V200010a'
    elif code[3] == '2':
        weights = 'V200010b'
    
    # Set the figure size
    plt.figure(figsize=(20, 15))  # Adjust width and height as needed
    sns.histplot(df_data.loc[df_data[code]>0], x=code, weights=weights, discrete=True)
    plt.xlabel(dict_labels[code])
    direccion_guardado = Path("../../../Imagenes/Distribucion_ANES/2020/Dudosos/Histograma {}.png".format(code))
    plt.savefig(direccion_guardado ,bbox_inches = "tight")
    plt.close()

"""
Tiempo(t0)