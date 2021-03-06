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
    This function serves as the first step in scraping a webpage by creating
    a soup object of the website text.
    
    Parameters
    ----------
    url : string
        url of webpage to scrape

    Returns
    -------
    soup : beautiful soup object
        bs object that contains webpage data

    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup
            
def get_array(soup):
    """
    This function converts the soup object into a usable numpy array.
    
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
    This function is the final step in webscraping as it converts the array
    into a dataframe.

    Parameters
    ----------
    array : numpy array
        website table data as array
    colnames : list of strings
        names of columns/variables in table
    n : int
        column number on which to split dataaframe

    Returns
    -------
    df_final : pandas dataframe
        website table data as df
    """
    df = pd.DataFrame(data=array, columns=colnames)
    df.drop([0], inplace = True)   # col names are also stored as first row
    df1 = df.iloc[:, 0:n]
    df2 = df.iloc[:, n:]
    df_final = pd.concat([df1, df2])
    return df_final

def scrape_to_df(url, n):
    """
    This function serves as a wrapper, as it calls the helper functions necessary
    to scrape a url.

    Parameters
    ----------
    url : string
        url of webpage to scrapte
    n : int
        number of columns to split array on

    Returns
    -------
    df : pandas dataframe
        information scraped from webpage stored as a df

    """
    soup = make_soup(url)
    array = get_array(soup)
    col_names = array[0]
    df = array_to_df(array, col_names, n)
    return df

def add_date(df, last_update):
    """
    This script scrapes data from a webpage that is updated regularly. This 
    function adds a column to the final dataframe that indicates the date on
    which the webpage was scraped.

    Parameters
    ----------
    df : pandas dataframe
        dataframe created from website data
    last_update : string
        date the website was last updated at the time that this script was run

    Returns
    -------
    df : pandas dataframe
        dataframe created from website data that now includes a date

    """
    dates = [last_update]*len(df)
    df['updated_on'] = dates
    return df

def main():
    # Retrieve COVID-19 reopening data from webpage
    rank_url = 'https://www.multistate.us/issues/covid-19-state-reopening-guide'
    rank_df = scrape_to_df(rank_url, 3)
    
    # Add date of last update at time of scrape
    last_update = '3/4/21'
    rank_df = add_date(rank_df, last_update)
    
    # Save to repository
    # path = Path.cwd()
    # f_save = path.joinpath('COVID Reopening Ranks.csv')
    # rank_df.to_csv(f_save)
    
main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    