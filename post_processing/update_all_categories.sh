#!/bin/bash

echo feature_importances_correlation
python post_processing/all_categories/feature_importances_correlation.py 
echo 
echo

echo log_hazard_ratio
python post_processing/all_categories/log_hazard_ratio.py 
echo 
echo

echo scores_residual
python post_processing/all_categories/scores_residual.py 
echo 
echo

echo scores_feature_importances
python post_processing/all_categories/scores_feature_importances.py
echo 
echo

echo information
python post_processing/all_categories/information.py
echo 
echo

