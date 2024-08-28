"""
  The TPS2TOPAS interface: An interface tool to parametrize treatment plans for the TrueBeam 
  radiotherapy system into OpenTOPAS parameter control files for Monte Carlo simulation.

  Authors:

  Ramon Ortiz, Ph.D.
  Department of Radiation Oncology
  University of California San Francisco.
  
  Jose Ramos-Mendez, Ph.D. *
  Department of Radiation Oncology
  University of California San Francisco.

  * corresponding author

  Please cite: 
 
  History:
      13 June 2024 - released version (v1.0)
"""

from input_handling import *
from plan_data import *
from write_PCF import *
import sys

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def printHelp():
    print('Use: TPS2TOPAS.py --m [mode] [parameterFile]')
    print(' Parameters:')
    print('   mode: gui or inputfile ')
    print('   parameterFile: ONLY IF "inputfile" mode selected: txt file including:')
    print('                 (1) Project name')
    print('                 (2) path to DICOM directory')
    print('                 (3) path to DICOM-structure file')
    print('                 (4) path to DICOM-dose file')
    print('                 (5) path to DICOM-RT plan file')
    print('                 (6) path to phase space file name')
    print('                 (7) MLC model: "generic", "Varian" or "VarianHD"')
    print('                 (8) Geometrical particle splitting factor (integer number)')
    print('                 (9) Scoring quantity: "DoseToWater" or "DoseToMedium')
    print('                (10) Output file name')
    print('                (11) Output file format: "binary", "DICOM", "csv", "root" or "xml"')
    exitProgram()

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def EvaluateCorrectInitialization():
    narg = len(sys.argv)
    if narg == 1:
        print("###### \n ERROR! incorrect use \n ######")
        printHelp()
        exitProgram()
    
    for i in range(narg):
        option = sys.argv[i].lower()
        if '--' in option:
            if option == '--help' or option == '--h':
                    printHelp()
            elif option == '--m':
                    if sys.argv[i+1] == 'gui':
                        mode = 'gui'
                        inputFile = ''
                    elif sys.argv[i+1] == 'inputfile':
                        mode = 'file'
                        try:
                            inputFile = sys.argv[i+2]
                        except:
                            print("###### \n ERROR! a parameter file is required in mode 'inputfile' \n ######")
                            printHelp()
                            exitProgram()
                        try:
                            f = open(inputFile, "r")
                        except:
                            print("###### \n ERROR! file not found \n######")
                            exitProgram()
                        f.close()
                    else: 
                        print("###### \n ERROR! Please use a valid mode \n######")
                        printHelp()
            else:
                print("###### \n ERROR! %s incorrect use \n######" % sys.argv[i])
                printHelp()
                exitProgram()
    return mode, inputFile

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def exitProgram():
    sys.exit(1)

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def main():
    # Initialization
    mode, inputFile = EvaluateCorrectInitialization()

    # Read data
    if mode == 'gui':
        DATA = InputDataInputGUIMode()
    if mode == 'file':
        DATA = InputDataInputFileMode(inputFile)

    # Create the project directory
    os.system('mkdir %s' %DATA["project_name"])
    os.system('mkdir %s/output' %DATA["project_name"])
    os.system('cp HUtoMaterialSchneider.txt %s' %DATA["project_name"])

    # Retrieve data from files exported from TPS
    CT_DATA = RetrieveCTData(DATA)
    PLAN_DATA = RetrievePlanData(DATA)
    ROI_DATA = RetrieveROIData(DATA) 

    # Write PCF
    WriteTimeFeaturesPCF(DATA,PLAN_DATA)
    WritePlanParameterFile(DATA,CT_DATA,PLAN_DATA)
    WriteGeometryFile(DATA,ROI_DATA)
    WriteMainWithVisualizationFile(DATA)
    WriteMainFile(DATA,PLAN_DATA)

    # Print output message
    print("\n--- DONE --- ")
    print(" - OpenTOPAS parameter files have been created and saved in %s" %(str(pathlib.Path().resolve())+"/"+DATA["project_name"]))
    print(" -- See above for possible warnings")
    print("-------------")

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

if __name__ == "__main__":
    main()