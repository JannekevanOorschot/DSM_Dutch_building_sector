# -*- coding: utf-8 -*-
"""
Created on Tue May 11 10:00:46 2021

@author: jvano

"""

#%% import and explore data

import pandas as pd
import numpy as np
import geopandas as gpd
import glob, os

os.chdir('C:/...')
gemeenten = []
for shpfile in glob.glob("*.shp"):
    filename = os.path.splitext(shpfile)[0]
    gemeenten.append(filename)


#%% load Files & edit Material DataBase
M_total_NL = pd.DataFrame()
M_total_gem = pd.DataFrame()

building_types = ['vrijstaand', 'serieel', 'appartement', 'winkel', 'kantoor', 'industrie', 'overheid', 'overig']

# Building stock data per municipality (355 in total)
os.chdir('C:/...')

all_years = np.arange(1900,2019,1)
I_gebouwen = pd.DataFrame(0, index = all_years, columns = building_types)
        
#%%    
gemeenten = []
for shpfile in glob.glob("*.shp"):
    filename = os.path.splitext(shpfile)[0]
    gemeenten.append(filename)

# Reclassified_II is "overig" aan toegevoegd, voor ongeclassificeerde BAG elementen (vaak schuurtjes etc.), is gemiddelde van alle andere gebouwen genomen
MI_db = pd.read_excel(r'C:/...MI_historic.xlsx')
 
MI_db['Type gebouw'] = MI_db['Type gebouw'].fillna(method='ffill')
tuples = list(zip(MI_db['Type gebouw'], MI_db['Cohort']))

MI_db.index = tuples
MI_db.drop(['Type gebouw', 'Cohort'], axis = 1, inplace = True)

material_columns = list(MI_db.columns)

material_index = list(MI_db.index)

#%% Loop door gemeenten Shapefiles 


for file in glob.glob("*.shp"):       
    
    BAGx = gpd.read_file(file)
    
    BAG = BAGx[['bouwjaar', 'status', 'gebruiks_1', 'geometry', 'GO','shape_Area', 'gebr_woonf' ]].copy()
    
    #2018 is start jaar, dus bouw na 2018 uit bestand verwijderen
    built_after_2018 = BAG[ BAG['bouwjaar'] > 2018].index
    BAG.drop(built_after_2018, inplace = True)
    
    filename = os.path.splitext(file)[0]
    print(filename)
    woningtypering = gpd.read_file(r'C:/.../'+filename+'.shp')
    
    # appartement : woning waaraan meerdere verblijfsobjecten zijn gerelateerd, ongeacht het gebruiksdoel van deze verblijfsobjecten, minimaal één 'woonfunctie'
    # vrijstaande woning: woning zonder andere verbonden verblijfsobjecten
    # tussen- of geschakelde woning: woning die met meerdere panden met een verblijsobject is verbonden, ook geschakelde woningen. 
    # hoekwoning: eerste of laatste woning in een serie panden. 
    # twee-onder-een-kap: deze woning is verbonden met een enkel pand met een verblijsobject en dit pand is alleen met het eerstgenoemde pand verbonden. 
    woningtypering = woningtypering[['Woningtype', 'geometry']]
    

#%% Spatial join woningtypering & BAG

    BAG_1 = gpd.sjoin(BAG, woningtypering, how = 'left', op = 'intersects')
    BAG_1 = BAG_1[~BAG_1.index.duplicated(keep='first')]
    

#%% Classificatie gebouwen MB

