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

# Exclude 0 from images (.tif)

os.chdir('C:\...\Int')
for file1 in glob.glob("*.tif"):          
    filename = os.path.splitext(file1)[0]
    arcpy.gp.ExtractByAttributes_sa(file1, '"Value">0', r'C:\.../'+filename+'.tif')
    print('EbA, Done with : '+filename)
    
#print('Done with removing 0's ')
