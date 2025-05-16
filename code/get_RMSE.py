# -*- coding: utf-8 -*-

from sklearn.metrics import mean_squared_error

def get_RMSE(obs, est):
    RMSE= mean_squared_error(obs, est) ** 0.5
    return RMSE