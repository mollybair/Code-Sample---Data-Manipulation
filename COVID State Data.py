#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:34:00 2020

@author: mollybair
"""
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt

def make_soup(url):
    """
    Parameters
    ----------
    url : url of website to scrape
    Returns
    -------
    soup : Beautiful Soup object
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup
            
def get_array(soup):
    """
    Parameters
    ----------
    soup : BeautifulSoup object
        soup object created from a website that has a table
    Returns
    -------
    array: numpy array
        returns data in website table in array format
    """
    table = soup.find('table')
    array = []
    for row in table.find_all('tr'):
        temp = []
        for cell in row.find_all(['th', 'td']):
            temp.append(cell.text)
        array.append(temp)
    return np.array(array)

def array_to_df(array, colnames, n):
    """
    Parameters
    ----------
    array : array to be converted to pandas df
    colnames : dataframe column names
    n : col number on which to split dataframe
        the array was created from a table with repeating columns; it is essentially
        two identical dataframes side by side; want them instead to be stacked vertically
    Returns
    -------
    df_final : pandas dataframe
    """
    df = pd.DataFrame(data=array, columns=colnames)
    df.drop([0], inplace = True)   # col names are also stored as first row
    df1 = df.iloc[:, 0:n]
    df2 = df.iloc[:, n:]
    df_final = pd.concat([df1, df2])
    return df_final

def join_to_panel(df1, df2, id_col, new_col, stubnames, j):
    """
    Parameters
    ----------
    df1 : main dataframe
    df2 : secondary dataframe
    id_col : col name, present in both dataframes, that identifies observations
    new_col : col name of new col being added to df1 from df2
    stubnames : stubnames
    j : identifying variable for reshape
    Returns
    -------
    df_panel : joined panel dataframe
    """
    df2[id_col] = [obs.upper() for obs in list(df2[id_col])]
    df2 = df2[df2[id_col].isin(list(df1[id_col]))]
    df1 = df1.sort_values(by=[id_col])
    df2 = df2.sort_values(by=[id_col])
    df1[new_col] = list(df2[new_col].str.strip('()').astype(int))
    df_panel = pd.wide_to_long(df1, stubnames=stubnames, i=[id_col, new_col], j=j,\
                                  sep=' ').reset_index()
    df_panel[j] = pd.to_datetime(df_panel[j], format='%y%m%d')
    return df_panel

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

def subset_df(df, s1, val1, s2, val2, val3):
    """
    Parameters
    ----------
    df : dataframe to subset
    s1 : series
        to be filtered on one condition
    val1 : value of series
        value to keep of s1
    s2 : series
        to be filtered on two conditions
    val2 : value of series
        value to keep of s2
    val3 : value of series
        value to keep of s2
    Returns
    -------
    df : subsetted dataframe
    """
    df = df[(df[s1] == val1)]
    df = df[(df[s2] == val2) | (df[s2] == val3)]
    return df

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
    df_cases = pd.read_csv('COVID Case Data.csv', nrows=23)
    rank_soup = make_soup('https://www.multistate.us/issues/covid-19-state-reopening-guide')
    rank_array = get_array(rank_soup)
    colnames = ['RANK', 'STATE', 'Reopening Plan', 'SCORE', 'RANK', 'STATE',\
                'Reopening Plan', 'SCORE']
    df_rank = array_to_df(rank_array, colnames, 4)
    df = join_to_panel(df_cases, df_rank, 'STATE', 'RANK',\
                       ['TOTAL CASES', 'BLACK CASES', 'HISPANIC CASES', 'WHITE CASES',\
                        'BLACK CI', 'HISPANIC CI', 'WHITE CI'], 'DATE')
    closed_state, open_state = get_min_max(df, 'RANK', 'STATE')
    df_recent = subset_df(df, 'DATE', '2020-09-22', 'STATE', open_state, closed_state)
    grouped_bar([closed_state, open_state], df_recent['WHITE CI'], df_recent['BLACK CI'],\
                df_recent['HISPANIC CI'], 'White', 'Black', 'Hispanic',\
                    [closed_state, open_state], 'Cumulative Incidence by Race')   
main()
        