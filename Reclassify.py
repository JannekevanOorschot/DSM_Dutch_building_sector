############################################################################################################################################################################################
# Adjust building classifications of scenario data to align with material intensity and BAG data
# Requirements: Spatial Analyst Extension

# 1. Import modules
import arcpy, arcinfo
import pandas as pd
import numpy as np
import glob, os

from arcpy import env
from arcpy.sa import *

arcpy.env.overwriteOutput = True


#Enable ArcGIS extensions
arcpy.CheckOutExtension("Spatial")


############################################################################################################################################################################################

# 2. Calculate missing values: Stock 2018 workspace (Basisjaar werken) & Demolition of dwellings (Sloop woningen)

# 2.1. Basisjaar Werken (2018)(5) = Restant Basisjaar (2050) (5 type werk) + sloop voorraad (2050) (5 type werk)


type_werk = ['WLO_hoog_DichtBij_Werken_Detailhandel', 'WLO_hoog_DichtBij_Werken_NijverheidEnLogistiek', 'WLO_hoog_DichtBij_Werken_Ov_consumentendiensten', 'WLO_hoog_DichtBij_Werken_Overheid_kw_diensten', 'WLO_hoog_DichtBij_Werken_Zak_dienstverlening']

for werk in type_werk:
    werk_type = werk[25:]
    Restant = 'C:\.../'+werk+'.tif'
    Sloop = 'C:\.../'+werk+'.tif'
    Basisjaar = Raster(Restant) + Raster(Sloop)
    Basisjaar.save('C:\.../Basisjaar_'+werk_type+'.tif')
    

# 2.2. Sloop Woningen (2050)(24) = Basisjaar Wonen - Restant Basijsaar

type_wonen = ['rijtjeswoning', 'vrijstaand', 'appartement', 'twee_onder_1_kap']
WLO = ['WLO_hoog', 'WLO_laag']
DVR = ['DichtBij', 'Verbonden', 'Ruim']
for wel in WLO:
    for loc in DVR:
        for woning in type_wonen:
            Basisjaar = 'C:\.../Basisjaar_'+woning.capitalize()+'.tif'
            Restant = 'C:\.../'+wel+'_'+loc+'_'+'RestantBasisjaar_'+woning+'.tif'
            Sloop = Raster(Basisjaar) - Raster(Restant)
            Sloop.save('C:\.../'+wel+'_'+loc+'_Sloop_'+woning+'.tif')

############################################################################################################################################################################################
             
# 3. Adjust classifications

# Detailhandel --> Winkel (shop)
# NijverheidEnLogistiek --> Industrie (industry)
# Ov_consumentendiensten + Zak_dienstverlening --> Kantoor (office)
# Overheid_kw_diensten --> Overheid (services) 

# vrijstaand + twee_onder_1_kap --> Vrijstaand (detached house)
# appartement --> Appartement (apartment)
# rijtjeswoning --> Serieel (row house)

WW = ['Werken', 'Wonen']
Activiteit = ['Bouw', 'RestantBasisjaar', 'Sloop']

# Basisjaar Wonen: Vrijstaand + Twee_onder_1_kap = losstaand
vrij_b = 'C:\.../Basisjaar_Vrijstaand.tif'
twee_b = 'C:\.../Basisjaar_Twee_onder_1_kap.tif'
vrij2_b = Raster(vrij_b) + Raster(twee_b)
vrij2_b.save('C:\.../Basisjaar_losstaand.tif')

# Basisjaar Werken: Ov_consumentendiensten + Zak_dienstverlening = kantoor
Ov_cons_b = 'C:\...\Basisjaar_Ov_consumentendiensten.tif'
Zak_dienst_b = 'C:\...\Basisjaar_Zak_dienstverlening.tif'
Kantoor_b = Raster(Ov_cons_b) + Raster(Zak_dienst_b)
Kantoor_b.save('C:\...\Basisjaar_Kantoor.tif')

for w in WW:
    for act in Activiteit:
        for wel in WLO:
            for loc in DVR:
                if w == 'Werken':
                    Ov_cons = 'C:\.../'+w+'/'+act+'/'+wel+'_'+loc+'_'+w+'_Ov_consumentendiensten.tif'
                    Zak_dienst = 'C:\.../'+w+'/'+act+'/'+wel+'_'+loc+'_'+w+'_Zak_dienstverlening.tif'
                    Kantoor = Raster(Ov_cons) + Raster(Zak_dienst)
                    Kantoor.save('C:\.../'+w+'/'+act+'/'+wel+'_'+loc+'_'+w+'_Kantoor.tif')
                elif w == 'Wonen':
                    vrij = 'C:\.../'+w+'/'+act+'/'+wel+'_'+loc+'_'+act+'_vrijstaand.tif'
                    twee = 'C:\.../'+w+'/'+act+'/'+wel+'_'+loc+'_'+act+'_twee_onder_1_kap.tif'
                    vrij2 = Raster(vrij) + Raster(twee)
                    vrij2.save('C:\.../'+w+'/'+act+'/'+wel+'_'+loc+'_'+act+'_losstaand.tif')


arcpy.CheckInExtension("spatial")
