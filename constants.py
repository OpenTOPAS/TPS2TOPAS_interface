class _Constants:
    # Calibration factor to convert MC calculated dose 
    # per primary history to 1 cGy/MU
    # 100 cm SSD
    calibrationFactor_6MV = 3.56647e+12 # From exponential fit
    calibrationFactor_10MV = 2.8867e+12 # From max dose

    # This script distributes evenly the Varian phase space 
    # to each control point, then the dose per control point
    # is scaled by the calibrationFactor the number of MU, and BSF.
    # Thus, we set explicitly the number of primary histories
    # obtained from the Varian phase spaces
    primaryHistories = 46041000 # from number of histories in Varian phsp

    # We stablish the TOPAS time feature unit time to 1 s.
    dt = 1.0

CONSTANTS = _Constants

