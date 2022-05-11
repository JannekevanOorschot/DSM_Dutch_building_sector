# Merges demolition results of municipalities
# Requirements: Spatial Analyst Extension

import arcpy
import glob, os

arcpy.env.workspace = "C:\...\Output_SJ.gdb"
shplist = arcpy.ListFeatureClasses('')


WLO = ['WLO_laag_']
scenario = ['Verbonden_', 'Ruim_', 'DichtBij_']
gebouwtypen = ['appartement', 'Detailhandel', 'Kantoor', 'losstaand', 'NijverheidEnLogistiek', 'Overheid_kw_diensten',  'rijtjeswoning']


for w in WLO:
    for s in scenario:
        for gebtyp in gebouwtypen:
            l_filter = []
            for l in shplist:
               if w+s in l and gebtyp in l:
                   l_filter.append(l)
            out = "C:\.../Merge"
            arcpy.Merge_management(l_filter, os.path.join(out, w+s+'Sloop_'+gebtyp+'.shp'))
            print('finished with'+w+s+'Sloop_'+gebtyp)
            
