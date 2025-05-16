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

s_time = time.time()

dataFile_X = 'E:/code/variable.mat'
dataFile_Y = 'E:/code/site.mat'
y_all = scio.loadmat(dataFile_Y)['site']
X_all = scio.loadmat(dataFile_X)['variable']

RMSE_lgb=[]
MAE_lgb=[]
R2_lgb=[]
RMSE_xgb=[]
MAE_xgb=[]
R2_xgb=[]
RMSE_cab=[]
MAE_cab=[]
R2_cab=[]

lgb_time=[]
xgb_time=[]
cab_time=[]

acc_lgb=[]
acc_xgb=[]
acc_cab=[]

result=[]

total_fold = 10
# spatial-based 10-fold valification
[train_index, test_index] = Split_Sets_10_Fold_spital(total_fold, X_all)

for fold in range(0, 10):
    X_train = X_all[train_index[fold], :]
    y_train = y_all[train_index[fold], :]
    X_val = X_all[test_index[fold], :]
    y_val = y_all[test_index[fold], :]
    y_train_f = list(np.array(y_train).flatten())
    y_val_f =list(np.array(y_val).flatten())

    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_val, y_val, reference=lgb_train)

    lgb_b_time = time.time()
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
    gbm = lgb.train(params,lgb_train,num_boost_round=3000,valid_sets=lgb_eval)
    lgb_e_time = time.time()
    y_est_lgb = gbm.predict(X_val, num_iteration=gbm.best_iteration)
    lgb_time.append(lgb_e_time-lgb_b_time)
    RMSE_lgb.append(get_RMSE(y_val_f, y_est_lgb))
    MAE_lgb.append(get_MAE(y_val_f, y_est_lgb))
    R2_lgb.append(get_R2(y_val_f, y_est_lgb))
    result.append(np.concatenate((X_val,y_val,np.array(y_est_lgb).reshape(-1,1)), axis=1))

    xgb_b_time = time.time()
    xlf = xgb.XGBRegressor(max_depth=12,
                           learning_rate=0.08,
                           n_estimators=3000,
                           objective='reg:squarederror',
                           nthread=-1,
                           subsample=0.8,
                           colsample_bytree=0.8,
                           reg_alpha=0,
                           reg_lambda=1,
                           scale_pos_weight=1,
                           seed=622,
                           early_stopping_rounds=20)
    eval_set = [(X_val, y_val)]
    xlf.fit(X_train, y_train,eval_set=eval_set)
    xgb_e_time = time.time()
    y_est_xgb = xlf.predict(X_val)
    xgb_time.append(xgb_e_time-xgb_b_time)
    RMSE_xgb.append(get_RMSE(y_val_f, y_est_xgb))
    MAE_xgb.append(get_MAE(y_val_f, y_est_xgb))
    R2_xgb.append(get_R2(y_val_f, y_est_xgb))

    cab_b_time = time.time()
    params = {'learning_rate': 0.2,
              'loss_function': "RMSE",
              'eval_metric': "RMSE",
              'depth': 6,
              'min_data_in_leaf': 20,
              'random_seed': 42,
              'logging_level': 'Silent',
              'one_hot_max_size': 5,
              'boosting_type': "Ordered",
              'max_ctr_complexity': 2,
              'nan_mode': 'Min',
              'use_best_model': True}
    model = cb.CatBoostRegressor(iterations=3000,early_stopping_rounds=20,**params)
    clf = model.fit(X_train, y_train, eval_set=(X_val, y_val))
    cab_e_time = time.time()
    y_est_cab = clf.predict(X_val)
    cab_time.append(cab_e_time-cab_b_time)
    RMSE_cab.append(get_RMSE(y_val_f, y_est_cab))
    MAE_cab.append(get_MAE(y_val_f, y_est_cab))
    R2_cab.append(get_R2(y_val_f, y_est_cab))


acc_lgb=np.concatenate((np.array(R2_lgb).reshape(-1, 1), np.array(RMSE_lgb).reshape(-1, 1), np.array(MAE_lgb).reshape(-1, 1), np.array(lgb_time).reshape(-1, 1)), axis=1)
acc_xgb=np.concatenate((np.array(R2_xgb).reshape(-1, 1), np.array(RMSE_xgb).reshape(-1, 1), np.array(MAE_xgb).reshape(-1, 1), np.array(xgb_time).reshape(-1, 1)), axis=1)
acc_cab=np.concatenate((np.array(R2_cab).reshape(-1, 1), np.array(RMSE_cab).reshape(-1, 1), np.array(MAE_cab).reshape(-1, 1), np.array(cab_time).reshape(-1, 1)), axis=1)

file_name = 'E:/'+'result_acc_lgb.mat'
savemat(file_name, {'result_acc_lgb': acc_lgb})
file_name = 'E:/'+'result_acc_xgb.mat'
savemat(file_name, {'result_acc_xgb': acc_xgb})
file_name = 'E:/'+'result_acc_cab.mat'
savemat(file_name, {'result_acc_cab': acc_cab})

file_name = 'E:/'+'result_lgb.mat'
savemat(file_name, {'result_lgb': result})
