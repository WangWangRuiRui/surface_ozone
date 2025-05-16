# -*- coding: utf-8 -*-
import json
import lightgbm as lgb
import xgboost as xgb
import catboost as cb
import numpy as np
import time
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing
import scipy.io as scio
import os
from scipy.io import savemat
from sklearn.datasets import fetch_california_housing

path_x_tra='H:/tra_x/'
path_x_va='H:/va_x/'
files_x_tra = os.listdir(path_x_tra)
files_x_va = os.listdir(path_x_va)
files_x_tra=natsorted(files_x_tra,alg=ns.PATH)
files_x_va=natsorted(files_x_va,alg=ns.PATH)

path_y_tra='H:/tra_y/'
path_y_va='H:/va_y/'
files_y_tra = os.listdir(path_y_tra)
files_y_va = os.listdir(path_y_va)
files_y_tra=natsorted(files_y_tra,alg=ns.PATH)
files_y_va=natsorted(files_y_va,alg=ns.PATH)

RMSE_lgb=[]
MAE_lgb=[]
R2_lgb=[]
acc_lgb=[]
result=[]

for file_x_tra,file_x_va,file_y_tra,file_y_va in zip(files_x_tra,files_x_va,files_y_tra,files_y_va):
    file_path_x_tra = os.path.join(path_x_tra, file_x_tra)
    tra_X = scio.loadmat(file_path_x_tra)['x_tra']
    file_path_x_va = os.path.join(path_x_va, file_x_va)
    va_X = scio.loadmat(file_path_x_va)['x_va']

    file_path_y_tra = os.path.join(path_y_tra, file_y_tra)
    tra_y = scio.loadmat(file_path_y_tra)['y_tra']
    file_path_y_va = os.path.join(path_y_va, file_y_va)
    va_y = scio.loadmat(file_path_y_va)['y_va']
    val_y_f = list(np.array(y_val).flatten())

    lgb_train = lgb.Dataset(tra_X, tra_y)
    lgb_eval = lgb.Dataset(va_X, va_y, reference=lgb_train)

    params = dict(task='train',
                  boosting_type='gbdt',
                  objective='regression',
                  metric='rmse',
                  max_depth=18,
                  num_leaves='680',
                  learning_rate=0.08,
                  feature_fraction='0.9',
                  bagging_fraction='0.9',
                  bagging_freq='5',
                  verbose='0',
                  min_child_samples='18',
                  min_child_weight='0.001',
                  early_stopping_round=20)
    gbm = lgb.train(params, lgb_train, num_boost_round=3000, valid_sets=lgb_eval)
    y_est_lgb = gbm.predict(va_X, num_iteration=gbm.best_iteration)
    RMSE_lgb.append(get_RMSE(val_y_f , y_est_lgb))
    MAE_lgb.append(get_MAE(val_y_f , y_est_lgb))
    R2_lgb.append(get_R2(val_y_f , y_est_lgb))
    result.append(np.concatenate((va_X, va_y, np.array(y_est_lgb).reshape(-1, 1)), axis=1))

acc_lgb=np.concatenate((np.array(R2_lgb).reshape(-1, 1), np.array(RMSE_lgb).reshape(-1, 1), np.array(MAE_lgb).reshape(-1, 1)), axis=1)

file_name = 'E:/'+'result_acc_lgb.mat'
savemat(file_name, {'result_acc_lgb': acc_lgb})

file_name = 'E:/'+'result_lgb.mat'
savemat(file_name, {'result_lgb': result})