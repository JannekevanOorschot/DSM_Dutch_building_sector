# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 14:53:14 2021

Totaal aantal of footprint kwantificeren per gebouwtype in PBL Beginstand data
Totaal GO kwantificeren per gebouwtype uit de BAG (2020 min bouw > 2018)
Omrekenfactor berekenen

@author: jvano
"""

import pandas as pd
import geopandas as gp
import numpy as np

type_gebouwen = ['App', 'Det', 'Kan', 'los', 'Nij', 'Ove', 'Rij']
# App = Appartement
# Det = Winkel
# Kan = Kantoor
# los = Vrijstaand
# Nij = Industrie
# Ove = Overheid
# Rij = Rijtjeswoning

Beginstand = pd.DataFrame(columns = ['Aantal', 'footprint', 'GO','factor_s1', 'factor_s2'], index = [ 'Appartement', 'Winkel', 'Kantoor', 'Vrijstaand','Industrie', 'Overheid', 'Rijtjeswoning'] )

#%% Totalen berekenen in aantallen of footprint gebouwtypen in de Basisstanden PBL
for geb in type_gebouwen:
    Basisstand = gp.read_file(r'C:/Users/jvano/OneDrive - Universiteit Leiden/Files/PBL (monitoring & sturing CE)/Bouw/DSM/Python/ArcPy/Output_ArcPy/RtP/Bas_'+geb+'.shp')
    totaal = Basisstand['gridcode'].sum()
    print('totaal ') 
    print(geb) 
    print('=') 
    print(totaal)
    if geb == 'App':
        Beginstand.iloc[0,0] = totaal
    elif geb == 'Det':
        Beginstand.iloc[1,1] = totaal
    elif geb == 'Kan':
        Beginstand.iloc[2,1] = totaal                        
    elif geb == 'los':
        Beginstand.iloc[3,0] = totaal
    elif geb == 'Nij':
        Beginstand.iloc[4,1] = totaal
    elif geb == 'Ove':
        Beginstand.iloc[5,1] = totaal
    elif geb == 'Rij':
        Beginstand.iloc[6,0] = totaal
        

#%% Totalen berekenen in GO gebouwtypen in de BAG (2020 - bouw > 2018)

# Test data voor 3 gemeenten
# Inflow_hist = pd.read_excel(r'C:/Users/jvano/OneDrive - Universiteit Leiden/Files/PBL (monitoring & sturing CE)/Bouw/DSM/Data/dummy_output_BAG/Inflow_gebouwen_hist_dummy.xlsx')

# Alle gemeenten
Inflow_hist = pd.read_excel(r'C:/Users/jvano/OneDrive - Universiteit Leiden/Files/PBL (monitoring & sturing CE)/Bouw/DSM/Data/Inflow_gebouwen_hist.xlsx')

Beginstand.iloc[0,2] = Inflow_hist['appartement'].sum()
Beginstand.iloc[1,2] = Inflow_hist['winkel'].sum()
Beginstand.iloc[2,2] = Inflow_hist['kantoor'].sum()
Beginstand.iloc[3,2] = Inflow_hist['vrijstaand'].sum()
Beginstand.iloc[4,2] = Inflow_hist['industrie'].sum()
Beginstand.iloc[5,2] = Inflow_hist['overheid'].sum()
Beginstand.iloc[6,2] = Inflow_hist['serieel'].sum()

#%%
for index, row in Beginstand.iterrows():
    if np.isnan(row['Aantal']):
        Beginstand.loc[index,'factor_s1'] = Beginstand.loc[index, 'GO']/Beginstand.loc[index,'footprint']
    elif np.isnan(row['footprint']):
        Beginstand.loc[index,'factor_s2']= Beginstand.loc[index, 'GO']/Beginstand.loc[index, 'Aantal']


Beginstand.iloc[0,4] = Beginstand.iloc[0,4]/2
Beginstand.iloc[1,4] = Beginstand.iloc[1,4]/2
Beginstand.iloc[2,4] = Beginstand.iloc[2,4]/2
Beginstand.iloc[3,4] = Beginstand.iloc[3,4]/2
Beginstand.iloc[4,4] = Beginstand.iloc[4,4]/2
Beginstand.iloc[5,4] = Beginstand.iloc[5,4]/2
Beginstand.iloc[6,4] = Beginstand.iloc[6,4]/2
                
#%%

# Test voor 3 gemeeten
#Beginstand.to_excel('C:/Users/jvano/OneDrive - Universiteit Leiden/Files/PBL (monitoring & sturing CE)/Bouw/DSM/Data/GO_factor_dummy.xlsx')

# Alle gemeenten
Beginstand.to_excel('C:/Users/jvano/OneDrive - Universiteit Leiden/Files/PBL (monitoring & sturing CE)/Bouw/DSM/Data/GO_factor.xlsx')

        
        
    
