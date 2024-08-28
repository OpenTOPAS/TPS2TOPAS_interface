import pathlib

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def GetTsTimeFunctionParameters(parmName, times, values, unit):
    n = len(times)
    stimes = ' '.join('{:1.2f}'.format(t) for t in times)
    svalues = ' '.join('{:1.4f}'.format(v) for v in values)

    par1 = ('s:Tf/%s/Function = "Step"' % parmName)
    par2 = ('dv:Tf/%s/Times   = %d %s s' % (parmName, n, stimes)) 
    if unit != '':
        par3 = ('dv:Tf/%s/Values  = %d %s %s' % (parmName, n, svalues, unit))
    else:
        par3 = ('uv:Tf/%s/Values  = %d %s' % (parmName, n, svalues))
    return [par1, par2, par3]

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def SaveTsTimeFunctionParameters(parmName, times, values, unit, directory):
    n = len(times)
    stimes = ' '.join('{:1.2f}'.format(t) for t in times)
    svalues = ' '.join('{:1.3f}'.format(v) for v in values)
    if unit == 'u':
        if 'MUper' in parmName:
            svalues = ' '.join('{:1.4f}'.format(v) for v in values)
        else:
            svalues = ' '.join('{:1.5e}'.format(v) for v in values)
    if unit == 'i':
        svalues = ' '.join('{:d}'.format(v) for v in values)
    
    oFile = open('./%s/%s_TimeFeatures.txt' %(directory, parmName),'w')
    oFile.write('s:Tf/%s/Function = "Step"\n' % parmName)
    oFile.write('dv:Tf/%s/Times   = %d %s s\n' % (parmName, n, stimes)) 
    if unit != 'u' and unit != 'i':
        oFile.write('dv:Tf/%s/Values  = %d %s %s\n' % (parmName, n, svalues, unit))
    else: 
        oFile.write('%sv:Tf/%s/Values  = %d %s\n' % (unit,parmName, n, svalues))
    oFile.close()

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def WriteTimeFeaturesPCF(DATA,PLAN_DATA):
    directory = DATA["project_name"]
    # Saving data into OpenTOPAS PCF
    SaveTsTimeFunctionParameters('CollimatorAngles',\
                                 PLAN_DATA["TsStepTimes"],\
                                 PLAN_DATA["TsCollimatorAngles"], 'deg', directory)
    SaveTsTimeFunctionParameters('TableAngles',\
                                 PLAN_DATA["TsStepTimes"],\
                                 PLAN_DATA["TsTableAngles"], 'deg', directory)
    SaveTsTimeFunctionParameters('GantryAngles',\
                                 PLAN_DATA["TsStepTimes"],\
                                 PLAN_DATA["TsGantryAngles"], 'deg', directory)
    SaveTsTimeFunctionParameters('JawX1',\
                                 PLAN_DATA["TsStepTimes"],\
                                 PLAN_DATA["TsJawX1"], 'cm', directory)
    SaveTsTimeFunctionParameters('JawX2',\
                                 PLAN_DATA["TsStepTimes"],\
                                 PLAN_DATA["TsJawX2"], 'cm', directory)
    SaveTsTimeFunctionParameters('JawY1',\
                                 PLAN_DATA["TsStepTimes"],\
                                 PLAN_DATA["TsJawY1"], 'cm', directory)
    SaveTsTimeFunctionParameters('JawY2',\
                                 PLAN_DATA["TsStepTimes"],\
                                 PLAN_DATA["TsJawY2"], 'cm', directory)
    SaveTsTimeFunctionParameters('MUperSegment',\
                                 PLAN_DATA["TsStepTimes"],\
                                 PLAN_DATA["TsWeights"], 'u', directory)
    SaveTsTimeFunctionParameters('CalibrationFactor',\
                                 PLAN_DATA["TsStepTimes"],\
                                 PLAN_DATA["TsCalFactor"], 'u', directory)
    SaveTsTimeFunctionParameters('PrimariesPerSegment',\
                                 PLAN_DATA["TsStepTimes"],\
                                 PLAN_DATA["TsPrimaries"], 'i', directory)

    # Save MLC positions for each control point
    mlcAsingle = []  
    mlcBsingle = []
    oFile = open('./%s/MLC_TimeFeatures.txt' %directory,'w')
    for key in PLAN_DATA["TsMLCX1"]: 
        aName = 'MLCX1_' + str(key)
        aPars = GetTsTimeFunctionParameters(aName, PLAN_DATA["TsStepTimes"], PLAN_DATA["TsMLCX1"][key], 'cm')
        for apar in aPars:
            oFile.write(apar + '\n')
        oFile.write('\n')
    for key in PLAN_DATA["TsMLCX2"]: 
        aName = 'MLCX2_' + str(key)
        aPars = GetTsTimeFunctionParameters(aName, PLAN_DATA["TsStepTimes"], PLAN_DATA["TsMLCX2"][key], 'cm')
        for apar in aPars:
            oFile.write(apar + '\n')
        oFile.write('\n')
    oFile.close()
    
    # Save isocenter positions for each beam
    oFile = open('./%s/Isocenter_TimeFeatures.txt' %directory,'w')
    for key in PLAN_DATA["TsIsocenter"]: 
        aName = 'Iso' + str(key)
        aPars = GetTsTimeFunctionParameters(aName, PLAN_DATA["TsBeamTimes"], PLAN_DATA["TsIsocenter"][key], 'cm')
        for apar in aPars:
            oFile.write(apar + '\n')
        oFile.write('\n')
    oFile.close()

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def WritePlanParameterFile(DATA,CT_DATA,PLAN_DATA):
    directory = DATA["project_name"]
    # Setup and Time feature parameters 
    parFile = open('./%s/planParameters.txt'%(directory),'w')
    parFile.write('includeFile = CollimatorAngles_TimeFeatures.txt TableAngles_TimeFeatures.txt\n')
    parFile.write('includeFile = JawY1_TimeFeatures.txt JawY2_TimeFeatures.txt JawX1_TimeFeatures.txt JawX2_TimeFeatures.txt\n')
    parFile.write('includeFile = MLC_TimeFeatures.txt GantryAngles_TimeFeatures.txt\n')
    parFile.write('includeFile = MUperSegment_TimeFeatures.txt \n')
    parFile.write('includeFile = Isocenter_TimeFeatures.txt\n')
    parFile.write('includeFile = CalibrationFactor_TimeFeatures.txt\n')
    parFile.write('\n')
    parFile.write('s:RS/DicomDirectory = \"%s\"\n' % DATA["dicom_dirname"]) 
    parFile.write('s:RS/DicomDoseFileName = \"%s\"\n' % DATA["RD_filename"]) 
    parFile.write('d:Tf/VirtualSimulationTimeEnd = %1.2f s\n' % (PLAN_DATA["finalTime"]-1))
    parFile.write('i:Tf/VirtualSimulationNumberOfSequentialTimes = %d\n' % int(PLAN_DATA["finalTime"]-1))
    parFile.write('\n') 
    parFile.write('# Dicom center\n')
    parFile.write('d:Ge/cx = %1.4f cm\n' % CT_DATA["cx"])
    parFile.write('d:Ge/cy = %1.4f cm\n' % CT_DATA["cy"])
    parFile.write('d:Ge/cz = %1.4f cm\n' % CT_DATA["cz"])
    parFile.write('\n')
    parFile.write('# Isocenter\n')
    parFile.write('d:Ge/isox = Tf/IsoX/Value cm\n')
    parFile.write('d:Ge/isoy = Tf/IsoY/Value cm\n')
    parFile.write('d:Ge/isoz = Tf/IsoZ/Value cm\n') 
    parFile.write('\n')
    parFile.write('d:Ge/Gantry_Angle = Tf/GantryAngles/Value deg\n')
    parFile.write('d:Ge/Couch_Angle  = Tf/TableAngles/Value deg\n') 
    parFile.write('d:Ge/Collimator_Angle = Tf/CollimatorAngles/Value deg\n')
    parFile.write('u:So/calibrationFactorPerHistory = Tf/CalibrationFactor/Value * %1.5e \n' %(1/PLAN_DATA["phspChunk"]) )
    parFile.write('u:So/ScalingFactor = So/calibrationFactorPerHistory * Tf/MUperSegment/Value\n')
    parFile.write('\n')
    parFile.write('d:Ge/JawX1 = Tf/JawX1/Value cm\n')
    parFile.write('d:Ge/JawX2 = Tf/JawX2/Value cm\n')
    parFile.write('d:Ge/JawY1 = Tf/JawY1/Value cm\n')
    parFile.write('d:Ge/JawY2 = Tf/JawY2/Value cm\n')
    parFile.write('d:Ge/PhSpX1 = 0.75 * Tf/JawX1/Value cm\n')
    parFile.write('d:Ge/PhSpX2 = 0.75 * Tf/JawX2/Value cm\n')
    parFile.write('d:Ge/PhSpY1 = 0.75 * Tf/JawY1/Value cm\n')
    parFile.write('d:Ge/PhSpY2 = 0.75 * Tf/JawY2/Value cm\n')
    parFile.write('\n')
    parFile.write('\n')
    if DATA["MLC_model"] == "generic":
        parFile.write('dv:Ge/MLC/NegativeFieldSetting = 60 ')
        for i in range(1,60+1,1):
            parFile.write('Tf/MLCX1_%d/Value ' % i)
        parFile.write('cm\n')
        parFile.write('dv:Ge/MLC/PositiveFieldSetting = 60 ')
        for i in range(1,60+1,1):
            parFile.write('Tf/MLCX2_%d/Value ' % i)
        parFile.write('cm\n')
    if DATA["MLC_model"] == "VarianMillenium" or DATA["MLC_model"] == "VarianMilleniumHD":
        parFile.write('dv:Ge/MLC/NegativeFieldSetting = 60 ')
        for i in range(1,60+1,1):
            parFile.write('Tf/MLCX1_%d/Value ' % i)
        parFile.write('cm\n')
        parFile.write('dv:Ge/MLC/PositiveFieldSetting = 60 ')
        for i in range(1,60+1,1):
            parFile.write('Tf/MLCX2_%d/Value ' % i)
        parFile.write('cm\n')
    parFile.close()

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def WriteGeometryFile(DATA,ROI_DATA):
    directory = DATA["project_name"]  
    # Geometry
    parFile = open('./%s/Geometry.txt'%(directory),'w')
    parFile.write('#\n')
    parFile.write('includeFile = planParameters.txt HUtoMaterialSchneider.txt\n')
    parFile.write('\n')
    parFile.write('###################################################\n')
    parFile.write('#  Materials\n')
    parFile.write('####################################################\n')
    for name, material in ROI_DATA["materials"].items():
        if ' ' in name:
            name = name.replace(' ','_')
        if '.' in name:
            name = name.replace('.','_')
        n = len(material[0])
        parFile.write('sv:Ma/%s/Components = %d ' % (name, n))
        for i in range(n):
            parFile.write('"%s" ' % ROI_DATA["elements"][material[0][i]])
        parFile.write('\n')
    
        parFile.write('uv:Ma/%s/Fractions = %d ' % (name, n))
        for i in range(n):
            parFile.write('%f ' % material[1][i])
        parFile.write('\n')
    
        parFile.write('d:Ma/%s/Density = %f g/cm3\n' % (name, material[2]))
        parFile.write('d:Ma/%s/MeanExcitationEnergy = %f eV\n' % (name, material[3]))
    parFile.write('\n')
    parFile.write('###################################################\n')
    parFile.write('#  Patient in DICOM\n')
    parFile.write('####################################################\n')
    parFile.write('s:Ge/Patient/Parent   = "DICOM_to_IEC"\n')
    parFile.write('s:Ge/Patient/Type     = "TsDicomPatient"\n')
    parFile.write('s:Ge/Patient/Material = "G4_WATER"\n')
    parFile.write('d:Ge/Patient/RotX     = 0.0 deg\n')
    parFile.write('d:Ge/Patient/RotY     = 0.0 deg\n')
    parFile.write('d:Ge/Patient/RotZ     = 0.0 deg\n')
    parFile.write('d:Ge/Patient/TransX   = 0 cm  \n')
    parFile.write('d:Ge/Patient/TransY   = 0 cm \n')
    parFile.write('d:Ge/Patient/TransZ   = 0 cm \n')
    parFile.write('s:Ge/Patient/HUtoMaterialConversionMethod = "Schneider"\n')
    parFile.write('s:Ge/Patient/DicomDirectory      = RS/DicomDirectory \n')
    parFile.write('b:Ge/Patient/IgnoreInconsistentFrameOfReferenceUID = "True"\n')
    parFile.write('sv:Ge/Patient/DicomModalityTags = 1 "CT"\n')
    parFile.write('iv:Ge/Patient/ShowSpecificSlicesZ = 1 33 \n')
    parFile.write('s:Ge/Patient/CloneRTDoseGridFrom = RS/DicomDoseFileName \n')
    if len(ROI_DATA["roiWithMaterials"]) > 0:
        parFile.write('sv:Ge/Patient/MaterialByRTStructNames = %d ' %  len(ROI_DATA["roiWithMaterials"]))
        for roi, name in ROI_DATA["roiWithMaterials"].items(): 
            parFile.write('"'+roi+'" ')
        parFile.write('\n')
        parFile.write('sv:Ge/Patient/MaterialByRTStructMaterials = %d ' % len(ROI_DATA["roiWithMaterials"])) 
        for roi, name in ROI_DATA["roiWithMaterials"].items():
            if ' ' in name:
                name = name.replace(' ','_')
            if '.' in name:
                name = name.replace('.','_')
            parFile.write('"'+name+'" ')
        parFile.write('\n')
      
    # Global control parameter files
    parFile.write('\n')
    parFile.write('###################################################\n')
    parFile.write('#  Jaws \n')
    parFile.write('####################################################\n')
    parFile.write('s:Ge/JawPos/Parent = "IEC_B"\n')
    parFile.write('s:Ge/JawPos/Type = "Group"\n')
    parFile.write('#d:Ge/JawPos/RotZ = -1 * Ge/Collimator_Angle deg\n')
    parFile.write('\n')
    parFile.write('dc:Ge/JawX/PositiveFieldSetting  = Ge/JawX2 cm \n')
    parFile.write('dc:Ge/JawX/NegativeFieldSetting  = +1 * Ge/JawX1 cm \n')
    parFile.write('s:Ge/JawX/Parent         = "JawPos" #IEC_B"\n')
    parFile.write('s:Ge/JawX/Type           = "TsJaws"\n')
    parFile.write('s:Ge/JawX/Material       = "G4_W"\n')
    parFile.write('s:Ge/JawX/Color          = "red"\n')
    parFile.write('s:Ge/JawX/DrawingStyle   = "Solid"\n')
    parFile.write('d:Ge/JawX/LX             = 13.462 cm \n')
    parFile.write('d:Ge/JawX/LY             = 21.844 cm \n')
    parFile.write('d:Ge/JawX/LZ             = 7.77 cm \n')
    parFile.write('dc:Ge/JawX/SourceToUpstreamSurfaceDistance = 27.89 cm \n')
    parFile.write('d:Ge/JawX/SAD            = 100 cm \n')
    parFile.write('d:Ge/JawX/DistSourceToSAD = Ge/JawX/SAD - Ge/JawX/SourceToUpstreamSurfaceDistance cm\n')
    parFile.write('d:Ge/JawX/HalfThickness = 0.5 * Ge/JawX/LZ cm\n')
    parFile.write('d:Ge/JawX/TransZ = Ge/JawX/DistSourceToSAD - Ge/JawX/HalfThickness cm\n')
    parFile.write('d:Ge/JawX/TravelAxisX = 0. deg \n')
    parFile.write('d:Ge/JawX/TravelAxisY = 90. deg \n')
    parFile.write('d:Ge/JawX/RotZ = Ge/JawX/TravelAxisX deg \n')
    parFile.write('s:Ge/JawX/AssignToRegionNamed = "jaws"\n')
    parFile.write('\n')
    parFile.write('dc:Ge/JawY/PositiveFieldSetting  = Ge/JawY2 cm \n')
    parFile.write('dc:Ge/JawY/NegativeFieldSetting  = +1 * Ge/JawY1 cm \n')
    parFile.write('s:Ge/JawY/Parent         = "JawPos" #IEC_B"\n')
    parFile.write('s:Ge/JawY/Type           = "TsJaws"\n')
    parFile.write('s:Ge/JawY/Material       = "G4_W"\n')
    parFile.write('s:Ge/JawY/Color          = "blue"\n')
    parFile.write('s:Ge/JawY/DrawingStyle   = "Solid"\n')
    parFile.write('d:Ge/JawY/LX             = 11.937 cm \n')
    parFile.write('d:Ge/JawY/LY             = 18.796 cm \n')
    parFile.write('d:Ge/JawY/LZ             = 7.77 cm \n')
    parFile.write('dc:Ge/JawY/SourceToUpstreamSurfaceDistance = 36.61 cm \n')
    parFile.write('d:Ge/JawY/SAD            = 100 cm \n')
    parFile.write('d:Ge/JawY/DistSourceToSAD = Ge/JawY/SAD - Ge/JawY/SourceToUpstreamSurfaceDistance cm\n')
    parFile.write('d:Ge/JawY/HalfThickness = 0.5 * Ge/JawY/LZ cm\n')
    parFile.write('d:Ge/JawY/TransZ = Ge/JawY/DistSourceToSAD - Ge/JawY/HalfThickness cm\n')
    parFile.write('d:Ge/JawY/TravelAxisX = 0. deg \n')
    parFile.write('d:Ge/JawY/TravelAxisY = -90. deg  ### CHANGED FROM +90deg\n')
    parFile.write('d:Ge/JawY/RotZ = Ge/JawY/TravelAxisY deg \n')
    parFile.write('s:Ge/JawY/AssignToRegionNamed = "jaws"\n')
    parFile.write('\n')
    parFile.write('###################################################\n')
    parFile.write('#  Base plate below the jaws \n')
    parFile.write('####################################################\n')
    parFile.write('s:Ge/BasePlate/Parent    = "IEC_B"\n')
    parFile.write('s:Ge/BasePlate/Type      = "TsCylinder"\n')
    parFile.write('s:Ge/BasePlate/Material  = "Steel"\n')
    parFile.write('s:Ge/BasePlate/Color     = "yellow" \n')
    parFile.write('d:Ge/BasePlate/RMax      = 30.226 cm \n')
    parFile.write('d:Ge/BasePlate/RMin      = 11.557 cm \n')
    parFile.write('d:Ge/BasePlate/HL        = 0.762 cm\n')
    parFile.write('d:Ge/BasePlate/TransZ    = 54.062 cm\n')
    parFile.write('s:Ge/BasePlate/DrawingStyle = "Solid"\n')
    parFile.write('\n')
    parFile.write('###################################################\n')
    parFile.write('#  MLCs \n')
    parFile.write('####################################################\n')
    parFile.write('s:Ge/MLCPos/Parent = "IEC_B"\n')
    parFile.write('s:Ge/MLCPos/Type   = "Group"\n')
    if DATA["MLC_model"] == "VarianMillenium" or DATA["MLC_model"] == "VarianMilleniumHD":
        parFile.write('d:Ge/MLCPos/TransZ = 49.02 cm\n')
    parFile.write('\n')
    generic_thickness   = 5.61 # cm
    generic_distToIso   = 49.02
    generic_SAD         = 100.0
    generic_SUSD        = generic_SAD - generic_distToIso - generic_thickness*0.5
    if DATA["MLC_model"] == "generic":
        parFile.write('s:Ge/MLC/Type = "TsDivergingMLC"\n')
        parFile.write('s:Ge/MLC/Parent = "MLCPos"\n')
        parFile.write('s:Ge/MLC/Material = "G4_W"\n')
        parFile.write('s:Ge/MLC/Color    = "gray"\n')
        parFile.write('s:Ge/MLC/DrawingStyle = "Solid"\n')
        parFile.write('d:Ge/MLC/SAD = %s cm\n' %generic_SAD)
        parFile.write('d:Ge/MLC/SourceToUpstreamSurfaceDistance = %s cm\n' %generic_SUSD)
        parFile.write('d:Ge/MLC/DistSourceToSAD = Ge/MLC/SAD - Ge/MLC/SourceToUpstreamSurfaceDistance cm\n')
        parFile.write('d:Ge/MLC/Thickness = %s cm\n' %generic_thickness) 
        parFile.write('d:Ge/MLC/HalfThickness = 0.5 * Ge/MLC/Thickness cm\n')
        parFile.write('d:Ge/MLC/MaxLeafOpen = 20 cm\n')
        parFile.write('d:Ge/MLC/Length = 19 cm\n')
        parFile.write('s:Ge/MLC/LeafTravelAxis = "Xb"\n')
        parFile.write('dv:Ge/MLC/LeafWidths = 60 ')
        for leaf_pair in range(60):
            leaf_pair += 1
            if leaf_pair > 10 and leaf_pair < 51: # 14 and 47 to reproduce HD120
                parFile.write('5.0 ') # 2.5 to reproduce HD120
            else:
                parFile.write('10.0 ') # 5 to reproduce HD120              
        parFile.write('mm\n')
        parFile.write('d:Ge/MLC/TransZ = Ge/MLC/DistSourceToSAD - Ge/MLC/HalfThickness cm\n')
        parFile.write('#d:Ge/MLCPos/RotZ = -1 * Ge/Collimator_Angle deg\n')
        parFile.write('\n')
    if DATA["MLC_model"] == "VarianMillenium" or DATA["MLC_model"] == "VarianMilleniumHD":
        parFile.write('s:Ge/MLC/Type = "TsTrueBeamMLC"\n')
        if DATA["MLC_model"] == "VarianMillenium":
            parFile.write('s:Ge/MLC/MLCModel = "NDS120"\n')
        if DATA["MLC_model"] == "VarianMilleniumHD":
            parFile.write('s:Ge/MLC/MLCModel = "NDS120HD"\n')
        parFile.write('s:Ge/MLC/Parent = "MLCPos"\n')
        parFile.write('s:Ge/MLC/Material = "G4_W"\n')
        parFile.write('s:Ge/MLC/Color    = "gray"\n')
        parFile.write('s:Ge/MLC/DrawingStyle = "Solid"\n')
        parFile.write('d:Ge/MLC/MinLeafAperture = 0.05 cm\n')
        parFile.write('d:Ge/MLC/MaxLeafAperture = 20 cm\n')
        parFile.write('b:Ge/MLC/CheckForOverlapsBetweenLeafs = "false"\n')
        parFile.write('#d:Ge/MLC/RotZ = -1 * Ge/Collimator_Angle deg\n')
        parFile.write('\n')
    parFile.write('###################################################\n')
    parFile.write('#  Mylar window at treatment head exit\n')
    parFile.write('####################################################\n')
    parFile.write('s:Ge/Tray/Parent    = "IEC_B"\n')
    parFile.write('s:Ge/Tray/Type      = "TsBox"\n')
    parFile.write('s:Ge/Tray/Material  = "Mylar"\n')
    parFile.write('s:Ge/Tray/Color     = "green"\n')
    parFile.write('d:Ge/Tray/HLX       = 15 cm\n')
    parFile.write('d:Ge/Tray/HLY       = 15 cm\n')
    parFile.write('d:Ge/Tray/HLZ       = 0.00508 cm\n')
    parFile.write('d:Ge/Tray/TransZ    = 44.3 cm\n')
    parFile.write('\n')
    parFile.write('\n')
    # parallel volumes to prevent overlapping
    parFile.write('b:Ge/Tray/IsParallel = "True"\n')
    parFile.write('b:Ge/MLC/IsParallel = "True"\n')
    parFile.write('\n')
    parFile.close()
    