# Classificatie (op basis van GO)

    # grofweg 1/4 van de data is ongeclassificeerd: het overgrootte schuurtjes/kleine huisjes in tuinen. 
    
    BAG_1['Class'] = np.NaN

    BAG_1['Class'].loc[((BAG_1.gebruiks_1 == 'kantoorfunctie') |\
                        (BAG_1.gebruiks_1 == 'bijeenkomstfunctie') |\
                            (BAG_1.gebruiks_1 == 'logiesfunctie'))] = 'kantoor' # voor m2 kantoor & bijeenkomst is < 5.000 gekozen, dit is het miden van de range in m2 voor de categorie middelgroot
          
    BAG_1['Class'].loc[((BAG_1.gebruiks_1 == 'onderwijsfunctie') | \
                        (BAG_1.gebruiks_1 == 'gezondheidszorgfunctie') | \
                            (BAG_1.gebruiks_1 == 'celfunctie') | \
                                (BAG_1.gebruiks_1 == 'overige gebruiksfunctie') | \
                                        (BAG_1.gebruiks_1 == 'sportfunctie'))] = 'overheid'
        
    BAG_1['Class'].loc[(BAG_1['gebruiks_1']).isna()] = 'overig'
    
    BAG_1['Class'].loc[(BAG_1.gebruiks_1 == 'winkelfunctie')] = 'winkel'
    
    BAG_1['Class'].loc[(BAG_1.gebruiks_1 == 'industriefunctie')] = 'industrie' # aannemened industrie is gelijk aan bedrijfshal / distributiecentrum

    BAG_1['Class'].loc[((BAG_1.Woningtype == 'vrijstaande woning') | (BAG_1.Woningtype == 'twee-onder-een-kap' ))] = "vrijstaand" 
    
    BAG_1['Class'].loc[((BAG_1.Woningtype == 'tussenwoning/geschakeld') | (BAG_1.Woningtype == 'hoekwoning' ))] = "serieel"
    
    BAG_1['Class'].loc[(BAG_1.Woningtype == 'appartement')] = "appartement" # tot 6 lagen, 6*3 meter per etage = 18m
         

#%% Sort per building year
    
    for building_type in building_types:
        summed_buildingtype = BAG_1['GO'].loc[(BAG_1.bouwjaar <= 1900) & (BAG_1.Class == building_type)].sum()
        I_gebouwen.at[1900, building_type] = I_gebouwen.at[1900, building_type] + summed_buildingtype
        for year in all_years:
            if year != 1900:
                summed_buildingtype = BAG_1['GO'].loc[(BAG_1.bouwjaar == year) & (BAG_1.Class == building_type)].sum()
                I_gebouwen.at[year, building_type] = I_gebouwen.at[year, building_type] + summed_buildingtype


#%% Add building material intensities

    BAG_copy = BAG_1.copy()
#    floor_height = 3 # MI in kg/m2, Materiaal(kg/m2) = opp(m)*hoogte(m)/floor_height(mi)*MI (kg/m2)

    cohort_names = ['<1945', '1945-1970', '1970-2000', '>2000']
    cohort_ranges = [[0,1945], [1945,1970], [1970, 2000],[2000,3000]]

    #BAG_copy['floor_area'] = BAG_copy.loc[:,'Opp_BVO']

    for material in material_columns:
        BAG_copy[material]=np.nan

    for index,cohort in enumerate(cohort_ranges): #  maakt 2 kolommen, index 1,2,3,4,... + waarde (cohort)
        for building_type in building_types:
            BAG_class_cohort_filter = ((BAG_copy['bouwjaar'] >= cohort[0]) & (BAG_copy['bouwjaar'] < cohort[1]) & (BAG_copy['Class'] == building_type))
            BAG_filtered = BAG_copy[BAG_class_cohort_filter]
            for material in material_columns:
                index_name = (building_type, cohort_names[index])
                material_intensity = MI_db.at[index_name, material]          
                BAG_filtered[material] = BAG_filtered.loc[:,'GO']*material_intensity
                BAG_copy[BAG_class_cohort_filter] = BAG_filtered
    
    
    BAG_copy.to_file("C:\.../"+filename+"_voorraden.shp")


 
#%% Calculate total materialintensities in municipality for each class

    M_total_class = pd.DataFrame(columns = material_columns, index = material_index)

    for material in material_columns:
        value = BAG_copy[material].sum()
        M_total_gem.at[os.path.splitext(filename)[0], material] = value
        for building_type in building_types:
            for index,cohort in enumerate(cohort_ranges): #  maakt 2 kolommen, index 1,2,3,4,... + waarde (cohort)
                BAG_class_filter = ((BAG_copy['bouwjaar'] >= cohort[0]) & (BAG_copy['bouwjaar'] < cohort[1]) & (BAG_copy['Class'] == building_type))
                BAG_filtered = BAG_copy[BAG_class_filter]
                value1 = BAG_filtered[material].sum()
                index_name = (building_type, cohort_names[index])
                M_total_class.at[index_name, material]=value1
                
    M_total_NL = M_total_NL.add(M_total_class, fill_value=0)

    print("Einde loop: "+filename)
    
M_total_gem.to_excel('C:/.../M_totalen_gemeentes.xlsx')
M_total_NL.to_excel('C:/.../M_totalen_MB.xlsx')  


I_gebouwen.to_excel('C:/.../Inflow_gebouwen_hist.xlsx')

