from constants import CONSTANTS
from BSF import *
import os
import pydicom
import numpy as np

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def RetrieveCTData(DATA):

    #global cx, cy, cz

    CTfiles = [x for x in os.listdir(DATA["dicom_dirname"]) if x.startswith('CT')]

    ds_CT = pydicom.dcmread(DATA["dicom_dirname"] + "/" + CTfiles[0])

    originx = ds_CT.ImagePositionPatient[0] # center of the first voxel
    originy = ds_CT.ImagePositionPatient[1]
    slicelocation = []
    for f in CTfiles:
        ds = pydicom.dcmread(DATA["dicom_dirname"] + "/" + f)
        slicelocation.append(ds.SliceLocation)
    slicelocation.sort()
    originz = slicelocation[0]    
    
    spacingx = ds_CT.PixelSpacing[0]
    spacingy = ds_CT.PixelSpacing[1]
    spacingz = ds_CT.SliceThickness
    
    dimx = ds_CT.Columns*spacingx 
    dimy = ds_CT.Rows*spacingy
    #dimz = len(CTfiles)*spacingz # find a better way(?)
    dimz = (slicelocation[-1] + spacingz/2) - (slicelocation[0] - spacingz/2)
    
    cx = (originx + 0.5*dimx - spacingx/2) / 10 # in cm
    cy = (originy + 0.5*dimy - spacingy/2) / 10 # in cm
    cz = (originz + 0.5*dimz - spacingz/2) / 10 # in cm

    CT_DATA = {}

    CT_DATA["cx"] = cx
    CT_DATA["cy"] = cy
    CT_DATA["cz"] = cz

    return CT_DATA

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def RetrieveROIData(DATA):
    ds_RS = pydicom.dcmread(DATA["RS_filename"])

    # Check for ROIs with materials. If there's any
    # a material is created in TOPAS and assigned to 
    # the corresponding structure.
    predefinedTOPASmaterials = ["Vacuum","Carbon","Aluminum","Nickel","Copper","Iron","Tantalum","Lead","Air","Brass","Lexan","Lucite","Mylar","Mylon","Kapton","Water_75eV","Titanium","Steel"]
    elements = {
    1: "Hydrogen", 2: "Helium", 3: "Lithium", 4: "Beryllium", 5: "Boron",
    6: "Carbon", 7: "Nitrogen", 8: "Oxygen", 9: "Fluorine", 10: "Neon",
    11: "Sodium", 12: "Magnesium", 13: "Aluminum", 14: "Silicon", 
    15: "Phosphorus", 16: "Sulfur", 17: "Chlorine", 18: "Argon", 
    19: "Potassium", 20: "Calcium", 21: "Scandium", 22: "Titanium", 
    23: "Vanadium", 24: "Chromium", 25: "Manganese", 26: "Iron", 
    27: "Cobalt", 28: "Nickel", 29: "Copper", 30: "Zinc", 31: "Gallium", 
    32: "Germanium", 33: "Arsenic", 34: "Selenium", 35: "Bromine", 
    36: "Krypton", 37: "Rubidium", 38: "Strontium", 39: "Yttrium", 
    40: "Zirconium", 41: "Niobium", 42: "Molybdenum", 43: "Technetium", 
    44: "Ruthenium", 45: "Rhodium", 46: "Palladium", 47: "Silver", 
    48: "Cadmium", 49: "Indium", 50: "Tin", 51: "Antimony", 52: "Tellurium", 
    53: "Iodine", 54: "Xenon", 55: "Cesium", 56: "Barium", 57: "Lanthanum", 
    58: "Cerium", 59: "Praseodymium", 60: "Neodymium", 61: "Promethium", 
    62: "Samarium", 63: "Europium", 64: "Gadolinium", 65: "Terbium", 
    66: "Dysprosium", 67: "Holmium", 68: "Erbium", 69: "Thulium", 
    70: "Ytterbium", 71: "Lutetium", 72: "Hafnium", 73: "Tantalum", 
    74: "Tungsten", 75: "Rhenium", 76: "Osmium", 77: "Iridium", 
    78: "Platinum", 79: "Gold", 80: "Mercury", 81: "Thallium", 
    82: "Lead", 83: "Bismuth", 84: "Polonium", 85: "Astatine", 
    86: "Radon", 87: "Francium", 88: "Radium", 89: "Actinium", 
    90: "Thorium", 91: "Protactinium", 92: "Uranium", 93: "Neptunium", 
    94: "Plutonium", 95: "Americium", 96: "Curium", 97: "Berkelium", 
    98: "Californium", 99: "Einsteinium", 100: "Fermium", 101: "Mendelevium", 
    102: "Nobelium", 103: "Lawrencium", 104: "Rutherfordium", 105: "Dubnium", 
    106: "Seaborgium", 107: "Bohrium", 108: "Hassium", 109: "Meitnerium", 
    110: "Darmstadtium", 111: "Roentgenium", 112: "Ununbiium"}
    
    RoiGeometries = ds_RS.RTROIObservationsSequence
    roiWithMaterials = {} 
    materials = {}
    warnings = 0
    for roi in RoiGeometries:
        skip = False
        if "MaterialID" in roi:
            materialName = roi.MaterialID
            defined_material = False
            for key in elements:
                if materialName == elements[key]:
                    defined_material = True
                    break
            for region in ds_RS.StructureSetROISequence:
                if region.ROINumber == roi.ReferencedROINumber:
                    roiName = region.ROIName
                    if len(roiName) > 16:
                        print("--- WARNING: ROI called %s not considered since its name is too long and the DICOM observation label and ROI name do not match. Then, TOPAS cannot assign the materials to regions correctly. Please shorten the name in your TPS."%roiName)
                        skip = True
                        warnings += 1
                    for letter in range(len(roiName)):
                        if roiName[letter] == ' ':
                            print("--- WARNING: ROI called %s not considered since TOPAS cannot handle structure names with spaces in it. Please change the ROI name in your TPS."%roiName)
                            skip = True
                            warnings += 1
            if skip == True:
                continue
            structName = ds_RS.StructureSetROISequence
            
            if materialName in predefinedTOPASmaterials: 
                materialName = materialName + "2"
                print("--- WARNING: The material %s is already defined in TOPAS - material name set to %s" %(materialName[:-1],materialName))
    
            if materialName[0:1] == "G4": 
                print("--- WARNING: The material %s was not included in the parameter files. The prefix 'G4' is reserved in TOPAS for materials from the pre-defined NIST database. Please change the name of the material in your TPS")
            
            roiWithMaterials[roi.ROIObservationLabel] = materialName
            
            if (not materialName in materials) and (defined_material == False):
                elemental_composition = []
                elemental_weight = []
                for item in roi.ROIPhysicalPropertiesSequence:
                    if item.ROIPhysicalProperty == "ELEM_FRACTION":
                        for element in item.ROIElementalCompositionSequence:
                            elemental_composition.append(element.ROIElementalCompositionAtomicNumber)
                            elemental_weight.append(element[0x3006,0xb8].value)
                    if item.ROIPhysicalProperty == "REL_MASS_DENSITY":
                        material_density = item.ROIPhysicalPropertyValue
                    if item.ROIPhysicalProperty == "MEAN_EXCI_ENERGY":
                        material_I = item.ROIPhysicalPropertyValue
                materials[materialName] = (elemental_composition,\
                                           elemental_weight,\
                                           material_density,\
                                           material_I)
    
    ROI_DATA = {}

    ROI_DATA["materials"] = materials
    ROI_DATA["elements"] = elements
    ROI_DATA["roiWithMaterials"] = roiWithMaterials

    return ROI_DATA
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def RetrievePlanData(DATA):

    ds_RP = pydicom.dcmread(DATA["RP_filename"])

    # Lists containing parameters for each control point
    TsBeamNames = [] 
    TsStepTimes = [] 
    TsBeamTimes = [] 
    TsIsocenter = {} ; TsIsocenter["X"] = [] ; TsIsocenter["Y"] = [] ; TsIsocenter["Z"] = []
    TsGantryAngles = [] 
    TsCollimatorAngles = [] 
    TsTableAngles = [] 
    TsJawX1 = [] 
    TsJawX2 = [] 
    TsJawY1 = [] 
    TsJawY2 = [] 
    TsWeights = []
    TsCalFactor = []
    TsPrimaries = []
    TsMLCX1 = {}
    TsMLCX2 = {}
    MLCX1 = {}
    MLCX2 = {}

    ### Beam sequence ### 
    reference_beam_set = ds_RP.FractionGroupSequence[0].ReferencedBeamSequence  # contains dose, meterset (MU) ...
    beam_set = ds_RP.BeamSequence   # contains control points
    number_of_beams = len(reference_beam_set)
    
    # Retrieving the control parameters per beam
    dt = 1.0
    for ref_beam,beam in zip(reference_beam_set, beam_set):
        
        if "BeamMeterset" in ref_beam:
            beamEnergy = float(beam_set[0].ControlPointSequence[0].NominalBeamEnergy)
            BeamMU = ref_beam.BeamMeterset
            RotDirection = beam.ControlPointSequence[0].GantryRotationDirection # e.g., CW // assumes one per beam - if not add to control point loop
            Technique = beam.BeamType
            IsoX = beam.ControlPointSequence[0].IsocenterPosition[0]/10 # in cm
            IsoY = beam.ControlPointSequence[0].IsocenterPosition[1]/10 # in cm
            IsoZ = beam.ControlPointSequence[0].IsocenterPosition[2]/10 # in cm
            TsIsocenter["X"].append(IsoX)
            TsIsocenter["Y"].append(IsoY)
            TsIsocenter["Z"].append(IsoZ)
    
            TsBeamNames.append(beam.BeamName)
            TsBeamTimes.append(dt)
            
            cumulative_weight = 0.0
    
            # Retrieving the control parameters per control point
            for segment in beam.ControlPointSequence:
                weight = segment.CumulativeMetersetWeight - cumulative_weight
                cumulative_weight = segment.CumulativeMetersetWeight
                globalWeight = weight * BeamMU
    
                if "PatientSupportAngle" in segment:
                    table_angle = segment.PatientSupportAngle
                else: 
                    table_angle = table_angle
    
                if "BeamLimitingDevicePositionSequence" in segment:
                    for collimator in segment.BeamLimitingDevicePositionSequence:
                        if collimator.RTBeamLimitingDeviceType[0:3] == "MLC":
                            MLC_type = collimator.RTBeamLimitingDeviceType[-1]
                            if MLC_type == "X":
                                if "BeamLimitingDeviceAngle" in segment:
                                    colli_rotation = segment.BeamLimitingDeviceAngle 
                                else:
                                    colli_rotation = colli_rotation
                                
                                number_of_leaves = len(collimator[0x300a,0x011c].value)
    
                                for i in range(1,len(collimator[0x300a,0x011c].value)+1):
                                    if i <= number_of_leaves/2:
                                        if not i in TsMLCX1:
                                            TsMLCX1[i] = []
                                            #MLCX1[i] = []
                                        if DATA["MLC_model"] == "generic" or DATA["MLC_model"] == "generichd":
                                            MLCX1[i] = (collimator[0x300a,0x011c][i-1]/10) #in cm
                                        if DATA["MLC_model"] == "VarianMillenium" or DATA["MLC_model"] == "VarianMilleniumHD":
                                            MLCX1[i] = (-collimator[0x300a,0x011c][i-1]/10) #in cm   
                                    else:
                                        i2 = str(int(i - number_of_leaves/2))
                                        if not i2 in TsMLCX2:
                                            TsMLCX2[i2] = []
                                            #MLCX2[i2] = []
                                        if DATA["MLC_model"] == "generic" or DATA["MLC_model"] == "generichd":
                                            MLCX2[i2] = (collimator[0x300a,0x011c][i-1]/10) #in cm
                                        if DATA["MLC_model"] == "VarianMillenium" or DATA["MLC_model"] == "VarianMilleniumHD":
                                            MLCX2[i2] = (collimator[0x300a,0x011c][i-1]/10)                                                 
                        else:
                            if collimator.RTBeamLimitingDeviceType[-1] == "X":
                                JX1 = collimator[0x300a,0x011c][0]/10 #in cm #.Leaf/JawPositions
                                JX2 = collimator[0x300a,0x011c][1]/10
                            else: 
                                JY1 = collimator[0x300a,0x011c][0]/10 #.Leaf/JawPositions
                                JY2 = collimator[0x300a,0x011c][1]/10
                else:
                    JX1 = JX1
                    JX2 = JX2
                    JY1 = JY1
                    JY2 = JY2
                    MLCX1 = MLCX1
                    MLCX2 = MLCX2                
    
                fieldX = np.abs(JX2-JX1)
                fieldY = np.abs(JY2-JY1)
                effectiveFieldSize = 4.*fieldX*fieldY/(2*(fieldX+fieldY))
    
                if beamEnergy == 6:
                    calibrationFactor = CONSTANTS.calibrationFactor_6MV * BSF(6,fieldX,fieldY)
                if beamEnergy == 10:
                    calibrationFactor = CONSTANTS.calibrationFactor_10MV * BSF(10,fieldX,fieldY)     
        
                if "GantryAngle" in segment:
                    gantryAngleSeg = segment.GantryAngle
                else:
                    gantryAngleSeg = gantryAngleSeg
    
                if globalWeight != 0.0: # only for control points with MU > 0
                    TsTableAngles.append(table_angle)
                    TsCollimatorAngles.append(colli_rotation)
                    TsJawX1.append(JX1)       
                    TsJawX2.append(JX2)       
                    TsJawY1.append(JY1)       
                    TsJawY2.append(JY2)  
                    TsCalFactor.append(calibrationFactor)
                    TsGantryAngles.append(gantryAngleSeg)
                    TsWeights.append(globalWeight)
                    TsStepTimes.append(dt)
                    for key in MLCX1:
                        TsMLCX1[key].append(MLCX1[key])
                    for key in MLCX2:
                        TsMLCX2[key].append(MLCX2[key])
                    
                    dt += CONSTANTS.dt 
    
    phspChunk = int(CONSTANTS.primaryHistories / len(TsWeights))
    for i in range(len(TsWeights)):
        TsPrimaries.append(phspChunk)

    PLAN_DATA = {}

    PLAN_DATA["TsBeamNames"] = TsBeamNames
    PLAN_DATA["TsStepTimes"] = TsStepTimes
    PLAN_DATA["TsBeamTimes"] = TsBeamTimes
    PLAN_DATA["TsIsocenter"] = TsIsocenter
    PLAN_DATA["TsGantryAngles"] = TsGantryAngles
    PLAN_DATA["TsCollimatorAngles"] = TsCollimatorAngles
    PLAN_DATA["TsTableAngles"] = TsTableAngles
    PLAN_DATA["TsJawX1"] = TsJawX1
    PLAN_DATA["TsJawX2"] = TsJawX2
    PLAN_DATA["TsJawY1"] = TsJawY1
    PLAN_DATA["TsJawY2"] = TsJawY2
    PLAN_DATA["TsWeights"] = TsWeights
    PLAN_DATA["TsCalFactor"] = TsCalFactor
    PLAN_DATA["TsPrimaries"] = TsPrimaries
    PLAN_DATA["TsMLCX1"] = TsMLCX1
    PLAN_DATA["TsMLCX2"] = TsMLCX2
    PLAN_DATA["MLCX1"] = MLCX1
    PLAN_DATA["MLCX2"] = MLCX2
    PLAN_DATA["phspChunk"] = phspChunk
    PLAN_DATA["finalTime"] = dt

    return PLAN_DATA
 

    

