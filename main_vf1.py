# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:53:35 2022

@author: Vivi
"""

############################ importa módulos e outros arquivos/rotinas ############################

import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
import datetime

###################################################################################################

############################ Leitura de input e criação dos outputs globais #######################
## Indica a versão e a última atualização realizada no script atual ##
version = "v1"
comment = "Desenvolvimento da rotina Watershed challenge"

## Importa a tabela de dados (em excel) para dentro do programa ##
print('[INFO] Carregando Dados as %s' % time.strftime("%H:%M:%S"))

df = pd.read_csv (r'C:\Users\hb87988\Codes_Jupyter_Notebook\Desafio\flux.csv')
print (df)

#base = pd.read_excel(open('C:/Users/hb87988/Codes_Jupyter_Notebook/Desafio/flux.csv','rb'),sheet_name = 'Sheet1') # Dataset 

print('[INFO] Término do carregamento as %s' % time.strftime("%H:%M:%S"))

## Analysis ##
print('columns', df.columns)
print('dTypes', df.dtypes)
print('iloc', df.iloc[1:10])
print('describe', df.describe())
print('info', df.info())



sns.set(rc={'figure.figsize': (14, 8)})
sns.pairplot(df)
sns.heatmap(df.corr(), annot=True, fmt='.2f', linewidths=2)
sns.boxplot(x='flux', y='temp_max', data = df)
sns.boxplot(x='flux', y='precip', data = df)
sns.boxplot(x='temp_max', y='precip', data = df)
sns.jointplot(x='flux',y='precip',data=df, kind='reg')

print('corr', df.corr())


# Plots

def plot_one_timeserie(cod_station, variable, min_date, max_date,df):
    
    df1 = df.loc[df['basin_id'] == cod_station]
    print ('df1:', df1)
    
      
  #  Create figure and plot space

    fig, ax = plt.subplots()
    ax.plot(df1['date'], df1[variable])
    
    ax.set(xlabel='date (s)', ylabel='variable', xlim=[min_date, max_date],
           title='Selected Variable Plot')
    ax.grid()
    
    fig.savefig("test.png")
    plt.show()
    
plot_one_timeserie(1001001,'flux', '1/1/1980', '1/10/1981',df)



def plot_trhree_timeseries(cod_station, variable1, variable2, variable3, min_date, max_date,df):
    

  
    df1 = df.loc[df['basin_id'] == cod_station]
    print ('df1:', df1)
    
  
    normalized1=(df1[variable1]-df1[variable1].min())/(df1[variable1].max()-df1[variable1].min())
    normalized2=(df1[variable2]-df1[variable2].min())/(df1[variable2].max()-df1[variable2].min())
    normalized3=(df1[variable3]-df1[variable3].min())/(df1[variable3].max()-df1[variable3].min())
    
           
 #  Create figure and plot space
   
    fig = plt.figure()

    ax = fig.add_subplot(1, 1, 1)

    ax.plot(df1['date'], normalized1, color='tab:blue')
    ax.plot(df1['date'], normalized2, color='tab:orange')
    ax.plot(df1['date'], normalized3, color='tab:green')
    
    ax.set(xlabel='date (s)', ylabel='variable', xlim=[min_date, max_date],
           title='Selected Variable Plot')
    ax.grid()
    
    fig.savefig("test2.png")
    plt.show()
    
plot_trhree_timeseries(1001001,'flux','precip','temp_max', '1/1/1980', '1/10/1981',df)

# Variables Extreme

   #Evaluating the season of a given date
def season_(date_):
    
    date_2= pd.to_datetime(df['date'])
    print('date_2', date_2)
    print('date to time month', date_2.month)
    print('date to time day', date_2.day)
    
    month = date_2.month
    day = date_2.day
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['day'] = pd.DatetimeIndex(df['date']).day
    
    if df['month'] in (1, 2, 3):
     	df['season'] = 'summer'
    elif df['month'] in (4, 5, 6):
     	df['season'] = 'autumn'
    elif df['month'] in (7, 8, 9):
     	df['season'] = 'winter'
    else:
     	df['season'] = 'spring'
    
    if (df['month'] == 3) and (df['day'] > 19):
     	df['season'] = 'autumn'
    elif (df['month'] == 6) and (df['day'] > 20):
     	df['season'] = 'winter'
    elif (df['month'] == 9) and (df['day'] > 21):
     	df['season'] = 'spring'
    elif (df['month'] == 12) and (df['day'] > 20):
     	df['season'] = 'summer'
    print(df['season'])
        
# season_(df)

    date_2= pd.to_datetime(date_)
    print('date_2', date_2)
    print('date to time month', date_2.month)
    print('date to time day', date_2.day)
    
    month = date_2.month
    day = date_2.day
    
    if month in (1, 2, 3):
    	season = 'summer'
    elif month in (4, 5, 6):
    	season = 'autumn'
    elif month in (7, 8, 9):
    	season = 'winter'
    else:
    	season = 'spring'
    
    if (month == 3) and (day > 19):
    	season = 'autumn'
    elif (month == 6) and (day > 20):
    	season = 'winter'
    elif (month == 9) and (day > 21):
    	season = 'spring'
    elif (month == 12) and (day > 20):
    	season = 'summer'
    print(season)
        
season_('1/10/1980')

for i in df.index:
    df['season']=season_(df['date'])

    # Calculating Extremes
    
# flux_extreme =

df_summer= df.loc[df['season'] == 'summer']
df_winter= df.loc[df['season'] == 'winter']
df_spring= df.loc[df['season'] == 'spring']
df_autumn= df.loc[df['season'] == 'autumn']

p95_flux_summer=df['flux_summer'].quantile(q=0.95)
p95_flux_winter=df['flux_winter'].quantile(q=0.95)
p95_flux_spring=df['flux_spring'].quantile(q=0.95)
p95_flux_autumn=df['flux_autumn'].quantile(q=0.95)

df.loc[df['flux_summer'] > p95_flux_summer, 'flux_extreme'] = '1'
df.loc[df['flux_summer'] <= p95_flux_summer, 'flux_extreme'] = '0' 

df.loc[df['flux_winter'] > p95_flux_winter, 'flux_extreme'] = '1'
df.loc[df['flux_winter'] <= p95_flux_winter, 'flux_extreme'] = '0' 

df.loc[df['flux_spring'] > p95_flux_summer, 'flux_spring'] = '1'
df.loc[df['flux_spring'] <= p95_flux_summer, 'flux_spring'] = '0' 

df.loc[df['flux_autumn'] > p95_flux_summer, 'flux_autumn'] = '1'
df.loc[df['flux_autumn'] <= p95_flux_summer, 'flux_autumn'] = '0' 

print(df['flux_extreme'])

