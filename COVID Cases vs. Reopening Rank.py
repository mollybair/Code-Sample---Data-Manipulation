#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:34:00 2020

@author: mollybair
"""
from pathlib import Path
import pandas as pd
import us
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

np.random.seed(100)

def csv_to_df(path, fname, cols):
    file = path.joinpath(fname)
    df = pd.read_csv(file, usecols=cols)
    return df

def format_state(full_df, abbrev_df, state_var):
    state_dict = {}
    for state_name in full_df[state_var]:
        state_abbrev = us.states.lookup(state_name).abbr
        state_dict.update({state_abbrev:state_name})
    abbrev_df[state_var] = abbrev_df[state_var].map(state_dict)
    return abbrev_df

def join(df1, df2, match):
    merged = df1.merge(df2, how='inner', on=match)
    return merged

def raw_to_rate(df, raw_vars, scale_by, rate_names):
    for i in range(len(raw_vars)):
        rates = round((df[raw_vars[i]]/df[scale_by])*100, 2)
        df[rate_names[i]] = rates
    return df

def scatter(x, y, title):
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_title(title)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_lw(1.5)
    ax.spines['left'].set_lw(1.5)
    plt.rcParams['font.family'] = 'sans-serif'

def add_dummies(df, var):
    dummies = pd.get_dummies(df[var])
    df_with_dummies = pd.concat([df, dummies], axis=1)
    return df_with_dummies

def strip_strings(df, var, strip_chars):
    formatted = []
    for value in df[var]:
        temp = value.strip(strip_chars)
        formatted.append(temp)
    df[var] = formatted
    return df

def backward_selection_helper(remaining_predictors, y):
    this_best_score = 1000
    this_best_pred = None
    remove_p = None
    for p in remaining_predictors:
        try_predictors = remaining_predictors.drop(columns=[p])
        this_score = np.mean(cross_val_score(LinearRegression(), try_predictors,\
                                             y, scoring='neg_mean_squared_error'))*-1
            
        if this_score > this_best_score:
            this_best_score = this_score
            this_best_pred = list(try_predictors.columns)
            remove_p = p

    return this_best_score, this_best_pred, remove_p

def backward_selection(all_predictors, y):
    # start with assumption that full model is best model
    best_score = np.mean(cross_val_score(LinearRegression(), all_predictors, y,\
                         scoring='neg_mean_squared_error'))*-1
    best_predictors = list(all_predictors.columns)
    
    removed = []
    
    for i in range(len(all_predictors)): # max possible iterations
        if len(removed) > 0:
            remaining_predictors = all_predictors.drop(columns=removed)
        else:
            remaining_predictors = all_predictors
        
        new_score, new_predictors, remove_p = backward_selection_helper(
            remaining_predictors, y)
        if new_score < best_score:
            best_score = new_score
            best_predictors = new_predictors
            removed.append(remove_p)
        else:
            break
    
    return best_score, best_predictors           

def ols(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,\
                                                        random_state=30)
    model = LinearRegression().fit(x_train, y_train)

    train_rsq = round(model.score(x_train, y_train), 4)
    test_rsq = round(model.score(x_test, y_test), 4)
    y_pred = model.predict(x_test)
    mse = round(mean_squared_error(y_test, y_pred), 4)
    
    return {'train r-squared':train_rsq, 'test r-squared':test_rsq, 'mse':mse}

def main():
    path = Path.cwd()
    
    # Retrieve COVID-19 case data from csv
    cases_fname = 'COVID Tracker Project-By State.csv'
    covid_cols = ['date', 'state', 'positive', 'positiveIncrease']
    cases = csv_to_df(path, cases_fname, covid_cols)

    # Retrieve web scraped df
    rank_fname = 'COVID Reopening Ranks.csv'
    rank = csv_to_df(path, rank_fname, ['Rank', 'State', 'Score', 'updated_on'])
    rank.columns = ['rank', 'state', 'score', 'date']
    
    # Format state columns (both should be full state name)
    cases = format_state(rank, cases, 'state')
    
    # Join cases and ranks
    cases = cases[cases['date'] == '3/4/21']
    df = join(cases, rank, ['state', 'date'])

    # Add column for state population, so that cases per capita can be compared
    # across states
    state_pop = csv_to_df(path, 'State Population.csv', ['State', 'Pop'])
    state_pop.columns = ['state', 'population']
    df = join(df, state_pop, 'state')
    
    # Scale cases by population
    raw_case_counts = ['positive', 'positiveIncrease']
    pc_names = ['total_cases_pc', 'new_cases_pc']
    df = raw_to_rate(df, raw_case_counts, 'population', pc_names)

    # Check for evidence of correlation
    scatter(df['score'], df['new_cases_pc'],\
            'Reopening Score (x) vs. New Cases per Capita (y)')
    
    scatter(df['score'], df['total_cases_pc'],\
            'Reopening Score (x) vs. Total Cases per Capita (y)')
        
    # Convert rank to int so it can be used in the regression model
    df = strip_strings(df, 'rank', '()')
    
    # Add state dummies to consider adding state fixed effects to model
    df_state_fe = add_dummies(df, 'state')
        
    # Perform backward selection to choose features to predict total cases per capita
    numeric_x = df.drop(columns=['date', 'state', 'total_cases_pc', 'new_cases_pc'])
    y_total = df['total_cases_pc']
    score_total, features_total = backward_selection(numeric_x, y_total)
    
    # Perform backward selection to choose features to predict new cases per capita
    y_new = df['new_cases_pc']    
    score_new, features_new = backward_selection(numeric_x, y_new)
    
    # Perform OLS with selected features
    total_pc_results = ols(df[features_total], y_total)
    print('To predict total COVID-19 cases per capita, we use the following \
          predictors and obtain the following results:')
    print('Features: ', features_total)
    print('Results: ', total_pc_results)
    print('\n')
    
    new_pc_results = ols(df[features_new], y_new)
    print('To predict new COVID-19 cases per capita, we use the following predictors\
          and obtain the following results:')
    print('Features: ', features_new)
    print('Results: ', new_pc_results)

    
main()
        