def WriteMainWithVisualizationFile(DATA):
    directory = DATA["project_name"]

    # Visualization
    parFile = open('./%s/Main_with_Visualization.txt'%(directory),'w')
    parFile.write('###################################################\n')
    parFile.write('# Get the main file\n')
    parFile.write('####################################################\n')
    parFile.write('includeFile = Main.txt\n')
    parFile.write('\n')
    parFile.write('###################################################\n')
    parFile.write('# Visualization\n')
    parFile.write('####################################################\n')
    parFile.write('b:Ts/UseQt = "True"\n')
    parFile.write('s:Gr/ViewA/Type        = "OpenGL"\n')
    parFile.write('i:Gr/ViewA/WindowSizeX = 900\n')
    parFile.write('i:Gr/ViewA/WindowSizeY = 900\n')
    parFile.write('d:Gr/ViewA/Theta          = 89.9 deg\n')
    parFile.write('d:Gr/ViewA/Phi            = -90 deg\n')
    parFile.write('b:Gr/ViewA/IncludeAxes    = "true"\n')
    parFile.write('d:Gr/ViewA/AxesSize       = 100 cm \n')
    parFile.write('u:Gr/ViewA/Zoom           = 1.\n')
    parFile.write('i:Gr/ShowOnlyOutlineIfVoxelCountExceeds = 100000000\n')
    parFile.write('\n')
    parFile.write('# Select a specific dicom slice to show\n')
    parFile.write('#iv:Ge/Patient/ShowSpecificSlicesX = 1 -1\n')
    parFile.write('#iv:Ge/Patient/ShowSpecificSlicesY = 1 -1\n')
    parFile.write('iv:Ge/Patient/ShowSpecificSlicesZ = 1 -1\n')
    parFile.write('\n')
    parFile.write('# comment the follow line in Geometry.txt to avoid displaying the RT Dose Grid\n')
    parFile.write('#s:Ge/Patient/CloneRTDoseGridFrom = RS/DicomDoseFileName \n')
    parFile.close()

