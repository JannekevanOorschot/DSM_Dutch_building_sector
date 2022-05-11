# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# SJ_sloop.py
# Created on: 2021-09-24 10:58:15.00000
# Description: Aggregates results for building scenarios from 100x100 meter resolution to municipalities. 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os

arcpy.env.overwriteOutput = True

workspace = r"C:\Users\jvano\OneDrive - Universiteit Leiden\Files\PBL (monitoring & sturing CE)\Bouw\DSM\Data\SJ_bouw/SJ_bouw_input.gdb"
outWorkspace = r"C:\Users\jvano\OneDrive - Universiteit Leiden\Files\PBL (monitoring & sturing CE)\Bouw\DSM\Data\SJ_bouw/SJ_bouw_output.gdb"

#selection = ['WLO_hoog_DichtBij_Bouw_', 'WLO_laag_Ruim_Bouw_']
selection = ['WLO_hoog_Ruim_Bouw_']
gebouwen = ['appartement', 'Detailhandel', 'NijverheidEnLogistiek', 'Kantoor', 'losstaand', 'rijtjeswoning', 'Overheid_kw_diensten']

Materialen = ['Aluminium', 'Baksteen', 'Beton', 'Bitumen', 'Electronic', 'Gips', 'Glas', 'Hout', 'Isolatie', 'Kalkzandst', 'Keramiek', 'Koper', 'Kunststoff', 'Lijm_en_ve', 'Mortel', 'Overig_bio', 'Overige_me', 'Papier', 'Staal___IJ', 'Steen', 'Zand']


for s in selection:
    for geb in gebouwen:
        name = s+geb+'_GO_BAU_M0'
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
        # field: Staal
        stl = fieldmappings.findFieldMapIndex("Staal___IJ")
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
        ov_m = fieldmappings.findFieldMapIndex("Overige_me")
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
        # field: Gips
        gips = fieldmappings.findFieldMapIndex("Gips")
        fieldmap = fieldmappings.getFieldMap(gips)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(gips, fieldmap)
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
        pl = fieldmappings.findFieldMapIndex("Kunststoff")
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
        # field: Lijm en verf
        lijm = fieldmappings.findFieldMapIndex("Lijm_en_ve")
        fieldmap = fieldmappings.getFieldMap(lijm)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(lijm, fieldmap)
        # field: Kalkzandsteen
        Kalkz = fieldmappings.findFieldMapIndex("Kalkzandst")
        fieldmap = fieldmappings.getFieldMap(Kalkz)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(Kalkz, fieldmap)
        # field: Bitumen
        Bitum = fieldmappings.findFieldMapIndex("Bitumen")
        fieldmap = fieldmappings.getFieldMap(Bitum)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(Bitum, fieldmap)
        # field: Zand
        zand = fieldmappings.findFieldMapIndex("Zand")
        fieldmap = fieldmappings.getFieldMap(zand)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(zand, fieldmap)
        # field: Electronics
        Elec = fieldmappings.findFieldMapIndex("Electronic")
        fieldmap = fieldmappings.getFieldMap(Elec)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(Elec, fieldmap)
        # field: steen
        Steen = fieldmappings.findFieldMapIndex("Steen")
        fieldmap = fieldmappings.getFieldMap(Steen)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(Steen, fieldmap)
        # field: Overige biobased materialen
        Bio = fieldmappings.findFieldMapIndex("Overig_bio")
        fieldmap = fieldmappings.getFieldMap(Bio)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(Bio, fieldmap)
        # field: Papier
        Papier = fieldmappings.findFieldMapIndex("Papier")
        fieldmap = fieldmappings.getFieldMap(Papier)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(Papier, fieldmap)
        # field: Mortel
        Mortel = fieldmappings.findFieldMapIndex("Mortel")
        fieldmap = fieldmappings.getFieldMap(Mortel)
        field = fieldmap.outputField
        fieldmap.mergeRule = "sum"
        fieldmappings.replaceFieldMap(Mortel, fieldmap)
   
        arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outfc,'#', '#', fieldmappings)

            
            

                           

