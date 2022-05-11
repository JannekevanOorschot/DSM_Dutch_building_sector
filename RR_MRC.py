# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 12:37:37 2021

@author: jvano
"""

import geopandas as gpd
import pandas as pd
import xlsxwriter

bouw = pd.read_excel('C:/.../Outflow.xlsx', sheet_name = 'Construction')
sloop = pd.read_excel('C:/.../Outflow.xlsx', sheet_name = 'Demolition')
percentage = pd.read_excel('C:/.../Outflow.xlsx', sheet_name = 'Sloop_p')

# empty dataframes with reusable outflow (herbruikbaar) and abundance (teveel), which we will calculate in next cell.
Herbruikbaar = pd.read_excel('C:/.../Outflow.xlsx', sheet_name = 'Herbruikbaar')
Teveel = pd.read_excel('C:/.../Outflow.xlsx', sheet_name = 'Teveel')

GO = ['Baseline', 'Groot', 'Klein']
MI = ['Baseline', 'Biobased', 'Hergebruik']
Sloop_p = ['rr', 'mrc'] #recycling rate & maximum recycled content
WLO = ['Hoog', 'Laag']
Ruimtelijk = ['Dichtbij', 'Verbonden', 'Ruim']

Materialen = ['Beton', 'Baksteen','Overige constructiematerialen', 'Staal & Ijzer', 'Steenwol', 'Glaswol', 'EPS', 'XPS', 'PUR', 'Houtvezels', 'Keramiek', 'Glas', 'Hout beam','Hout board', 'Overig', 'Kunststoffen', 'Aluminium', 'Koper', 'Overige metalen', 'Overige biobased materialen']
#%%
for G in GO:
    for M in MI:
        for W in WLO:
            for R in Ruimtelijk:
                for mat in Materialen:
                    rij_bouw = bouw.loc[(bouw['GO']== G) & (bouw['MI']== M) & (bouw['WLO'] == W) & (bouw['Ruimtelijk']==R)]
                    bouw_m = rij_bouw.loc[:,mat]

                    rij_sloop = sloop.loc[(sloop['WLO'] == W) & (sloop['Ruimtelijk'] == R)]
                    sloop_m = rij_sloop.loc[:, mat]

                    rr = percentage.loc[percentage['Rate'] == 'rr']
                    rr_m = rr.loc[:,mat]*sloop_m.iloc[0]

                    mrc = percentage.loc[percentage['Rate'] == 'mrc']
                    mrc_m = mrc.loc[:,mat]

                    
                    if mat == "Glaswol": # special case because of recycling of glaswool to glaswool + recycling of glas to glaswool, glaswool to glaswool has priority over glas to glaswool
                        if rr_m.iloc[0] <= bouw_m.iloc[0]*mrc_m.iloc[0]: # only if MRC for glass wool production is not reached
                            herbruikbaar_gw = rr_m.iloc[0] #reusable glass wool
                            teveel_gw = 0
                            
                            rr_glas = rij_sloop.loc[:,'Glas']*rr.loc[0,"Glas glaswol"] # % of glass that can be recycled into glasswool
                            leftover_demand = bouw_m.iloc[0] - (herbruikbaar_gw/mrc.loc[:,'Glaswol']) # remaining demand of glasswool
                            
                            if leftover_demand.iloc[0]*mrc.loc[1,'Glas glaswol'] <= rr_glas.iloc[0]:
                                herbruikbaar_glas_gw = leftover_demand.iloc[0]*mrc_m.loc[:,'Glas glaswol']
                                teveel_glas_gw = rr_glas.iloc[0] - herbruikbaar_glas_gw
                            
                            elif leftover_demand.iloc[0]*mrc.loc[1,'Glas glaswol'] > rr_glas.iloc[0]:
                                herbruikbaar_glas_gw = rr_glas.iloc[0]
                                teveel_glas_gw = 0
                        
                            Herbruikbaar['Glas glaswol'].loc[(Herbruikbaar['GO']== G) & (Herbruikbaar['MI']== M) & (Herbruikbaar['WLO'] == W) & (Herbruikbaar['Ruimtelijk']==R)] = herbruikbaar_glas_gw
                            Herbruikbaar['Glaswol'].loc[(Herbruikbaar['GO']== G) & (Herbruikbaar['MI']== M) & (Herbruikbaar['WLO'] == W) & (Herbruikbaar['Ruimtelijk']==R)] = herbruikbaar_gw
                            
                            Teveel['Glas glaswol'].loc[(Teveel['GO']== G) & (Teveel['MI']== M) & (Teveel['WLO'] == W) & (Teveel['Ruimtelijk']==R)] = teveel_glas_gw
                            Teveel['Glaswol'].loc[(Teveel['GO']== G) & (Teveel['MI']== M) & (Teveel['WLO'] == W) & (Teveel['Ruimtelijk']==R)] = teveel_gw

                        elif rr_m.iloc[0] > bouw_m.iloc[0]*mrc_m.iloc[0]:
                            herbruikbaar = bouw_m.iloc[0]*mrc_m.iloc[0]
                            teveel = rr_m.iloc[0] - herbruikbaar    
                            
                            Herbruikbaar['Glas glaswol'].loc[(Herbruikbaar['GO']== G) & (Herbruikbaar['MI']== M) & (Herbruikbaar['WLO'] == W) & (Herbruikbaar['Ruimtelijk']==R)] = 0
                            Teveel['Glas glaswol'].loc[(Teveel['GO']== G) & (Teveel['MI']== M) & (Teveel['WLO'] == W) & (Teveel['Ruimtelijk']==R)] = rij_sloop.loc[:,'Glas']*rr.loc[:,"Glas glaswol"]
                            
                            Herbruikbaar[mat].loc[(Herbruikbaar['GO']== G) & (Herbruikbaar['MI']== M) & (Herbruikbaar['WLO'] == W) & (Herbruikbaar['Ruimtelijk']==R)] = herbruikbaar
                            Teveel[mat].loc[(Teveel['GO']== G) & (Teveel['MI']== M) & (Teveel['WLO'] == W) & (Teveel['Ruimtelijk']==R)] = teveel
                    else:
                        
                        if rr_m.iloc[0] <= bouw_m.iloc[0]*mrc_m.iloc[0]:
                            herbruikbaar = rr_m.iloc[0]
                            teveel = 0
                        elif rr_m.iloc[0] > bouw_m.iloc[0]*mrc_m.iloc[0]:
                            herbruikbaar = bouw_m.iloc[0]*mrc_m.iloc[0]
                            teveel = rr_m.iloc[0] - herbruikbaar
                    
                        Herbruikbaar[mat].loc[(Herbruikbaar['GO']== G) & (Herbruikbaar['MI']== M) & (Herbruikbaar['WLO'] == W) & (Herbruikbaar['Ruimtelijk']==R)] = herbruikbaar
                        Teveel[mat].loc[(Teveel['GO']== G) & (Teveel['MI']== M) & (Teveel['WLO'] == W) & (Teveel['Ruimtelijk']==R)] = teveel

#%%                            
                       
writer = pd.ExcelWriter('Sloop_hergebruik_24022022.xlsx', engine= 'xlsxwriter')
Herbruikbaar.to_excel(writer, sheet_name = 'Herbruikbaar') 
Teveel.to_excel(writer, sheet_name = 'Teveel')          

writer.save()


