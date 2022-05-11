
## Loops through BAG stocks for each municipality (gemeente), spatial join with demolition scenarios, if BAG and demolition data overlaps, BAG building is assumed to be demolished. 

# 1. Import modules
import arcpy, arcinfo
import pandas as pd
import numpy as np
import glob, os

from arcpy import env
from arcpy.sa import *


#Enable ArcGIS extensions
arcpy.CheckOutExtension("Spatial")

arcpy.env.overwriteOutput = True


# Define workspace
workspace_sloop = r"C:/.../Input_SJ.gdb"
workspace_BAG = r"C:/.../Voorraden_BAG_gem.gdb"
workspace_out = r"C:/.../Output_SJ.gdb"

# Spatial join
gebouwtypen = ['vrijstaand', 'industrie', 'serieel', 'overheid', 'kantoor', 'appartement', 'winkel']
gebouwtypen_2 = ['losstaand', 'NijverheidEnLogistiek', 'rijtjeswoning', 'Overheid_kw_diensten', 'Kantoor', 'appartement', 'Detailhandel']

WLO = ['WLO_hoog_', 'WLO_laag_']
scenario = ['DichtBij', 'Ruim', 'Verbonden']

# Municipalities
gemeenten = ['Aa_en_Hunze_voorraden', 'Aalsmeer_voorraden', 'Aalten_voorraden', 'Achtkarspelen_voorraden', 'Alblasserdam_voorraden', 'Albrandswaard_voorraden', 'Alkmaar_voorraden', 'Almelo_voorraden', 'Almere_voorraden', 'Alphen_aan_den_Rijn_voorraden', 'Alphen_Chaam_voorraden', 'Altena_voorraden', 'Ameland_voorraden', 'Amersfoort_voorraden', 'Amstelveen_voorraden', 'Amsterdam_voorraden', 'Apeldoorn_voorraden', 'Appingedam_voorraden', 'Arnhem_voorraden', 'Assen_voorraden', 'Asten_voorraden', 'Baarle_Nassau_voorraden', 'Baarn_voorraden', 'Barendrecht_voorraden', 'Barneveld_voorraden', 'Beekdaelen_voorraden', 'Beek_voorraden', 'Beemster_voorraden', 'Beesel_voorraden', 'Berg_en_Dal_voorraden', 'Bergeijk_voorraden', 'Bergen_op_Zoom_voorraden', 'Bergen__L__voorraden', 'Bergen__NH__voorraden', 'Berkelland_voorraden', 'Bernheze_voorraden', 'Best_voorraden', 'Beuningen_voorraden', 'Beverwijk_voorraden', 'Bladel_voorraden', 'Blaricum_voorraden', 'Bloemendaal_voorraden', 'Bodegraven_Reeuwijk_voorraden', 'Boekel_voorraden', 'Borger_Odoorn_voorraden', 'Borne_voorraden', 'Borsele_voorraden', 'Boxmeer_voorraden', 'Boxtel_voorraden', 'Breda_voorraden', 'Brielle_voorraden', 'Bronckhorst_voorraden', 'Brummen_voorraden', 'Brunssum_voorraden', 'Bunnik_voorraden', 'Bunschoten_voorraden', 'Buren_voorraden', 'Capelle_aan_den_IJssel_voorraden', 'Castricum_voorraden', 'Coevorden_voorraden', 'Cranendonck_voorraden', 'Cuijk_voorraden', 'Culemborg_voorraden', 'Dalfsen_voorraden', 'Dantumadiel_voorraden', 'De_Bilt_voorraden', 'De_Fryske_Marren_voorraden', 'De_Ronde_Venen_voorraden', 'De_Wolden_voorraden', 'Delft_voorraden', 'Delfzijl_voorraden', 'Den_Helder_voorraden', 'Deurne_voorraden', 'Deventer_voorraden', 'Diemen_voorraden', 'Dinkelland_voorraden', 'Doesburg_voorraden', 'Doetinchem_voorraden', 'Dongen_voorraden', 'Dordrecht_voorraden', 'Drechterland_voorraden', 'Drimmelen_voorraden', 'Dronten_voorraden', 'Druten_voorraden', 'Duiven_voorraden', 'Echt_Susteren_voorraden', 'Edam_Volendam_voorraden', 'Ede_voorraden', 'Eemnes_voorraden', 'Eersel_voorraden', 'Eijsden_Margraten_voorraden', 'Eindhoven_voorraden', 'Elburg_voorraden', 'Emmen_voorraden', 'Enkhuizen_voorraden', 'Enschede_voorraden', 'Epe_voorraden', 'Ermelo_voorraden', 'Etten_Leur_voorraden', 'Geertruidenberg_voorraden', 'Geldrop_Mierlo_voorraden', 'Gemert_Bakel_voorraden', 'Gennep_voorraden', 'Gilze_en_Rijen_voorraden', 'Goeree_Overflakkee_voorraden', 'Goes_voorraden', 'Goirle_voorraden', 'Gooise_Meren_voorraden', 'Gorinchem_voorraden', 'Gouda_voorraden', 'Grave_voorraden', 'Groningen_voorraden', 'Gulpen_Wittem_voorraden', 'Haaksbergen_voorraden', 'Haaren_voorraden', 'Haarlemmermeer_voorraden', 'Haarlem_voorraden', 'Halderberge_voorraden', 'Hardenberg_voorraden', 'Harderwijk_voorraden', 'Hardinxveld_Giessendam_voorraden', 'Harlingen_voorraden', 'Hattem_voorraden', 'Heemskerk_voorraden', 'Heemstede_voorraden', 'Heerde_voorraden', 'Heerenveen_voorraden', 'Heerhugowaard_voorraden', 'Heerlen_voorraden', 'Heeze_Leende_voorraden', 'Heiloo_voorraden', 'Hellendoorn_voorraden', 'Hellevoetsluis_voorraden', 'Helmond_voorraden', 'Hendrik_Ido_Ambacht_voorraden', 'Hengelo_voorraden', 'Het_Hogeland_voorraden', 'Heumen_voorraden', 'Heusden_voorraden', 'Hillegom_voorraden', 'Hilvarenbeek_voorraden', 'Hilversum_voorraden', 'Hoeksche_Waard_voorraden', 'Hof_van_Twente_voorraden', 'Hollands_Kroon_voorraden', 'Hoogeveen_voorraden', 'Hoorn_voorraden', 'Horst_aan_de_Maas_voorraden', 'Houten_voorraden', 'Huizen_voorraden', 'Hulst_voorraden', 'IJsselstein_voorraden', 'Kaag_en_Braassem_voorraden', 'Kampen_voorraden', 'Kapelle_voorraden', 'Katwijk_voorraden', 'Kerkrade_voorraden', 'Koggenland_voorraden', 'Krimpen_aan_den_IJssel_voorraden', 'Krimpenerwaard_voorraden', 'Laarbeek_voorraden', 'Landerd_voorraden', 'Landgraaf_voorraden', 'Landsmeer_voorraden', 'Langedijk_voorraden', 'Lansingerland_voorraden', 'Laren_voorraden', 'Leeuwarden_voorraden', 'Leiden_voorraden', 'Leiderdorp_voorraden', 'Leidschendam_Voorburg_voorraden', 'Lelystad_voorraden', 'Leudal_voorraden', 'Leusden_voorraden', 'Lingewaard_voorraden', 'Lisse_voorraden', 'Lochem_voorraden', 'Loon_op_Zand_voorraden', 'Lopik_voorraden', 'Loppersum_voorraden', 'Losser_voorraden', 'Maasdriel_voorraden', 'Maasgouw_voorraden', 'Maassluis_voorraden', 'Maastricht_voorraden', 'Medemblik_voorraden', 'Meerssen_voorraden', 'Meierijstad_voorraden', 'Meppel_voorraden', 'Middelburg_voorraden', 'Midden_Delfland_voorraden', 'Midden_Drenthe_voorraden', 'Midden_Groningen_voorraden', 'Mill_en_Sint_Hubert_voorraden', 'Moerdijk_voorraden', 'Molenlanden_voorraden', 'Montferland_voorraden', 'Montfoort_voorraden', 'Mook_en_Middelaar_voorraden', 'Nederweert_voorraden', 'Neder_Betuwe_voorraden', 'Nieuwegein_voorraden', 'Nieuwkoop_voorraden', 'Nijkerk_voorraden', 'Nijmegen_voorraden', 'Nissewaard_voorraden', 'Noardeast_Fryslân_voorraden', 'Noordenveld_voorraden', 'Noordoostpolder_voorraden', 'Noordwijk_voorraden', 'Noord_Beveland_voorraden', 'Nuenen__Gerwen_en_Nederwetten_voorraden', 'Nunspeet_voorraden', 'Oegstgeest_voorraden', 'Oirschot_voorraden', 'Oisterwijk_voorraden', 'Oldambt_voorraden', 'Oldebroek_voorraden', 'Oldenzaal_voorraden', 'Olst_Wijhe_voorraden', 'Ommen_voorraden', 'Oost_Gelre_voorraden', 'Oosterhout_voorraden', 'Ooststellingwerf_voorraden', 'Oostzaan_voorraden', 'Opmeer_voorraden', 'Opsterland_voorraden', 'Oss_voorraden', 'Oude_IJsselstreek_voorraden', 'Ouder_Amstel_voorraden', 'Oudewater_voorraden', 'Overbetuwe_voorraden', 'Papendrecht_voorraden', 'Peel_en_Maas_voorraden', 'Pekela_voorraden', 'Pijnacker_Nootdorp_voorraden', 'Purmerend_voorraden', 'Putten_voorraden', 'Raalte_voorraden', 'Reimerswaal_voorraden', 'Renkum_voorraden', 'Renswoude_voorraden', 'Reusel_De_Mierden_voorraden', 'Rheden_voorraden', 'Rhenen_voorraden', 'Ridderkerk_voorraden', 'Rijssen_Holten_voorraden', 'Rijswijk_voorraden', 'Roerdalen_voorraden', 'Roermond_voorraden', 'Roosendaal_voorraden', 'Rotterdam_voorraden', 'Rozendaal_voorraden', 'Rucphen_voorraden', 'Schagen_voorraden', 'Scherpenzeel_voorraden', 'Schiedam_voorraden', 'Schiermonnikoog_voorraden', 'Schouwen_Duiveland_voorraden', 'Simpelveld_voorraden', 'Sint_Anthonis_voorraden', 'Sint_Michielsgestel_voorraden', 'Sittard_Geleen_voorraden', 'Sliedrecht_voorraden', 'Sluis_voorraden', 'Smallingerland_voorraden', 'Soest_voorraden', 'Someren_voorraden', 'Son_en_Breugel_voorraden', 'Stadskanaal_voorraden', 'Staphorst_voorraden', 'Stede_Broec_voorraden', 'Steenbergen_voorraden', 'Steenwijkerland_voorraden', 'Stein_voorraden', 'Stichtse_Vecht_voorraden', 'Súdwest_Fryslân_voorraden', 'Terneuzen_voorraden', 'Terschelling_voorraden', 'Texel_voorraden', 'Teylingen_voorraden', 'Tholen_voorraden', 'Tiel_voorraden', 'Tilburg_voorraden', 'Tubbergen_voorraden', 'Twenterand_voorraden', 'Tynaarlo_voorraden', 'Tytsjerksteradiel_voorraden', 'Uden_voorraden', 'Uitgeest_voorraden', 'Uithoorn_voorraden', 'Urk_voorraden', 'Utrechtse_Heuvelrug_voorraden', 'Utrecht_voorraden', 'Vaals_voorraden', 'Valkenburg_aan_de_Geul_voorraden', 'Valkenswaard_voorraden', 'Veendam_voorraden', 'Veenendaal_voorraden', 'Veere_voorraden', 'Veldhoven_voorraden', 'Velsen_voorraden', 'Venlo_voorraden', 'Venray_voorraden', 'Vijfheerenlanden_voorraden', 'Vlaardingen_voorraden', 'Vlieland_voorraden', 'Vlissingen_voorraden', 'Voerendaal_voorraden', 'Voorschoten_voorraden', 'Voorst_voorraden', 'Vught_voorraden', 'Waadhoeke_voorraden', 'Waalre_voorraden', 'Waalwijk_voorraden', 'Waddinxveen_voorraden', 'Wageningen_voorraden', 'Wassenaar_voorraden', 'Waterland_voorraden', 'Weert_voorraden', 'Weesp_voorraden', 'West_Betuwe_voorraden', 'West_Maas_en_Waal_voorraden', 'Westerkwartier_voorraden', 'Westerveld_voorraden', 'Westervoort_voorraden', 'Westerwolde_voorraden', 'Westland_voorraden', 'Weststellingwerf_voorraden', 'Westvoorne_voorraden', 'Wierden_voorraden', 'Wijchen_voorraden', 'Wijdemeren_voorraden', 'Wijk_bij_Duurstede_voorraden', 'Winterswijk_voorraden', 'Woensdrecht_voorraden', 'Woerden_voorraden', 'Wormerland_voorraden', 'Woudenberg_voorraden', 'Zaanstad_voorraden', 'Zaltbommel_voorraden', 'Zandvoort_voorraden', 'Zeewolde_voorraden', 'Zeist_voorraden', 'Zevenaar_voorraden', 'Zoetermeer_voorraden', 'Zoeterwoude_voorraden', 'Zuidplas_voorraden', 'Zundert_voorraden', 'Zutphen_voorraden', 'Zwartewaterland_voorraden', 'Zwijndrecht_voorraden', 'Zwolle_voorraden', '_s_Gravenhage_voorraden', '_s_Hertogenbosch_voorraden']


