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
    # df['id'] = df.index
    df_reshaped = pd.wide_to_long(df, stubnames = stubnames, i = ['STATE', 'RANK'], j = j,\
                                  sep = ' ')
    # df_reshaped.drop(columns = ['id'], inplace = True)    # drop id column
    return df_reshaped

def format_date(df, col_name):
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
    for i in df[col_name]:
        i = str(i)
        new = i[0] + '/' + i[1:]
        df.replace({int(i):new}, inplace = True)
    return df

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

def check_soup(soup, strings):
    """
    Parameters
    ----------
    soup : Beautiful Soup object
        DESCRIPTION.
    strings : list of strings
        contains string that should be in the soup object and strings that
        should not be in the soup object

    Returns
    -------
    None.
    """
    for string in strings:
        if string in soup.text:
            print('Yes, this soup object contains the string "' + string + '"')
        else:
            print('No, this soup object does not contain the string "' + string + '"')
            
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
    # df_merged.reset_index(inplace = True)
    return df_merged

def multi_scatter(df, x, y_list, colors, labels, title, ylabel, save_as):
    fig, ax = plt.subplots()
    counter = 0
    for y in y_list:
        ax.plot(df[x], df[y], color = colors[counter],\
                label = labels[counter], linewidth = 1)
        counter += 1
    plt.rcParams["font.family"] = "serif"
    ax.set_title(title)
    ax.title.set_weight('bold')
    ax.title.set_size(14)
    ax.title.set_position([.5, 1.05])
    ax.set_ylabel(ylabel)
    ylab = ax.yaxis.get_label()
    ylab.set_size(10)
    plt.xticks(rotation = 45)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_lw(1.5)
    ax.spines['left'].set_lw(1.5)
    plt.legend()
    plt.tight_layout()
    myfig = plt.gcf()
    plt.show()
    myfig.savefig(save_as, dpi = 1000)

def main():
    ## load and manipulate data
    df_cases = csv_df('COVID Case Data.csv', 23)
    
    ## scrape and shape web data
    rank_soup = make_soup('https://www.multistate.us/issues/covid-19-state-reopening-guide',\
                           {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'})
    # check_soup(rank_soup, ['COVID-19 State Reopening Guide', 'Ratings', 'Methodology',\
    #                      'Molly'])     # should print yes, yes, yes, no
    rank_array = get_array(rank_soup)
    colnames = ['RANK', 'STATE', 'Reopening Plan', 'SCORE', 'RANK', 'STATE',\
                'Reopening Plan', 'SCORE']
    df_rank = array_to_df(rank_array, colnames, 4)
    df_rank = df_rank.drop(columns = 'Reopening Plan')

    ## merge df_cases and df_rank
    df = join(df_cases, df_rank, 'STATE', 'RANK')
    df = reshape(df, ['TOTAL CASES', 'BLACK CASES', 'HISPANIC CASES', 'WHITE CASES',\
                      'BLACK IR', 'HISPANIC IR', 'WHITE IR'], 'DATE')
    df.reset_index(inplace = True)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    