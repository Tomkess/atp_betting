#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score

## ----- Setting the files location ----- ##
features_loc = "C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Generated Data/atp_data_features.csv"
modelling_loc = "C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Generated Data/modelling_data.csv"
pred_loc = "C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Generated Data/predict_data.csv"

## ----- Loading the Modelling Data ----- ##
features_data = pd.read_csv(features_loc)
modelling_data = pd.read_csv(modelling_loc)

## ----- Get win loss ----- ##
temp_data = modelling_data[["Player", "Date", "win_loss", "PS", "B365"]]
temp_data["B365"] = pd.to_numeric(temp_data["B365"], errors = "coerce")
temp_data["PS"] = pd.to_numeric(temp_data["PS"], errors = "coerce")
temp_data["weight"] = np.sqrt((50 - 100/temp_data.PS)**2 + (50 - 100/temp_data.B365)**2)
temp_data.drop(["B365", "PS"], axis = 1, inplace = True)

## ----- Assign Win Loss to features ----- ##
features_data = features_data.merge(temp_data, 
                                    left_on = ["Player", "Date"],
                                    right_on = ["Player", "Date"])

## ----- Remove Missing Values ----- ##
features_data = features_data.dropna()

features_data["Date"] = pd.to_datetime(features_data.Date)
def data_split(data_input, test_date_i, train_date_i):
    train_d = data_input[data_input.Date < train_date_i]
    test_d = data_input[(data_input.Date >= train_date_i) & (data_input.Date < test_date_i)]
    yield train_d.drop(["Player", "Date", "win_loss"], axis = 1)
    yield test_d.drop(["Player", "Date", "win_loss"], axis = 1)
    yield train_d.win_loss
    yield test_d.win_loss
    yield data_input[data_input.Date > test_date_i]

xtrain, xtest, ytrain, ytest, p_data = data_split(data_input = features_data, 
                                                  test_date_i = datetime(2019, 1, 1),
                                                  train_date_i = datetime(2018, 1, 1))

def xgboost_fit(n_estimators, learning_rate, min_child_weight, 
                max_depth, gamma, subsample, reg_alpha, colsample,
                weight):
    """
    Input - parameters of the model
    Output model and accuracy from cross validation.
    """
    n_estimators = int(n_estimators)
    max_depth = int(max_depth)
    min_child_weight = int(min_child_weight)
    
    reg = XGBClassifier(n_estimators = n_estimators,
                        learning_rate = learning_rate,
                        min_child_weight = min_child_weight,
                        max_depth = max_depth, 
                        gamma = gamma,
                        subsample = subsample,
                        reg_alpha = reg_alpha,
                        colsample_bytree = colsample,
                        weight = weight,
                        objective = "binary:logistic")

    evaluation = [(xtrain, ytrain), (xtest, ytest)]
    
    reg.fit(xtrain, ytrain,
            eval_set = evaluation,
            early_stopping_rounds = 10,
            verbose = False)
    
    scores = cross_val_score(reg, xtrain, ytrain, cv = 20)
    yield reg
    yield scores

## ----- Define Lerning Parameters ----- ##
model_fit, model_acc = xgboost_fit(n_estimators = 10, 
                                   learning_rate = 0.15, 
                                   min_child_weight = 4, 
                                   max_depth = 4, 
                                   gamma = 3, 
                                   subsample = 1, 
                                   reg_alpha = 0.2,
                                   colsample = 1,
                                   weight = xtrain.weight)

## ----- Get Preditions ----- ##
t_data = p_data.drop(["Date", "Player", "win_loss"], axis = 1, inplace = False)
pred_data = pd.DataFrame(model_fit.predict_proba(t_data))

output_data = pd.concat([p_data[["Date", "Player", "win_loss"]].reset_index(drop = True),
                         pred_data], axis = 1)
output_data.to_csv(pred_loc, index = False)