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

def ols(x, y):
    model = LinearRegression().fit(x, y)
    print(model.score(x, y))
    return

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
    
    print(df.head())
    
    # Check for evidence of correlation
    scatter(df['score'], df['new_cases_pc'],\
            'Reopening Score (x) vs. New Cases per Capita (y)')
    
    scatter(df['score'], df['total_cases_pc'],\
            'Reopening Score (x) vs. Total Cases per Capita (y)')
        
    # Perform fixed effects regression

    
    #ols(np.array(df['score']).reshape(-1, 1), df['total_cases_pc'])





      
main()
        