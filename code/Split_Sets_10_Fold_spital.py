# -*- coding: utf-8 -*-
import numpy as np
from sklearn.model_selection import KFold

def Split_Sets_10_Fold_spital(total_fold, X_all,row,col):
    a = np.unique(X_all[:,[row,col]],axis=0)
    kf = KFold(n_splits=total_fold, shuffle=True, random_state=True)
    train_index = []
    test_index = []
    for train_i, test_i in kf.split(a):
        train_data_index = []
        test_data_index = []
        train_data = a[train_i,:]
        test_data = a[test_i, :]
        for i in range(0,train_data.shape[0]):
            p=np.where((X_all[:,[row,col]] == train_data[i,:]).all(1))[0]
            train_data_index.extend(p)
        for j in range(0,test_data.shape[0]):
            q=np.where((X_all[:,[row,col]] == test_data[j,:]).all(1))[0]
            test_data_index.extend(q)
        train_index.append(train_data_index)
        test_index.append(test_data_index)
    return train_index, test_index