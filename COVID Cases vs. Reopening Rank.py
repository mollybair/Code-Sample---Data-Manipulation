#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:34:00 2020

@author: mollybair
"""
from pathlib import Path
import pandas as pd
import us
import numpy as np
import matplotlib.pyplot as plt

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

def join(df1, df2, date, match):
    df1 = df1[df1['date'] == date]
    merged = df1.merge(df2, how='inner', on=match)
    return merged

def get_min_max(df, var, target_var):
    """
    Parameters
    ----------
    df : dataframe
    var : series name
        series to get min/max index of
    target_var : series name
        series observation to locate with min/max index
    Returns
    -------
    max_val : max series obs
    min_val : min series obs
    """
    max_val = df.at[df[var].idxmax(), target_var]
    min_val = df.at[df[var].idxmin(), target_var]
    return max_val, min_val

def grouped_bar(x, y1, y2, y3, lab1, lab2, lab3, xticks, title):
    """
    Parameters
    ----------
    x : x variable
        variable bars are grouped by
    y1 : first bar in grouping
    y2 : second bar in grouping
    y3 : third bar in grouping
    lab1 : first bar label
    lab2 : second bar label
    lab3 : third bar label
    xticks : labels for xticks (bar groupings)
    title : plot title
    """
    ind = np.arange(len(x))  # x location for bar groups
    width = 0.2
    # create plot
    fig, ax = plt.subplots()
    bar1 = ax.bar(ind - 0.2, y1, width, label=lab1, color='mediumseagreen')
    bar2 = ax.bar(ind, y2, width, label=lab2, color='cornflowerblue')
    bar2 = ax.bar(ind + 0.2, y3, width, label=lab3, color='goldenrod')
    # set x ticks
    ax.set_xticks(ind)
    ax.set_xticklabels(xticks)
    # add title
    ax.set_title(title)
    ax.title.set_weight('bold')
    ax.title.set_size(16)
    ax.title.set_position([.5, 1])
    # set spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_lw(1.5)
    ax.spines['left'].set_lw(1.5)
    # misc formatting and display
    plt.legend()    
    plt.rcParams["font.family"] = "serif"
    plt.tight_layout()
    plt.show()

def main():
    path = Path.cwd()
    
    # Retrieve COVID-19 case data from csv
    cases_fname = 'COVID Tracker Project-By State.csv'
    covid_cols = ['date', 'state', 'positive', 'positiveIncrease']
    cases = csv_to_df(path, cases_fname, covid_cols)

    # Retrieve web scraped df
    rank_fname = 'COVID Reopening Ranks.csv'
    rank = csv_to_df(path, rank_fname, ['Rank', 'State', 'Score'])
    rank.columns = ['rank', 'state', 'score']
    
    # Format state columns (both should be full state name)
    cases = format_state(rank, cases, 'state')
    
    print(cases.head())
    print(rank.head())
    
    # Join cases and ranks
    df = join(cases, rank, '3/4/21', 'state')
    print(df.head())
    
    
    # df = join_to_panel(df_cases, df_rank, 'STATE', 'RANK',\
    #                    ['TOTAL CASES', 'BLACK CASES', 'HISPANIC CASES', 'WHITE CASES',\
    #                     'BLACK CI', 'HISPANIC CI', 'WHITE CI'], 'DATE')
    # closed_state, open_state = get_min_max(df, 'RANK', 'STATE')
    # df_recent = subset_df(df, 'DATE', '2020-09-22', 'STATE', open_state, closed_state)
    # grouped_bar([closed_state, open_state], df_recent['WHITE CI'], df_recent['BLACK CI'],\
    #             df_recent['HISPANIC CI'], 'White', 'Black', 'Hispanic',\
    #                 [closed_state, open_state], 'Cumulative Incidence by Race')   
main()
        