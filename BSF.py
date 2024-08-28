import numpy as np

def BSF(E,X,Y):
    # this function determines the backscattering factors based on experimental data from (Zavgorodni et al, 20014)
    
    field_sizes = [1,2,3,6,10,15,25,40] # from (Zavgorodni et al, 20014)
    
    BSF = {}
    
    BSF[6] = np.array([
    [0.988, 0.988, 0.988, 0.988, 0.988, 0.988, 0.988, 0.989],
    [0.998, 0.999, 0.999, 0.999, 0.999, 0.999, 1.000, 1.000],
    [0.998, 0.999, 0.999, 0.999, 0.999, 1.000, 1.000, 1.000],
    [0.999, 0.999, 0.999, 1.000, 1.000, 1.000, 1.001, 1.001],
    [0.999, 0.999, 1.000, 1.000, 1.000, 1.001, 1.001, 1.001],
    [1.000, 1.000, 1.001, 1.001, 1.001, 1.001, 1.002, 1.002],
    [1.001, 1.001, 1.001, 1.002, 1.002, 1.002, 1.002, 1.003]]) # from (Zavgorodni et al, 20014)
    
    BSF[10] = np.array([
    [0.993, 0.993, 0.993, 0.993, 0.993, 0.993, 0.994, 0.994],
    [0.998, 0.998, 0.998, 0.998, 0.998, 0.999, 0.999, 0.999],
    [0.998, 0.998, 0.999, 0.999, 0.999, 1.000, 1.000, 1.000],
    [0.999, 0.999, 0.999, 1.000, 1.000, 1.000, 1.001, 1.001],
    [1.000, 1.000, 1.001, 1.001, 1.001, 1.002, 1.002, 1.002],
    [1.001, 1.001, 1.002, 1.003, 1.003, 1.004, 1.004, 1.005]]) # from (Zavgorodni et al, 20014)

    JawX = min(field_sizes, key=lambda x: abs(x - X))
    JawY = min(field_sizes, key=lambda x: abs(x - Y))

    index_JawX = field_sizes.index(JawX)
    index_JawY = field_sizes.index(JawY)

    return BSF[E][index_JawY,index_JawX]