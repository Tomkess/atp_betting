#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder

## ----- CATEGORICAL FEATURES ENCODING ----- ##
def categorical_features_encoding(cat_features):
    """
    Input - names of categorical features from data
    Output - one hot encoded columns 
    """
    cat_features = cat_features.apply(preprocessing.LabelEncoder().fit_transform)
    ohe = OneHotEncoder()
    cat_features = ohe.fit_transform(cat_features)
    cat_features = pd.DataFrame(cat_features.todense())
    cat_features.columns = ["cat_feature_" + str(i) for i in range(len(cat_features.columns))]
    cat_features = cat_features.astype(int)
    return cat_features

def features_players_encoding(data):
    """
    Input - data for modelling part
    Output - encoded data
    
    Description:
        columns are player names. 
        Each row corresponds to match - 
        1' are on columns corresponding to players
    """
    winners = data.Winner
    losers = data.Loser
    le = preprocessing.LabelEncoder()
    le.fit(list(winners) + list(losers))
    winners = le.transform(winners)
    losers = le.transform(losers)
    encod = np.zeros([len(winners), len(le.classes_)])
    
    for i in range(len(winners)):
        encod[i, winners[i]] += 1
    for i in range(len(losers)):
        encod[i, losers[i]] += 1
    
    columns = ["player_" + el for el in le.classes_]
    players_encoded = pd.DataFrame(encod,columns = columns)
    return players_encoded

def features_tournaments_encoding(data):
    """
    Input - column with the name of tournament
    Output - columns corresponding to name of the tournament with value 1 or 0
    
    Description: 1/0 encoding of tournament.
    """
    tournaments = data.Tournament
    le = preprocessing.LabelEncoder()
    tournaments = le.fit_transform(tournaments)
    encod = np.zeros([len(tournaments), len(le.classes_)])
    
    for i in range(len(tournaments)):
        encod[i, tournaments[i]] += 1
    columns = ["tournament_" + el for el in le.classes_]
    tournaments_encoded = pd.DataFrame(encod, columns = columns)
    return tournaments_encoded
