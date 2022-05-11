# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 13:29:39 2021

@author: jvano
"""

import pandas
import geopandas as gpd
import os, glob


#WLO_hoog_DichtBij_Bouw_appartement_GO_BAU_M0.shp
#scenario = ['WLO_hoog_DichtBij_Bouw_', 'WLO_laag_Ruim_Bouw_']
scenario = ['WLO_hoog_Ruim_Bouw_']

materialen = ['Aluminium', 'Baksteen', 'Beton', 'Bitumen', 'Electronic', 'Gips', 'Glas', 'Hout', 'Isolatie', 'Kalkzandst', 'Keramiek', 'Koper', 'Kunststoff', 'Lijm_en_ve', 'Mortel', 'Overig_bio', 'Overige_me', 'Papier', 'Staal___IJ', 'Steen', 'Zand']
os.chdir('C:/Users/jvano/OneDrive - Universiteit Leiden/Files/PBL (monitoring & sturing CE)/Bouw/DSM/Data/SJ_bouw/SJ_bouw_output_niet_gdb')

#%%

#h_D_Bo_appa_GO_BAU_M0_DSM.shp

for s in scenario:       
    file_1 = gpd.read_file(s+'appartement_GO_BAU_M0.shp')
    file_2 = gpd.read_file(s+'Detailhandel_GO_BAU_M0.shp')
    file_3 = gpd.read_file(s+'NijverheidEnLogistiek_GO_BAU_M0.shp')
    file_4 = gpd.read_file(s+'Kantoor_GO_BAU_M0.shp')
    file_5 = gpd.read_file(s+'losstaand_GO_BAU_M0.shp')
    file_6 = gpd.read_file(s+'rijtjeswoning_GO_BAU_M0.shp')
    file_7 = gpd.read_file(s+'Overheid_kw_diensten_GO_BAU_M0.shp')
    
    for index, mat in enumerate(materialen):

        file_sum = file_1.loc[:,mat] + file_2.loc[:, mat] + file_3.loc[:, mat]+file_4.loc[:, mat]+file_5.loc[:, mat] + file_6.loc[:, mat] + file_7.loc[:, mat]
        
        if index == 0:
            file_y = file_1.copy()
        
        file_y.loc[:,mat]=file_sum

        
    file_y.to_file('C:/Users/jvano/OneDrive - Universiteit Leiden/Files/PBL (monitoring & sturing CE)/Bouw/DSM/Data/SJ_bouw/SJ_bouw_gem/'+s+'_totaal.shp')


