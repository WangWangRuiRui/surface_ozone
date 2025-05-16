# -*- coding: utf-8 -*-
import numpy as np

def get_Result_lonlat(y, y_Pred,lonlat_y,lonlat_y_Pred):
    y = y.flatten()
    data = np.concatenate((y, y_Pred), axis=0)
    lonlat=np.concatenate((lonlat_y, lonlat_y_Pred), axis=0)
    result = np.zeros((1800, 3600))
    for i in range(1, lonlat.shape[0]):
        row_i = int(lonlat[i - 1, 0]) - 1
        col_i = int(lonlat[i - 1, 1]) - 1
        d = data[i - 1]
        result[row_i, col_i] = d
    result = np.where(result, result, np.nan)
    return result