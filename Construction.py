# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 14:55:55 2021

@author: jvano
"""

#%% Import input data & modules

#import arcpy
import pandas as pd
import geopandas as gpd
import glob, os

gebouwtypen_afk = ['appartement', 'Detailhandel', 'Kantoor', 'losstaand', 'NijverheidEnLogistiek', 'Overheid_kw_diensten',  'rijtjeswoning']

gebouwtypen = ['appartement', 'winkel', 'kantoor', 'vrijstaand', 'industrie', 'overheid', 'serieel']

#_overheid_kw_diensten == diensten
# _losstaand == vrijstaand
# _NijverheidEnLogistiek == industrie
# serieel = _rijtjeswoning

#%%
#Material intensities scenario 1 (Conventional)
MI_s1 = pd.read_excel(r'MI_scenarios.xlsx', sheet_name = 'Conventional')
MI_s1 = MI_s1.set_index('Type gebouw')

#Material intensities scenario 2 (Biobased)
MI_s2 = pd.read_excel(r'MI_scenarios.xlsx', sheet_name = 'Biobased')
MI_s2 = MI_s2.set_index('Type gebouw')

#Material intensities scenario 3 (Circular)
MI_s3 = pd.read_excel(r'MI_scenarios.xlsx', sheet_name = 'Circular')
MI_s3 = MI_s3.set_index('Type gebouw')

# list of materials analyzed
material_columns = list(MI_s1.columns)

mat_scenario = [MI_s1, MI_s2, MI_s3]


# UFA BAU (UFA in Dutch = GO)
GO_BAU = pd.read_excel(r'GO_nr_ftprint_BAG.xlsx', sheet_name = 'BAU')
GO_BAU = GO_BAU.set_index('Unnamed: 0')

# UFA small: x 0,8
GO_Kleiner = pd.read_excel(r'GO_nr_ftprint_BAG.xlsx', sheet_name = 'GO_small')
GO_Kleiner = GO_Kleiner.set_index('Unnamed: 0')

# UFA large: x 1,2
GO_Groter = pd.read_excel(r'GO_nr_ftprint_BAG.xlsx', sheet_name = 'GO_large')
GO_Groter = GO_Groter.set_index('Unnamed: 0')

GOs = [GO_BAU, GO_Kleiner, GO_Groter]
    
#%% Calculate construction per material per cohort for 2 socio-economic scenarios (WLO High (Hoog) & WLO Low (Laag)), 
# 3 urbanization scenario (Urban (Dichtbij), Connected (Verbonden) and Rural (Ruim)), 3 UFA scenarios (GO klein, GO groot, GO BAU)
# and 3 building construction scenarios (M1 Conventional, M2 Biobased and M3 Circular)
# and 7 building types

#All maps
os.chdir('C:/.../RtP')

WLO = ['WLO_hoog_', 'WLO_laag_']
scenario = ['DichtBij_', 'Verbonden_', 'Ruim_']

for w in WLO:
    for s in scenario:
        for (a,b) in zip(gebouwtypen, gebouwtypen_afk):
            file = gpd.read_file(w+s+'Bouw_'+b+'.shp')
            filename = w+s+'Bouw_'+b
            print('Start with: '+filename)
            file['gridcode_II']=file['gridcode']*(file['POLY_AREA']/10000)
            for index, g in enumerate(GOs):
                if index == 0:
                    gnaam = 'GO_BAU'
                elif index == 1:
                    gnaam = 'GO_Klein'
                elif index == 2: 
                    gnaam = 'GO_Groot'
                for index, MI in enumerate(mat_scenario):
                    ms = 'M'+str(index)
                    for m in material_columns:
                        file[m] = file['gridcode_II']*g.loc[a, 'omrekenfactor']*MI.loc[a,m]
                    file.to_file('C:/Users/jvano/OneDrive - Universiteit Leiden/Files/PBL (monitoring & sturing CE)/Bouw/DSM/Data/Output_DSM_378_v4/'+filename+'_'+gnaam+'_'+ms+'.shp') 

#%% Data output files: 2 (WLO) * 3 (Dichtbij, Verbonden, Ruim) * 7 (gebouwtypen) * 3 (GO scenario's ) * 3 (MI scenario's ) = 378 maps
# Data editing: totalen per scenario berkenen (Excel) voor de 7 gebouwtypen: 54 in totaal

# Alle 378 kaarten:
os.chdir('C:/Output_378')

# sommige mateiraalnamen zijn afgekort in vorige stap
materialen = ['Aluminium', 'Baksteen', 'Beton', 'Bitumen', 'Electronic', 'Gips', 'Glas', 'Hout', 'Isolatie', 'Kalkzandst', 'Keramiek', 'Koper', 'Kunststoff', 'Lijm en ve', 'Mortel', 'Overig bio', 'Overige me', 'Papier', 'Staal & IJ', 'Steen', 'Zand']

WLO = ['WLO_hoog_', 'WLO_laag_']
scenario = ['DichtBij_Bouw_', 'Verbonden_Bouw_', 'Ruim_Bouw_']
factor = ['GO_BAU', 'GO_Klein', 'GO_Groot']
MI_s = ['M0', 'M1', 'M2']


#format: WLO_hoog_DichtBij_Bouw_appartement_GO_BAU_M0.shp

totaal_bouw = pd.DataFrame(index = gebouwtypen, columns = materialen)

for w in WLO:
    for s in scenario: 
        for s1 in MI_s:
            for f in factor: 
                for (a,b) in zip(gebouwtypen, gebouwtypen_afk):
                    file1 = gpd.read_file(w+s+b+'_'+f+'_'+s1+'.shp')
                    filename = w+s+'_'+b+'_'+f+'_'+s1
                    for m in materialen:
                        totaal_bouw.loc[a,m] = file1.loc[:,m].sum()
                                
                print('Klaar met: '+filename)
                totaal_bouw.to_excel('C:/.../Output_54/Tot_bouw_'+w+'_'+s+'_'+s1+'_'+f+'.xlsx')
                
            
                
