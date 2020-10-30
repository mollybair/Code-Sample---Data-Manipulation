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

def main():
    ## load and manipulate data
    df = csv_df('COVID Case Data.csv', 23)
    df = reshape(df, ['TOTAL CASES', 'BLACK CASES', 'HISPANIC CASES', 'WHITE CASES',\
                      'BLACK IR', 'HISPANIC IR', 'WHITE IR'], 'DATE')
    df = format_date(df, 'DATE')
    
    print(df.head())
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    