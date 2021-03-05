#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 13:43:34 2021

@author: mollybair
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
from pathlib import Path

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

def scrape_to_df(url, n):
    soup = make_soup(url)
    array = get_array(soup)
    col_names = array[0]
    df = array_to_df(array, col_names, n)
    return df

def main():
    # Retrieve COVID-19 reopening data from webpage
    rank_url = 'https://www.multistate.us/issues/covid-19-state-reopening-guide'
    rank_df = scrape_to_df(rank_url, 3)
    
    path = Path.cwd()
    f_save = path.joinpath('COVID Reopening Ranks.csv')
    rank_df.to_csv(f_save)
    
main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    