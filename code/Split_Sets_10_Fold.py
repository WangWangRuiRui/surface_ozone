# -*- coding: utf-8 -*-

from sklearn.model_selection import KFold

def Split_Sets_10_Fold(total_fold, data):
    train_index = []
    test_index = []
    kf = KFold(n_splits=total_fold, shuffle=True, random_state=True)
    for train_i, test_i in kf.split(data):
        train_index.append(train_i)
        test_index.append(test_i)
    return train_index, test_index