def WriteMainFile(DATA,PLAN_DATA):
    directory = DATA["project_name"]

    # Main PCF
    parFile = open('./%s/Main.txt'%(directory),'w')
    parFile.write('##################################################\n')
    parFile.write('includeFile = planParameters.txt Geometry.txt PrimariesPerSegment_TimeFeatures.txt\n')
    parFile.write('sv:Ph/Default/Modules = 1 "g4em-standard_opt4"\n')
    parFile.write('d:Ph/Default/LowestElectronEnergy = 189 keV\n')
    parFile.write('d:Ph/Default/ForRegion/jaws/CutForGamma = 1 mm\n')
    parFile.write('d:Ph/Default/ForRegion/jaws/CutForElectron = 0.3 mm\n')
    parFile.write('\n')
    parFile.write('sv:Ph/Default/LayeredMassGeometryWorlds = 2 "MLC" "Tray"\n')
    parFile.write('\n')
    parFile.write('s:Ge/World/Material         = "Air"\n')
    parFile.write('d:Ge/World/HLX              = 1.5 m\n')
    parFile.write('d:Ge/World/HLY              = 1.5 m\n')
    parFile.write('d:Ge/World/HLZ              = 1.5 m\n')
    parFile.write('b:Ge/World/Invisible        = "True"\n')
    parFile.write('\n')
    parFile.write('# Fixed system IEC_F, parent Geant4 world - e.g. Xf; (Xf,Yf,Zf) is world (X,Y,Z)^M\n')
    parFile.write('s:Ge/IEC_F/Parent           = "World"\n')
    parFile.write('s:Ge/IEC_F/Type             = "Group"\n')
    parFile.write('d:Ge/IEC_F/RotZ             = +1 * Ge/Collimator_Angle deg\n')
    parFile.write('\n')
    parFile.write('s:Ge/IEC_W/Parent           = "World"\n')
    parFile.write('s:Ge/IEC_W/Type             = "Group"\n')
    parFile.write('\n')
    parFile.write('# Gantry system IEC_G, parent IEC_F - e.g. Xg; Gantry rotates about Yg by IEC_G/RotY^M\n')
    parFile.write('# Gantry rotation, if any, is applied in the includeFile (see above)^M\n')
    parFile.write('s:Ge/IEC_G/Parent           = "IEC_F"\n')
    parFile.write('s:Ge/IEC_G/Type             = "Group"\n')
    parFile.write('dc:Ge/IEC_G/RotY_S          = Ge/Gantry_Angle deg \n')
    parFile.write('#d:Ge/IEC_G/RotY             = -1 * Ge/IEC_G/RotY_S deg\n')
    parFile.write('d:Ge/IEC_G/RotY             = +1 * Ge/IEC_G/RotY_S deg # to rotate the patient instead\n')
    parFile.write('\n')
    parFile.write('# Beam limiting system IEC_B, parent IEC_G - e.g. Xb; Collimator rotates about Zb by IEC_B/RotZ^M\n')
    parFile.write('# Collimator rotation, if any, is applied in the includeFile (see above)^M\n')
    parFile.write('s:Ge/IEC_B/Parent           = "IEC_W" # "IEC_G" to rotate the patient\n')
    parFile.write('s:Ge/IEC_B/Type             = "Group"\n')
    parFile.write('\n')
    parFile.write('# Patient support system (couch) IEC_S, parent IEC_F - couch rotates by RotZs^M\n')
    parFile.write('# Couch rotation, if any, is applied in the includeFile (see above)^M\n')
    parFile.write('s:Ge/IEC_S/Parent           = "IEC_G" # "IEC_F" to rotate patient instead\n')
    parFile.write('s:Ge/IEC_S/Type             = "Group"\n')
    parFile.write('d:Ge/IEC_S/TransX           = -1 * Ge/Isox cm \n')
    parFile.write('d:Ge/IEC_S/TransY           = -1 * Ge/Isoz cm \n')
    parFile.write('d:Ge/IEC_S/TransZ           = +1 * Ge/Isoy cm \n')
    parFile.write('dc:Ge/IEC_S/RotZ_S          = Ge/Couch_Angle deg \n')
    parFile.write('d:Ge/IEC_S/RotZ             = -1 * Ge/IEC_S/RotZ_S deg\n')
    parFile.write('\n')
    parFile.write('s:Ge/DICOM_to_IEC/Type   = "Group"\n')
    parFile.write('s:Ge/DICOM_to_IEC/Parent = "IEC_S"\n')
    parFile.write('d:Ge/DICOM_to_IEC/TransX = Ge/cx cm \n')
    parFile.write('d:Ge/DICOM_to_IEC/TransY = Ge/cz cm \n')
    parFile.write('d:Ge/DICOM_to_IEC/TransZ = -1 * Ge/cy cm # Swap Y <-> Z and invert the sigh\n')
    parFile.write('d:Ge/DICOM_to_IEC/RotX   = 90.0 deg # This rotation brings back Z <-> Y\n')
    parFile.write('\n')
    if DATA["multipleUse"] > 1:
        parFile.write('#########################\n')
        parFile.write('# Geometry for vrt\n')
        parFile.write('#########################\n')
        parFile.write('s:Ge/VrtParallelWorld/Type       = "TsBox"\n')
        parFile.write('s:Ge/VrtParallelWorld/Parent     = "World"\n')
        parFile.write('d:Ge/VrtParallelWorld/HLX        = 35 cm\n')
        parFile.write('d:Ge/VrtParallelWorld/HLY        = 35 cm\n')
        parFile.write('d:Ge/VrtParallelWorld/HLZ        = 80 cm\n')
        parFile.write('s:Ge/VrtParallelWorld/Color      = "grass"\n')
        parFile.write('b:Ge/VrtParallelWorld/IsParallel = "true"\n')
        parFile.write('\n')
        parFile.write('s:Ge/subComponent1/Parent = "VrtParallelWorld"\n')
        parFile.write('s:Ge/subComponent1/Type = "TsBox"\n')
        parFile.write('s:Ge/subComponent1/Color = "blue"\n')
        parFile.write('b:Ge/subComponent1/IsParallel = "True"\n')
        parFile.write('d:Ge/subComponent1/HLX = 35 cm\n')
        parFile.write('d:Ge/subComponent1/HLY = 35 cm\n')
        parFile.write('d:Ge/subComponent1/HLZ = 45 cm\n')
        parFile.write('\n')
        parFile.write('##########################\n')
        parFile.write('# Variance reduction\n')
        parFile.write('##########################\n')
        parFile.write('b:Vr/UseVarianceReduction                    = "true"\n')
        parFile.write('b:Vr/ParticleSplit/Active                    = "true"\n')
        parFile.write('sv:Vr/ParticleSplit/ParticleName             = 3 "gamma" "e-" "e+"\n')
        parFile.write('s:Vr/ParticleSplit/Component                 = "VrtParallelWorld"\n')
        parFile.write('sv:Vr/ParticleSplit/SubComponents            = 1 "subComponent1"\n')
        parFile.write('s:Vr/ParticleSplit/Type                      = "GeometricalParticleSplit"\n')
        parFile.write('iv:Vr/ParticleSplit/SplitNumber              = 1 %d\n' % DATA["multipleUse"])
        parFile.write('bv:Vr/ParticleSplit/Symmetric                = 1 "false"\n')
        parFile.write('d:Vr/ParticleSplit/RussianRoulette/ROIRadius = 60 cm\n')
        parFile.write('d:Vr/ParticleSplit/RussianRoulette/ROITrans  = 2 cm\n')
        parFile.write('bv:Vr/ParticleSplit/RussianRoulette          = 1 "false"\n')
        parFile.write('s:Vr/ParticleSplit/SplitAxis                 = "zaxis"\n')
        parFile.write('\n')    
    parFile.write('####################################################\n')
    parFile.write('# Beam is at Gantry coordination\n')
    parFile.write('####################################################\n')
    parFile.write('s:Ge/BeamPosition/Parent = "IEC_F" # "IEC_G" to rotate the patient instead\n')
    parFile.write('d:Ge/BeamPosition/RotX =  180 deg\n')
    parFile.write('d:Ge/BeamPosition/TransZ = 100 cm \n')
    parFile.write('\n')
    parFile.write('s:Ge/source/Type = "Group" \n')
    parFile.write('s:Ge/source/Parent = "BeamPosition"\n')
    parFile.write('d:Ge/source/TransZ = 26.7 cm #for TrueBeam phaseSpaceFile\n')
    parFile.write('\n')
    parFile.write('s:So/phsp/Type = "PhaseSpace"\n')
    parFile.write('s:So/phsp/Component = "source"\n')
    parFile.write('s:So/phsp/PhaseSpaceFileName = "%s"\n' % DATA["phsp_filename"])
    parFile.write('b:So/phsp/PhaseSpacePrecheck = "F"\n')
    parFile.write('i:So/phsp/PhaseSpaceMultipleUse = 0\n')
    parFile.write('i:So/phsp/NumberOfHistoriesInRun = Tf/PrimariesPerSegment/Value #10 * Ts/ShowHistoryCountAtInterval\n') 
    parFile.write('b:So/phsp/LimitedAssumeFirstParticleIsNewHistory = "True" #if IAEA phsp\n') 
    parFile.write('b:So/phsp/LimitedAssumePhotonIsNewHistory = "True" #if IAEA phsp\n') 
    parFile.write('\n')
    parFile.write('s:Sc/Dose/Quantity = "%s" \n' % (DATA["scoring_quantity"]))
    parFile.write('u:Sc/Dose/OutputWeightingFactor = So/ScalingFactor\n')
    parFile.write('b:Sc/Dose/PreCalculateStoppingPowerRatios = "True"\n')
    parFile.write('s:Sc/Dose/Component = "Patient/RTDoseGrid" \n')
    parFile.write('s:Sc/Dose/IfOutputfileAlreadyExists = "Overwrite"\n')
    parFile.write('s:Sc/Dose/OutputType = "%s" \n' % DATA["output_format"])
    parFile.write('s:Sc/Dose/OutputFile = "./output/%s" \n' % (DATA["output_file"]))
    parFile.write('\n')
    parFile.write('d:Tf/TimeLineEnd = Tf/VirtualSimulationTimeEnd s\n')
    parFile.write('i:Tf/NumberOfSequentialTimes = Tf/VirtualSimulationNumberOfSequentialTimes\n')
    parFile.write('i:Ts/Seed = 1\n')
    parFile.write('i:Ts/NumberOfThreads = 0\n')
    parFile.write('b:Ts/ShowCPUTime = "True"\n')
    countAtInterval = int(PLAN_DATA["phspChunk"]/10)
    parFile.write('i:Ts/ShowHistoryCountAtInterval = %d \n' % countAtInterval)
    parFile.write('i:Ts/ParameterizationErrorMaxCount = 1000000000\n')
    parFile.write('i:Ts/ParameterizationErrorMaxReports = 10\n')
    parFile.write('\n')
    