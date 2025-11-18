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

import argparse
import pathlib
import sys

from input_handling import *
from plan_data import *
from write_PCF import *

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def build_argument_parser():
    description = (
        "Convert Varian TrueBeam treatment plans into TOPAS-ready parameter control files.\n"
        "Use GUI mode for interactive entry or inputfile mode for scripted conversions."
    )
    parser = argparse.ArgumentParser(
        prog="TPS2TOPAS.py",
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["gui", "inputfile"],
        default="gui",
        help="Run the GUI (default) or provide parameters via an input file.",
    )
    parser.add_argument(
        "-i",
        "--input-file",
        metavar="PATH",
        help="Path to the 11-line parameter file (required for inputfile mode).",
    )
    parser.add_argument(
        "legacy_input_file",
        nargs="?",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="TPS2TOPAS interface v1.0",
    )
    return parser

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def parse_cli_arguments(argv=None):
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    mode = args.mode.lower()
    legacy_file = args.input_file or args.legacy_input_file

    if mode == "inputfile":
        if not legacy_file:
            parser.error("inputfile mode requires --input-file PATH.")
        input_path = pathlib.Path(legacy_file).expanduser()
        if not input_path.exists():
            parser.error(f"Input file not found: {input_path}")
        return "file", str(input_path)

    if args.input_file or args.legacy_input_file:
        parser.error("An input file may only be supplied when --mode inputfile is selected.")
    return "gui", ""

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def main():
    # Initialization
    mode, inputFile = parse_cli_arguments()

    # Read data
    if mode == 'gui':
        DATA = InputDataInputGUIMode()
    if mode == 'file':
        try:
            DATA = InputDataInputFileMode(inputFile)
        except ValueError as exc:
            print("######")
            print(f" ERROR! {exc}")
            print("######")
            sys.exit(1)

    # Create the project directory
    os.system('mkdir %s' %DATA["project_name"])
    os.system('mkdir %s/output' %DATA["project_name"])
    os.system('cp HUtoMaterialSchneider.txt %s' %DATA["project_name"])

    # Retrieve data from files exported from TPS
    if DATA["score_phase_space"]:
        CT_DATA = {"cx": 0.0, "cy": 0.0, "cz": 0.0}
        ROI_DATA = {"materials": {}, "elements": {}, "roiWithMaterials": {}}
    else:
        CT_DATA = RetrieveCTData(DATA)
        ROI_DATA = RetrieveROIData(DATA)
    PLAN_DATA = RetrievePlanData(DATA)

    # Write PCF
    WriteTimeFeaturesPCF(DATA,PLAN_DATA)
    WritePlanParameterFile(DATA,CT_DATA,PLAN_DATA)
    WriteGeometryFile(DATA,ROI_DATA,CT_DATA)
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
