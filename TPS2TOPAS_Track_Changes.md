track changes to TPS2TOPAS

Changes implemented by Justin Stanton-Sheetz 1/14/2026





\####################### Changes/additions ###############################

**inputfile\_template:**

 	Added OS to the template

**input\_handling:**

 	Added "PhaseSpace" to the options for Scoring Quantity dropdown

 	Added OS option to inputFile mode

 	Adjusted numbers in inputfile mode to fit OS choice in

 	Added "ASCII" to output format

 	Added if statement to score "PhaseSpace" 

 	Added a selection button for OS. 2 choices Linux/iOS or Windows. This will allow for some specific changes built for the wsl environment to be 			able to access files stored in windows drives

 	Added ASCII and PhaseSpace to the checks for errors and added input file length check dependent on if PhaseSpace is chosen (13 inputs instead of 		12 so you can choose ROIs to score)

 	For inputfile mode: Added reading, converting, and checking of line 13. This checks that the ROIs listed are within the structure set and TOPAS 		can read them (lines 122-170)

 	For GUI Mode: If scoring quantity is phasespace, user will be prompted with a second gui that allows for ROI selection from the structure set.

 		Added ChooseROIs function to prompt said gui

 

**TPS2TOPAS:**

 	Changed cp to copy for windows (line 125) with if statement

**write\_PCF:**

 	changed theta view angle for phase space to 0 degrees. Honestly I think this should be the case for all, but I don't want to mess up what is 			already here if there is a good reason for 89.9 degrees.

 	added if statement for file path in TOPAS file. If OS is selected to be windows it will change the file path from a drive (like C:/... or H:/... 		to something WSL can read like "/mnt/c/..."

 	Added if statement to adjust the scoring for PhaseSpace if selected. This will make scoring for all separate structures selected

 	Added If statement to visualization file so that ROIs are colored on DICOM. They all are set to yellow. User can change the topas file if desired.



**plan\_data:**

 	Added a warning if a beam has 0 MU

