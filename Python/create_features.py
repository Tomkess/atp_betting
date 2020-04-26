#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import multiprocessing

## ----- Set files locations ----- ##
modelling_loc = "C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Generated Data/modelling_data.csv"
features_loc = "C:/Users/Peter.Tomko/OneDrive - 4Finance/concept/ATPBetting/Generated Data/atp_data_features.csv"

## ----- FEATURES BASED ON THE PAST OF THE PLAYERS ----- ##
def features_past(data_input, last_n, date_input, player_name):
    """
    Input - modelling data
    Output - features
    
    Description: Creates features based on the past of the players. 
    Basically a for loop. Takes 1 match at a time, selects the matches that occurred during 
    its close past and computes some features.
    """
    
    # data_input = modelling_data
    # last_n = (10, 15, 20, 25, 30, 35, 40, 45, 50)
    # feature_names_prefix = 'last10_'
    # date_input = date_sel
    # player_name = player_sel
    
    # - subset data
    t_data = data_input
    t_data = t_data.sort_values('Date', ascending = False)
    
    feature_df = pd.DataFrame(columns = ['Player', 'last_n', 'm_wl', 'm_elo',
                                         'm_pelo', 'm_drank', 'm_delo',
                                         'm_rank', 'm_clay', 'm_grass', 
                                         'm_hard', 'm_carpet'])
    for j in range(0, len(last_n)):
        temp_data = t_data.head(last_n[j])
        
        if len(temp_data) < 5:
            feature_df = feature_df.append({'Player': player_name, 
                                            'last_n': 'last' + str(last_n[j]),
                                            'm_wl': 0,
                                            'm_elo': 0,
                                            'm_pelo': 0,
                                            'm_drank': 0,
                                            'm_delo': 0,
                                            'm_rank': 0,
                                            'm_clay': 0,
                                            'm_grass': 0,
                                            'm_hard': 0,
                                            'm_carpet': 0}, 
                                           ignore_index = True)
        else:
            feature_df = feature_df.append({'Player': player_name, 
                                            'last_n': 'last' + str(last_n[j]),
                                            'm_wl': temp_data['win_loss'].mean(),
                                            'm_elo': temp_data['elo'].mean(),
                                            'm_pelo': temp_data['proba_elo'].mean(),
                                            'm_drank': temp_data['d_rank'].mean(),
                                            'm_delo': temp_data['d_elo'].mean(),
                                            'm_rank': temp_data['Rank'].mean(),
                                            'm_clay': temp_data['Surface_Clay'].mean(),
                                            'm_grass': temp_data['Surface_Grass'].mean(),
                                            'm_hard': temp_data['Surface_Hard'].mean(),
                                            'm_carpet': temp_data['Surface_Carpet'].mean()}, 
                                           ignore_index = True)
    
    feature_temp = feature_df.melt(id_vars = ['Player', 'last_n'])
    feature_temp['var_name'] = feature_temp['last_n'].str.cat(feature_temp['variable'], sep = "_")
    feature_temp.drop(['last_n', 'variable'], axis = 1, inplace = True)
    
    feature_vector = feature_temp.pivot(index = 'Player', columns = 'var_name', values = 'value')
    feature_vector = feature_vector.reset_index(drop = True)
    feature_vector['Player'] = player_name
    feature_vector['Date'] = date_input

    return feature_vector

def var_calc(i_input):
    # for i in range(0, len(unique_matches)):
    # - i = 10000
    
    player_sel = unique_matches.iloc[i_input, 1]
    date_sel = unique_matches.iloc[i_input, 0]
    
    condition1 = modelling_data.Player == player_sel
    condition2 = modelling_data.Date < date_sel
    
    modelling_temp = modelling_data[condition1 & condition2]
    
    # - calculate feature vector
    features_data = features_past(data_input = modelling_temp, 
                                  last_n = (10, 15, 20, 25, 30, 40, 45, 50), 
                                  date_input = date_sel, 
                                  player_name = player_sel)
    return pd.DataFrame(features_data)

modelling_data = pd.read_csv(modelling_loc)
unique_matches = modelling_data[['Date', 'Player']].drop_duplicates()

def handler():
    p = multiprocessing.Pool(6)
    r = p.map(var_calc, range(0, len(unique_matches)))
    return r

out = None
if __name__ == '__main__':
    out = pd.concat(handler()).reset_index(drop = True)
    out.to_csv(features_loc, index = False)