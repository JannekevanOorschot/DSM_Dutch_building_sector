# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# SJ_sloop.py
# Created on: 2021-09-22 14:45:15.00000
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os

workspace = r"C:\Users\jvano\OneDrive - Universiteit Leiden\Files\PBL (monitoring & sturing CE)\Bouw\DSM\Data\SJ_sloop_v2\SJ_sloop_input.gdb"
outWorkspace = r"C:\Users\jvano\OneDrive - Universiteit Leiden\Files\PBL (monitoring & sturing CE)\Bouw\DSM\Data\SJ_sloop_v2\SJ_sloop_output.gdb"

#scenario = ['WLO_hoog_DichtBij_Sloop_', 'WLO_laag_Ruim_Sloop_']
scenario = ['WLO_hoog_Ruim_Sloop_']
gebouwen = ['appartement', 'Detailhandel', 'NijverheidEnLogistiek', 'Kantoor', 'losstaand', 'rijtjeswoning', 'Overheid_kw_diensten']

for s in scenario:
    for g in gebouwen:
        name = s+g
        print(name)
        
        targetFeatures = os.path.join(workspace, "Gemeenten")
        joinFeatures = os.path.join(workspace, name)

        outfc = os.path.join(outWorkspace, name)
        
        # Create a new fieldmappings and add the two input feature classes.
        fieldmappings = arcpy.FieldMappings()
        fieldmappings.addTable(targetFeatures)
        fieldmappings.addTable(joinFeatures)
        
        # field: gridcode
        gd = fieldmappings.findFieldMapIndex("gridcode")
        fieldmap = fieldmappings.getFieldMap(gd)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(gd, fieldmap) 
        # field: bouwjaar
        bj = fieldmappings.findFieldMapIndex("bouwjaar")
        fieldmap = fieldmappings.getFieldMap(bj)
        field = fieldmap.outputField
        fieldmap.mergeRule = "mean"
        fieldmappings.replaceFieldMap(bj, fieldmap)           
        # field: GO
        GO = fieldmappings.findFieldMapIndex("GO")
        fieldmap = fieldmappings.getFieldMap(GO)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(GO, fieldmap)
        # field: Staal
        stl = fieldmappings.findFieldMapIndex("Staal")
        fieldmap = fieldmappings.getFieldMap(stl)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(stl, fieldmap)
        # field: Koper
        cu = fieldmappings.findFieldMapIndex("Koper")
        fieldmap = fieldmappings.getFieldMap(cu)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(cu, fieldmap)
        # field: Aluminium
        al = fieldmappings.findFieldMapIndex("Aluminium")
        fieldmap = fieldmappings.getFieldMap(al)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(al, fieldmap)
        # field: Overig metaal
        ov_m = fieldmappings.findFieldMapIndex("Overig_met")
        fieldmap = fieldmappings.getFieldMap(ov_m)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(ov_m, fieldmap)
        # field: Hout
        h = fieldmappings.findFieldMapIndex("Hout")
        fieldmap = fieldmappings.getFieldMap(h)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(h, fieldmap)
        # field: Beton
        bet = fieldmappings.findFieldMapIndex("Beton")
        fieldmap = fieldmappings.getFieldMap(bet)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(bet, fieldmap)
        # field: Baksteen
        bak = fieldmappings.findFieldMapIndex("Baksteen")
        fieldmap = fieldmappings.getFieldMap(bak)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(bak, fieldmap)
        # field: Overig constructiemineraal
        ov_co = fieldmappings.findFieldMapIndex("Overige_co")
        fieldmap = fieldmappings.getFieldMap(ov_co)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(ov_co, fieldmap)
        # field: Glas
        gl = fieldmappings.findFieldMapIndex("Glas")
        fieldmap = fieldmappings.getFieldMap(gl)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(gl, fieldmap)
        # field: Keramiek
        ke = fieldmappings.findFieldMapIndex("Keramiek")
        fieldmap = fieldmappings.getFieldMap(ke)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(ke, fieldmap)
        # field: Plastic
        pl = fieldmappings.findFieldMapIndex("Plastic")
        fieldmap = fieldmappings.getFieldMap(pl)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(pl, fieldmap)
        # field: Isolatie
        iso = fieldmappings.findFieldMapIndex("Isolatie")
        fieldmap = fieldmappings.getFieldMap(iso)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(iso, fieldmap)
        # field: Overig
        ove = fieldmappings.findFieldMapIndex("Overig")
        fieldmap = fieldmappings.getFieldMap(ove)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(ove, fieldmap)

        # delete fields
        x = fieldmappings.findFieldMapIndex("gebr_woonf")
        fieldmappings.removeFieldMap(x)
        
        z = fieldmappings.findFieldMapIndex("Unnamed__1")
        fieldmappings.removeFieldMap(z)
        
        arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outfc,'#', '#', fieldmappings)

        
        

                       
