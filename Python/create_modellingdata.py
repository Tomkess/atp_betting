#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## ----- Loading the modules ----- ##
from datetime import datetime
from datetime import timedelta
from elo_features import *
from categorical_features import *
from stategy_assessment import *
import glob
import pandas as pd
import numpy as np
import xgboost as xgb
import sklearn
from sklearn.model_selection import StratifiedKFold, KFold

###############################################################################
## Data Preparation - Download, Preprocessing, Features #######################
###############################################################################

## ----- Building of the raw dataset ----- ##

# Importation of the Excel files - 1 per year (from tennis.co.uk)
# Some preprocessing is necessary because for several years the odds are not present
# We consider only the odds of Bet365 and Pinnacle.

filenames = list(glob.glob("C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Downloaded Data/men/20*.xls*")) + list(glob.glob("C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Downloaded Data/women/20*.xls*"))
l = [pd.read_excel(filename, encoding = 'latin-1') for filename in filenames]
no_b365 = [i for i,d in enumerate(l) if "B365W" not in l[i].columns]
no_pi = [i for i,d in enumerate(l) if "PSW" not in l[i].columns]

for i in no_pi:
    l[i]["PSW"] = np.nan
    l[i]["PSL"] = np.nan
for i in no_b365:
    l[i]["B365W"] = np.nan
    l[i]["B365L"] = np.nan
l = [d[list(d.columns)[:13] + ["Wsets","Lsets","Comment"] + ["PSW","PSL","B365W","B365L"]] for d in [l[0]] + l[2:]]
data = pd.concat(l,0)

# - data cleaning
data = data[pd.notnull(data['Date'])]
data = data.sort_values("Date")
data["WRank"] = data["WRank"].replace(np.nan, 0)
data["WRank"] = data["WRank"].replace("NR", 2000)
data["LRank"] = data["LRank"].replace(np.nan, 0)
data["LRank"] = data["LRank"].replace("NR", 2000)
data["WRank"] = data["WRank"].astype(int)
data["LRank"] = data["LRank"].astype(int)
data["Wsets"] = data["Wsets"].astype(float)
data["Lsets"] = data["Lsets"].replace("`1", 1)
data["Lsets"] = data["Lsets"].astype(float)
data = data.reset_index(drop = True)

# - computing of the elo ranking
elo_rankings = compute_elo_rankings(data)
data = pd.concat([data, elo_rankings], 1)

# - drop columns
data.drop(['Round', 'Best of', 'ATP', 'Location', 'Tier', 'Series'], 
          axis = 1, inplace = True)

# - storage of the raw dataset
data.to_csv("C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Generated Data/atp_data.csv", index = False)
data = pd.read_csv("C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Generated Data/atp_data.csv")
data.Date = data.Date.apply(lambda x:datetime.strptime(x, '%Y-%m-%d'))

## ----- The period that interests us ----- ##
beg = datetime(2000, 1, 1)
end = data.Date.iloc[-1]
indices = data[(data.Date > beg) & (data.Date <= end)].index

## ----- Selection of our period ----- ##
data = data.iloc[indices,:].reset_index(drop = True)

## ----- Encoding of categorical features ----- ##
master_data = pd.get_dummies(data, columns = ['Court', 'Surface', 'Comment'])
master_data.drop(['Tournament', 'Wsets', 'Lsets'], axis = 1, inplace = True)
master_data['d_rank'] = master_data['WRank'] - master_data['LRank']
master_data['d_elo'] = master_data['elo_winner'] - master_data['elo_loser']

## ----- Creating Modelling Data ----- ##
master_w = master_data
master_w = master_w.drop(['Loser', 'LRank', 'PSL', 'B365L', 'elo_loser'], axis = 1, inplace = False)
master_w = master_w.rename(columns = {"Winner": "Player", "WRank": "Rank", "PSW": "PS", "B365W":"B365", "elo_winner":"elo"})
master_w['win_loss'] = 1

master_l = master_data
master_l = master_l.drop(['Winner', 'WRank', 'PSW', 'B365W', 'elo_winner'], axis = 1, inplace = False)
master_l = master_l.rename(columns = {"Loser": "Player", "LRank": "Rank", "PSL": "PS", "B365L":"B365", "elo_loser":"elo"})
master_l['proba_elo'] = 1 - master_l['proba_elo']
master_l['win_loss'] = 0

modelling_data = master_w.append(master_l)
modelling_data.to_csv("C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Generated Data/modelling_data.csv", index = False)