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
from sklearn.model_selection import KFold
import os
from scipy.io import savemat
from sklearn.datasets import fetch_california_housing

dataFile_X = 'E:/code/variable.mat'
dataFile_Y = 'E:/code/site.mat'
y_all = scio.loadmat(dataFile_Y)['site']
X_all = scio.loadmat(dataFile_X)['variable']

lgb_train = lgb.Dataset(X_train, y_train)

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
                  min_child_weight='0.001')
gbm = lgb.train(params,lgb_train,num_boost_round=3000)

path_x_nosite='H:/nosite_addimage_addrers/' + r +'/'
path_x_site='H:/site_addimage_addrers/' + r +'/'
files_x_nosite = os.listdir(path_x_nosite)
files_x_site = os.listdir(path_x_site)
files_x_nosite=natsorted(files_x_nosite,alg=ns.PATH)
files_x_site=natsorted(files_x_site,alg=ns.PATH)

path_xy_nosite='H:/nosite_addimage_addrers/' + r +'/'
path_xy_site='H:/site_addimage_addrers/' + r +'/'
files_xy_nosite = os.listdir(path_xy_nosite)
files_xy_site = os.listdir(path_xy_site)
files_xy_nosite=natsorted(files_xy_nosite,alg=ns.PATH)
files_xy_site=natsorted(files_xy_site,alg=ns.PATH)

for file_x_nosite,file_x_site,file_xy_nosite,file_xy_site in zip(files_x_nosite,files_x_site,files_xy_nosite,files_xy_site):
    file_path_x_nosite = os.path.join(path_x_nosite, file_x_nosite)
    x_nosite = scio.loadmat(file_path_x_nosite)['result_nan']
    file_path_x_site = os.path.join(path_x_site, file_x_site)
    x_site = scio.loadmat(file_path_x_site)['result_nonan']
    x_site_pred = x_site[:,1:x_site.shape[1]]

    file_path_xy_nosite = os.path.join(path_xy_nosite, file_xy_nosite)
    xy_nosite = scio.loadmat(file_path_xy_nosite)['xy_nan']
    file_path_xy_site = os.path.join(path_xy_site, file_xy_site)
    xy_site = scio.loadmat(file_path_xy_site)['xy_nonan']

    y_nosite_Pred = gbm.predict(x_site_pred , num_iteration=gbm.best_iteration)
    y_site_Pred = gbm.predict(x_nosite, num_iteration=gbm.best_iteration)
    print("Start outputing "+ file_path_x_nosite + "...")
    result = get_Result_lonlat(y_site_Pred, y_nosite_Pred, xy_site, xy_nosite)

    file_name = 'H:/result/' + r + '/' + file_x_nosite[0:8] + '_result' + '.mat'
    savemat(file_name, {'result': result})
