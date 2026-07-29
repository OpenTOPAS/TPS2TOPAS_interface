import pydicom
import numpy as np
from tkinter import filedialog
from tkinter import *
import sys

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

def EvaluateCorrectInputData(DATA):
    warnings = 0

    if DATA["MLC_model"] == 'generic diverging mlc' or DATA["MLC_model"] == 'generic':
        DATA["MLC_model"] = "generic"
    if DATA["MLC_model"] == 'generic hd diverging mlc' or DATA["MLC_model"] == 'generichd':
        DATA["MLC_model"] = "generichd"
    elif DATA["MLC_model"] == 'varian 120 millenium (extension required)' or DATA["MLC_model"] == 'varian':
        DATA["MLC_model"] = "VarianMillenium"
    elif DATA["MLC_model"] == 'varian 120 millenium hd (extension required)' or DATA["MLC_model"] == 'varianhd':
        DATA["MLC_model"] = "VarianMilleniumHD"
    else:
        print("--- WARNING: No valid MLC model selected (%s) - generic divergent MLC used by default" %DATA["MLC_model"])
        DATA["MLC_model"] = "generic"
        warnings +=1
    if type(DATA["multipleUse"]) != 'int':
        try:
            DATA["multipleUse"] = int(DATA["multipleUse"])
        except:
            print("--- WARNING: Geometrical particle splitting factor is not an integer - value 1 used")
            DATA["multipleUse"] = 1
            warnings +=1

    if DATA["scoring_quantity"] == 'dosetowater':
        DATA["scoring_quantity"] = "DoseToWater"
    elif DATA["scoring_quantity"] == 'dosetomedium':
        DATA["scoring_quantity"] = "DoseToMedium"
    elif DATA["scoring_quantity"] == 'phasespace':
        DATA["scoring_quantity"] = "PhaseSpace"
    else:
        print("--- WARNING: No valid scoring quantity selected (%s) - DoseToMedium used by default" %DATA["scoring_quantity"])
        DATA["scoring_quantity"] = "DoseToMedium"
        warnings +=1
    
    if DATA["output_format"] != "binary" and DATA["output_format"] != "csv" and DATA["output_format"] != "dicom" and DATA["output_format"] != "root" and DATA["output_format"] != "ascii" and DATA["output_format"] != "xml":
        print("--- WARNING: No valid Output Format selected (%s) - binary format used by default" %DATA["output_format"])
        DATA["output_format"] = "binary"
        warnings +=1
    
    if DATA["phsp_filename"].endswith('phsp'):
        DATA["phsp_filename"] = DATA["phsp_filename"][:-5]
    if DATA["phsp_filename"].endswith('header'):
        DATA["phsp_filename"] = DATA["phsp_filename"][:-7]

    print("Input information:")
    print("     (1) Project name:           %s" % DATA["project_name"])
    print("     (2) DICOM directory:        %s" % DATA["dicom_dirname"])
    print("     (3) DICOM-structure file:   %s" % DATA["RS_filename"])
    print("     (4) DICOM-dose file:        %s" % DATA["RD_filename"])
    print("     (5) DICOM-RT plan file:     %s" % DATA["RP_filename"])
    print("     (6) Phase space file name:  %s" % DATA["phsp_filename"])
    print("     (7) MLC model:              %s" % DATA["MLC_model"])
    print("     (8) Geometrical particle splitting factor: %s" % DATA["multipleUse"])
    print("     (9) Scoring quantity:       %s" % DATA["scoring_quantity"])
    print("    (10) Output file name:       %s" % DATA["output_file"])
    print("    (11) Output format:          %s" % DATA["output_format"])
    if DATA["scoring_quantity"] == "PhaseSpace":
        print("    (12) ROIs to score:          %s" % DATA["ROIs_to_score"])

    return DATA

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