for gem in gemeenten:
    print(gem)
    for w in WLO:
        for s in scenario:
            
            joinFeatures = os.path.join(workspace_BAG, gem)

            targetFeatures = os.path.join(workspace_sloop, w+s)
            
            outfc = os.path.join(workspace_out, 'temp')

            # fieldmapping
            
            fieldmappings = arcpy.FieldMappings()
            fieldmappings.addTable(targetFeatures)
            fieldmappings.addTable(joinFeatures)
            # field: Class
            cl = fieldmappings.findFieldMapIndex("Class")
            fieldmap = fieldmappings.getFieldMap(cl)
            field = fieldmap.outputField
            fieldmap.mergeRule = "first"
            fieldmappings.replaceFieldMap(cl, fieldmap)
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
            x = fieldmappings.findFieldMapIndex("Woningtype")
            fieldmappings.removeFieldMap(x)

            y = fieldmappings.findFieldMapIndex("status")
            fieldmappings.removeFieldMap(y)

            z = fieldmappings.findFieldMapIndex("gebruiks_1")
            fieldmappings.removeFieldMap(z) 

            # spatial join

            arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outfc,'#', '#', fieldmappings)

            # delete rows 0 (gemeneenten buiten analyse)
            env.workspace = r"C:\.../Output_SJ.gdb"
            inp = 'temp'
            outp = w+s+'_Sloop_'+gem
            where_clause = "Staal>0\n"
            file3 = arcpy.Select_analysis(inp, outp, where_clause)

    print('done with '+gem)
            

