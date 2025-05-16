# -*- coding: utf-8 -*-

def get_MAE(obs, est):
    error = []
    for i in range(len(obs)):
        error.append(abs(obs[i] - est[i]))
    MAE=sum(error) / len(error)
    return MAE