def InputDataInputFileMode(inputFile):
    inputInfo = open(inputFile,'r').read().split('\n')
    inputInfo = list(filter(None, inputInfo)) # filter empty lines
    if len(inputInfo) != 13 and inputInfo[9].lower() == 'phasespace':
        print("######")
        print('ERROR! %s arguments found in input file. %s arguments required' %(len(inputInfo),13))
        print("######")
        printHelp()
        exit(0)
    elif len(inputInfo) != 12 and inputInfo[9].lower() != 'phasespace':
        print("######")
        print('ERROR! %s arguments found in input file. %s arguments required' %(len(inputInfo),12))
        print("######")
        printHelp()
        exit(0)
    
    DATA = {}
    ROI_List = {}
    project_name_temp = inputInfo[0]
    DATA["project_name"]        = project_name_temp.replace(" ", "_")
    DATA["OS"]                  = inputInfo[1]
    DATA["dicom_dirname"]       = inputInfo[2]
    DATA["RS_filename"]         = inputInfo[3] 
    DATA["RD_filename"]         = inputInfo[4]
    DATA["RP_filename"]         = inputInfo[5]
    DATA["phsp_filename"]       = inputInfo[6]
    DATA["MLC_model"]           = inputInfo[7].lower()
    DATA["multipleUse"]         = inputInfo[8]
    DATA["scoring_quantity"]    = inputInfo[9].lower() 
    output_file_temp = inputInfo[10]
    DATA["output_file"]         = output_file_temp.replace(" ", "_")
    DATA["output_format"]    = inputInfo[11].lower()


    if DATA["scoring_quantity"] == 'phasespace':
        DATA["ROIs_to_score"]     = inputInfo[12].split(',')
        for roi in DATA["ROIs_to_score"]:
            newroi = roi.strip()
            for letter in range(len(newroi)):
                if newroi[letter] == ' ':
                    newroi = newroi.replace(' ','_')
                if '.' in newroi:
                    newroi = newroi.replace('.','_')
                if '+' in newroi:
                    newroi = newroi.replace('+','_')
            DATA["ROIs_to_score"][DATA["ROIs_to_score"].index(roi)] = newroi
    
        ds_RS = pydicom.dcmread(DATA["RS_filename"])
        RoiGeometries = ds_RS.RTROIObservationsSequence
        ROI_List = {}
        for roi in RoiGeometries:
            for region in ds_RS.StructureSetROISequence:
                if region.ROINumber == roi.ReferencedROINumber:
                    roiName = region.ROIName
                    for letter in range(len(roiName)):
                        if roiName[letter] == ' ':
                            
                            roiName = roiName.replace(' ','_')
                        if '.' in roiName:
                            roiName = roiName.replace('.','_')
                        if '+' in roiName:
                            roiName = roiName.replace('+','_')
                    if len(roiName) > 16:
                        roiName = roiName[:16]
                        print("--- WARNING: The ROI %s has a name longer than 16 characters. The name will be truncated to %s. Please rename in structure set" %(roiName,roiName[:16]))
                    ROI_List[region.ROINumber] = roiName

    
        for roi in DATA["ROIs_to_score"]:
            score = 0 
            for region in ds_RS.StructureSetROISequence:
                if roi == ROI_List[region.ROINumber]:
                    score = score + 1
            if score == 0:
                print("######")
                print('ERROR! The ROI %s specified in the input file do not match the ROIs found in the DICOM-structure file'%roi)
                print("######")
                exit(0)
            elif score > 1:
                print("######")
                print('ERROR! The ROI %s specified in the input file match multiple ROIs found in the DICOM-structure file'%roi)
                print("######")
                exit(0)

    return EvaluateCorrectInputData(DATA)

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################



def _quit():
    root.quit()
    root.destroy() 

