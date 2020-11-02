#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:34:00 2020

@author: mollybair
"""

import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt

def csv_df(filename, nrows):
    """
    Parameters
    ----------
    filename : name of csv file
    nrows: number of rows to read from file

    Returns
    -------
    df : pandas dataframe
    """
    df = pd.read_csv(filename, nrows = nrows)
    return df

def reshape(df, stubnames, j):
    """
    Parameters
    ----------
    df : pandas dataframe
    stubnames : stubnames
    j : identifying variable

    Returns
    -------
    df_reshaped : long pandas dataframe
    """
    df_reshaped = pd.wide_to_long(df, stubnames = stubnames, i = ['STATE', 'RANK'], j = j,\
                                  sep = ' ')
    return df_reshaped

def format_date(series):
    """
    Parameters
    ----------
    df : pandas pataframe
    col_name : name of date col
    Returns
    -------
    df : pandas dataframe
        date col has been reformatted as MM/DD instead of MMDD
    """
    new_series = []
    for i in series:
        i = str(i)
        new = i[0] + '/' + i[1:]
        new_series.append(new)
    return new_series

def make_soup(url, headers):
    """
    Parameters
    ----------
    url : url of website to scrape
    headers : TYPE
        DESCRIPTION.
        
    Returns
    -------
    soup : Beautiful Soup object
    """
    response = requests.get(url, headers = headers)
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
    df = pd.DataFrame(data = array, columns = colnames)
    df.drop([0], inplace = True)   # col names are also stored as first row
    df1 = df.iloc[:, 0:n]
    df2 = df.iloc[:, n:]
    df_final = pd.concat([df1, df2])
    return df_final

def join(df1, df2, id_col, new_col):
    """
    Parameters
    ----------
    df1 : first dataframe to join
    df2 : second dataframe to join
    id_col : col name, present in both dataframes, that identifies observations
    new_col : col name of new col being added to df1 from df2
    Returns
    -------
    df_merged : joined dataframe
    """
    df2.reset_index(inplace = True)
    counter = 0
    for state in df2[id_col]:
        if state.upper() not in list(df1[id_col]):
            df2 = df2.drop([counter])
        counter += 1 
    df1 = df1.sort_values(by = [id_col])
    df2 = df2.sort_values(by = [id_col])
    col = []
    for i in df2[new_col]:
        i = i.strip('()')
        col.append(int(i))
    df_merged = df1
    df_merged[new_col] = col
    return df_merged

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
    bar1 = ax.bar(ind - 0.2, y1, width, label = lab1, color = 'mediumseagreen')
    bar2 = ax.bar(ind, y2, width, label = lab2, color = 'cornflowerblue')
    bar2 = ax.bar(ind + 0.2, y3, width, label = lab3, color = 'goldenrod')
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
    ## load data
    df_cases = csv_df('COVID Case Data.csv', 23)
    ## scrape and shape web data
    rank_soup = make_soup('https://www.multistate.us/issues/covid-19-state-reopening-guide',\
                           {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'})
    rank_array = get_array(rank_soup)
    colnames = ['RANK', 'STATE', 'Reopening Plan', 'SCORE', 'RANK', 'STATE',\
                'Reopening Plan', 'SCORE']
    df_rank = array_to_df(rank_array, colnames, 4)
    df_rank = df_rank.drop(columns = 'Reopening Plan')
    ## merge df_cases and df_rank
    df = join(df_cases, df_rank, 'STATE', 'RANK')
    df = reshape(df, ['TOTAL CASES', 'BLACK CASES', 'HISPANIC CASES', 'WHITE CASES',\
                      'BLACK CI', 'HISPANIC CI', 'WHITE CI'], 'DATE')
    df.reset_index(inplace = True)
    df['DATE'] = format_date(df['DATE'])
    ## create visualization to show relationship between cumulative incidence and reopening
    ## rank, for 2 most open states and 2 most closed states for most recent wave of data
    open_state = df.at[df['RANK'].idxmin(), 'STATE']
    closed_state = df.at[df['RANK'].idxmax(), 'STATE']
    df_recent = df[(df['DATE'] == '9/22')]
    df_recent = df_recent[(df_recent['STATE'] == open_state) | (df_recent['STATE'] == closed_state)]
    grouped_bar([closed_state, open_state], df_recent['WHITE CI'], df_recent['BLACK CI'],\
                df_recent['HISPANIC CI'], 'White', 'Black', 'Hispanic',\
                    [closed_state, open_state],'Cumulative Incidence by Race')   
main()
        