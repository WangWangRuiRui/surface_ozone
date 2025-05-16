# -*- coding: utf-8 -*-
import numpy as np

def get_R2(obs, est):
    corr= np.corrcoef(obs, est)
    R2=corr[1, 0] ** 2
    return R2