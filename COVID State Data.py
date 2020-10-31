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
    df['id'] = df.index
    df_reshaped = pd.wide_to_long(df, stubnames = stubnames, i = 'id', j = j,\
                                  sep = ' ').reset_index()
    df_reshaped.drop(columns = ['id'], inplace = True)    # drop id column
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
    df = pd.DataFrame(data = array, columns = colnames)
    df.drop([0], inplace = True)   # col names are also stored as first row
    df1 = df.iloc[:, 0:n]
    df2 = df.iloc[:, n:]
    df_final = pd.concat([df1, df2])
    return df_final

def main():
    ## load and manipulate data
    df = csv_df('COVID Case Data.csv', 23)
    df = reshape(df, ['TOTAL CASES', 'BLACK CASES', 'HISPANIC CASES', 'WHITE CASES',\
                      'BLACK IR', 'HISPANIC IR', 'WHITE IR'], 'DATE')
    df = format_date(df, 'DATE')
    
    ## scrape and shape web data
    rank_soup = make_soup('https://www.multistate.us/issues/covid-19-state-reopening-guide',\
                           {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'})
    check_soup(rank_soup, ['COVID-19 State Reopening Guide', 'Ratings', 'Methodology',\
                         'Molly'])     # should print yes, yes, yes, no
    rank_array = get_array(rank_soup)
    colnames = ['Rank', 'State', 'Reopening Plan', 'Score', 'Rank', 'State',\
                'Reopening Plan', 'Score']
    df_rank = array_to_df(rank_array, colnames, 4)
    print(df_rank.head())

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    