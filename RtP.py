# Import modules
import arcpy, arcinfo
import pandas as pd
import numpy as np
import glob, os

from arcpy import env
from arcpy.sa import *

arcpy.env.overwriteOutput = True
#Enable ArcGIS extensions
arcpy.CheckOutExtension("Spatial")

# Raster to Polygons

os.chdir('C:\Users\jvano\OneDrive - Universiteit Leiden\Files\PBL (monitoring & sturing CE)\Bouw\DSM\Python\ArcPy\Output_ArcPy_v2\EbA')
for file1 in glob.glob("*.tif"):          
    filename = os.path.splitext(file1)[0]
    arcpy.RasterToPolygon_conversion(file1, r'C:\Users\jvano\OneDrive - Universiteit Leiden\Files\PBL (monitoring & sturing CE)\Bouw\DSM\Python\ArcPy\Output_ArcPy_v2\RtP/'+filename+'.shp', 'NO_SIMPLIFY', 'Value', 'SINGLE_OUTER_PART', '#')
    print('RtP, Done with : '+filename)

print('Done with Raster to Polygon')
