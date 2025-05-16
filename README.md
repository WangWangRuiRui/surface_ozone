# surface_ozone
A global land daily 10-km-resolution surface ozone dataset from 2013-2022

Download ERA5 reanalysis data:
download_ERA5.py

🟣 Ten-fold cross validation

Cross-validation based on the split 10 folds: folds validation.py

Sample-based 10-fold cross-validation: sample-based 10-fold validation.py

Spatial-based 10-fold cross-validation: spatial-based 10-fold validation.py

🟣 SDCV Validation Method
1、Produce training data for SDCV validation method: SDCV_input.m
2、Ten-fold cross validation: folds validation.py

🟣 Comparison of the effects of modelling multi-year data:
1、Creating the list of multi-year data cross-validation stations: station_location_list.m
2、Producing machine learning input data from the list of multi-year data cross-validation stations: many_years_input.m
3、Validation by the produced 10-fold cross-validation input data: folds validation.py

🟣 Production of datasets:
1、Estimated daily surface ozone: product_map.py
2、Make nc files: make_nc.m
3、Compress nc files according to the year: zip_nc.m