def InputDataInputGUIMode():

    ### functions to handle the GUI
    global dicomDirectoryName
    def browse_dicom_button():
        global dicomDirectoryName 
        filename = filedialog.askdirectory()
        dicomDirectoryName.set(filename)
    
    global dicomStructureFileName
    def browse_dicom_structure_button():
        global dicomStructureFileName 
        filename = filedialog.askopenfilename() 
        dicomStructureFileName.set(filename)
    
    global dicomDoseFileName
    def browse_dicom_dose_button():
        global dicomDoseFileName 
        filename = filedialog.askopenfilename() 
        dicomDoseFileName.set(filename)
    
    global dicomRTplanFileName
    def browse_dicom_RTplan_button():
        global dicomRTplanFileName 
        filename = filedialog.askopenfilename() 
        dicomRTplanFileName.set(filename)
    
    global phspFileName
    def browse_phsp_button():
        global phspFileName 
        filename = filedialog.askopenfilename() 
        phspFileName.set(filename)
    
    global root; root = Tk()
    root.title("TPS2TOPAS Interface")
    ################
    i = 1
    label0=StringVar()
    label0.set('Project name:')
    lbl0 = Label(master=root, textvariable=label0)
    lbl0.grid(row=i, column=1)
    
    projectName = StringVar()
    projectName.set('Project_1')
    projectEntry = Entry(master=root, textvariable=projectName)
    projectEntry.grid(row=i, column=2)
    ################
    ################
    i += 1
    label13=StringVar()
    label13.set("Operating System")
    lbl13 = Label(master=root, textvariable=label13)
    lbl13.grid(row=i, column=1)
    OperatingSys = StringVar()
    OperatingSys.set('select')
    options = ["Linux/MacOS","Windows"]
    OSentry = OptionMenu(root , OperatingSys , *options)
    OSentry.grid(row=i, column=2)

    lbl13 = Label()
    lbl13.grid(row=i+1, column=1)
    ################
    ################
    i += 1
    label1=StringVar()
    label1.set('DICOM directory')
    lbl1 = Label(master=root, textvariable=label1) 
    lbl1.grid(row=i, column=1)
    button1 = Button(text="Browse", command=browse_dicom_button)
    button1.grid(row=i, column=2)
    
    dicomDirectoryName = StringVar()
    dicomDirectoryName.set('')
    lbl1 = Label(master=root, textvariable=dicomDirectoryName)
    lbl1.grid(row=i+1, column=1)
    ################    
    ################
    i += 2
    label2=StringVar()
    label2.set('DICOM-structure file')
    lbl2 = Label(master=root, textvariable=label2) 
    lbl2.grid(row=i, column=1)
    button2 = Button(text="Browse", command=browse_dicom_structure_button)
    button2.grid(row=i, column=2)
    
    dicomStructureFileName = StringVar()
    dicomStructureFileName.set('')
    lbl2 = Label(master=root, textvariable=dicomStructureFileName)
    lbl2.grid(row=i+1, column=1)
    ################ 
    ################
    i += 2
    label3=StringVar()
    label3.set('DICOM-dose file')
    lbl3 = Label(master=root, textvariable=label3) 
    lbl3.grid(row=i, column=1)
    button3 = Button(text="Browse", command=browse_dicom_dose_button)
    button3.grid(row=i, column=2)
    
    dicomDoseFileName = StringVar()
    dicomDoseFileName.set('')
    lbl3 = Label(master=root, textvariable=dicomDoseFileName)
    lbl3.grid(row=i+1, column=1)
    ################
    ################
    i += 2
    label4=StringVar()
    label4.set('DICOM-RT plan file')
    lbl4 = Label(master=root, textvariable=label4) 
    lbl4.grid(row=i, column=1)
    button4 = Button(text="Browse", command=browse_dicom_RTplan_button)
    button4.grid(row=i, column=2)
    
    dicomRTplanFileName = StringVar()
    dicomRTplanFileName.set('')
    lbl4 = Label(master=root, textvariable=dicomRTplanFileName)
    lbl4.grid(row=i+1, column=1)
    ################
    ################ 
    i += 2
    label5=StringVar()
    label5.set('Phase space file name:')
    lbl5 = Label(master=root, textvariable=label5)
    lbl5.grid(row=i, column=1)
    button5 = Button(text="Browse", command=browse_phsp_button)
    button5.grid(row=i, column=2)
    
    phspFileName = StringVar()
    phspFileName.set('')
    lbl5 = Label(master=root, textvariable=phspFileName)
    lbl5.grid(row=i+1, column=1)
    ################
    ################
    i += 2
    label6=StringVar()
    label6.set("MLC model")
    lbl6 = Label(master=root, textvariable=label6)
    lbl6.grid(row=i, column=1)
    MLCmodel = StringVar()
    MLCmodel.set('select')
    options = ["generic diverging MLC","generic HD diverging MLC", "Varian 120 Millenium (extension required)", "Varian 120 Millenium HD (extension required)"]
    MLCentry = OptionMenu(root , MLCmodel , *options)
    MLCentry.grid(row=i, column=2)

    lbl6 = Label()
    lbl6.grid(row=i+1, column=1)
    ################
    ################
    i += 2
    label7=StringVar()
    label7.set('Geometrical particle splitting factor:')
    lbl7 = Label(master=root, textvariable=label7)
    lbl7.grid(row=i, column=1)
    multipleUse = IntVar()
    multipleUse.set(1)
    multEntry = Entry(master=root, textvariable=multipleUse)
    multEntry.grid(row=i, column=2)

    lbl7 = Label()
    lbl7.grid(row=i+1, column=1)
    ################
    ################
    i += 2
    label8=StringVar()
    label8.set("Scoring quantity")
    lbl8 = Label(master=root, textvariable=label8)
    lbl8.grid(row=i, column=1)
    Scoring = StringVar()
    Scoring.set('select')
    options = ["DoseToWater", "DoseToMedium", "PhaseSpace"]
    scoringentry = OptionMenu(root , Scoring , *options)
    scoringentry.grid(row=i, column=2)

    lbl8 = Label()
    lbl8.grid(row=i+1, column=1)
    ################    
    ################
    i += 2
    label9=StringVar()
    label9.set('Output file name:')
    lbl9 = Label(master=root, textvariable=label9)
    lbl9.grid(row=i, column=1)
    outFileName = StringVar()
    outFileName.set('output')
    outEntry = Entry(master=root, textvariable=outFileName)
    outEntry.grid(row=i, column=2)

    lbl9 = Label()
    lbl9.grid(row=i+1, column=1)
    ################   
    ################
    i += 2
    label10=StringVar()
    label10.set("Output format")
    lbl10 = Label(master=root, textvariable=label10)
    lbl10.grid(row=i, column=1)
    outputFormat = StringVar()
    outputFormat.set('select')
    options = ["binary", "DICOM", "csv", "root", "xml", "ASCII"]
    Outpytentry = OptionMenu(root , outputFormat , *options)
    Outpytentry.grid(row=i, column=2)

    lbl10 = Label()
    lbl10.grid(row=i+1, column=1)
    ################
    ################
    i += 2
    exitButton = Button(text="Generate TOPAS files", command=_quit)
    exitButton.grid(row=i, column=1)
    lbl11 = Label()
    lbl11.grid(row=i+1, column=1)
    ################
    ################
    i += 0
    abortButton = Button(text="Exit", command=exitProgram)
    abortButton.grid(row=i, column=2)
    lbl12 = Label()
    lbl12.grid(row=i+1, column=2)
    ################
    mainloop()
     
    DATA = {}
    project_name_temp = projectName.get()
    DATA["project_name"]        = project_name_temp.replace(" ", "_")
    DATA["OS"]                  = OperatingSys.get().lower()
    DATA["dicom_dirname"]       = dicomDirectoryName.get()
    DATA["RS_filename"]         = dicomStructureFileName.get()
    DATA["RD_filename"]         = dicomDoseFileName.get()
    DATA["RP_filename"]         = dicomRTplanFileName.get()
    DATA["phsp_filename"]       = phspFileName.get()
    DATA["MLC_model"]           = MLCmodel.get().lower()
    DATA["multipleUse"]         = multipleUse.get()
    DATA["scoring_quantity"]    = Scoring.get().lower()
    output_file_temp = outFileName.get()
    DATA["output_file"]         = output_file_temp.replace(" ", "_")
    DATA["output_format"]    = outputFormat.get().lower()
    
    
    if DATA["scoring_quantity"] == "phasespace":
        ds_RS = pydicom.dcmread(DATA["RS_filename"])
        RoiGeometries = ds_RS.RTROIObservationsSequence
        ROI_List = {}
        for roi in RoiGeometries:
            for region in ds_RS.StructureSetROISequence:
                if region.ROINumber == roi.ReferencedROINumber:
                    roiName = region.ROIName
                    for letter in range(len(roiName)):
                        if roiName[letter] == ' ':
                            
                            roiName = roiName.replace(' ','_')
                        if '.' in roiName:
                            roiName = roiName.replace('.','_')
                        if '+' in roiName:
                            roiName = roiName.replace('+','_')
                    if len(roiName) > 16:
                        roiName = roiName[:16]
                    ROI_List[region.ROINumber] = roiName

        DATA["ROIs_to_score"] = []
        DATA["ROIs_to_score"] = ChooseROIs(ROI_List)

    return EvaluateCorrectInputData(DATA)
############################################################################################################################################
############################################################################################################################################
############################################Choose ROIs to score from DICOM-structure file##################################################
############################################################################################################################################
############################################################################################################################################

def ChooseROIs(ROI_List):
    selected_ROIs = []
    ROI_List = dict(sorted(ROI_List.items()))
    def _quit_ROI():
        nonlocal selected_ROIs
        selected_ROIs = [ROI_List[i+1] for i in listbox.curselection()]
        roi_root.quit()
        roi_root.destroy() 
        
    global roi_root; roi_root = Tk()
    roi_root.title("Select ROIs to score")
    roi_root.geometry('180x200')

    listbox = Listbox(roi_root, width=40,height=10, selectmode=MULTIPLE)
    idx = 0
    for key in ROI_List:
        
        listbox.insert(idx, ROI_List[key])
        idx+=1
    # print(ROI_List)
    # print(selected_ROIs)
    listbox.pack()

    exitButton = Button(text="Confirm selection", command=_quit_ROI)
    exitButton.pack()

    mainloop()

    return selected_ROIs