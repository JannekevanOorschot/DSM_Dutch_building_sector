# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 13:29:39 2021

@author: jvano
"""

import pandas
import geopandas as gpd
import os, glob

#WLO = ['h_', 'l_']
WLO = ['l_']

#scenario = ['WLO_hoog_DichtBij_Sloop_', 'WLO_laag_Ruim_Sloop_']
scenario = ['WLO_hoog_Ruim_Sloop_']
# WLO_hoog_DichtBij_Sloop_appartement

materialen = ['Staal', 'Koper', 'Aluminium', 'Overig_met', 'Hout', 'Beton', 'Baksteen','Overige_co','Glas', 'Keramiek', 'Plastic', 'Isolatie', 'Overig']

os.chdir('C:/Users/jvano/OneDrive - Universiteit Leiden/Files/PBL (monitoring & sturing CE)/Bouw/DSM/Data/SJ_sloop_v2/SJ_sloop_Output_niet_gdb')

#%%



for s in scenario:        
    file_1 = gpd.read_file(s+'appartement.shp')
    file_2 = gpd.read_file(s+'Detailhandel.shp')
    file_3 = gpd.read_file(s+'NijverheidEnLogistiek.shp')
    file_4 = gpd.read_file(s+'Kantoor.shp')
    file_5 = gpd.read_file(s+'losstaand.shp')
    file_6 = gpd.read_file(s+'rijtjeswoning.shp')
    file_7 = gpd.read_file(s+'Overheid_kw_diensten.shp')
    
    for index, mat in enumerate(materialen):

        file_sum = file_1.loc[:,mat] + file_2.loc[:, mat] + file_3.loc[:, mat]+file_4.loc[:, mat]+file_5.loc[:, mat] + file_6.loc[:, mat] + file_7.loc[:, mat]
        
        if index == 0:
            file_y = file_1.copy()
        
        file_y.loc[:,mat]=file_sum

        
    file_y.to_file('C:/Users/jvano/OneDrive - Universiteit Leiden/Files/PBL (monitoring & sturing CE)/Bouw/DSM/Data/SJ_sloop_v2/SJ_Sloop_gem/'+s+'totaal.shp')


    
