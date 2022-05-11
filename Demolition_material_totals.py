# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 08:52:04 2021

Sums demolition data                                                                                                                         

@author: jvano
"""
#%%
import pandas as pd
import geopandas as gpd
import glob, os

os.chdir('C:/.../Merge')


gebouwtypen = ['vrijstaand', 'serieel', 'appartement', 'winkel', 'kantoor', 'industrie', 'overheid']
gebouwtypen_afk = ['appartement', 'Detailhandel', 'Kantoor', 'losstaand', 'NijverheidEnLogistiek', 'Overheid_kw_diensten',  'rijtjeswoning']
materialen = ['Staal', 'Koper', 'Aluminium', 'Overig_met', 'Hout', 'Beton', 'Baksteen','Overige_co','Glas', 'Keramiek', 'Plastic', 'Isolatie', 'Overig']
WLO = ['WLO_hoog_', 'WLO_laag_']
scenario = ['Ruim_Sloop', 'Verbonden_Sloop', 'DichtBij_Sloop']

filenames = []
for shpfile in glob.glob("*.shp"):
    filename = os.path.splitext(shpfile)[0]
    filenames.append(filename)


Totalen_sloop = pd.DataFrame(index = gebouwtypen, columns = materialen)


#%%

for w in WLO:
    for s in scenario:
        file1 = gpd.read_file(w+s+'.shp')
        for gt in gebouwtypen:
            fil = file1['Class'] == gt
            filt = file1[fil]
            for mat in materialen:         
                Totalen_sloop.loc[gt, mat] = filt.loc[:,mat].sum()
                        
        
        Totalen_sloop.to_excel('C:/.../Totalen_'+w+s+'.xlsx')