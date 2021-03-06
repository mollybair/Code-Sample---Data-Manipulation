# Python Code Sample - Data Manipulation

RQ: Can the degree of a state's openness predict that states total number of 
COVID-19 cases per capita?

This code sample uses COVID-19 case data from The COVID Tracker Project,
COVID-19 reopening data from MultiState, and population data from the World
Population Review. There are three csv files in this repository.
Notably, COVID Reopening Ranks.csv was generated from the web scraping.py
file in this repository. Currently, that csv file contains data that was last
updated on March 4, 2021. Accordingly, the COVID-19 case data, downloaded from
the url pasted below, also contains data that was last updated on March 4, 2021.
Note that running the web scraping.py file without commenting out the line that
writes the dataframe to a csv file will overwrite the current data, and thus 
the case data and rank data will have been collected on different dates. 

After cleaning and merging all three dataframes, I created scatter plots to
look for evidence of correlation. If a scatter plot indicates correlation, the
variables used to create the plot were inputted into a regression model. The goal
is to try to predict a state's COVID-19 cases per capita (either new or total)
using data on the state's reopening plan.

A scatter plot of reopening score on the x-axis and total cases per capita on
the y-axis shows a possibly linear correlation. So, I inputted these variables
in a linear regression model, and used the mean squared error and the R-squared
value to evaluate the model's performance. I decided against adding state fixed
effects to the model because doing so increased the mean squared error.

COVID-19 case data retrieved from: https://covidtracking.com/data/
COVID-19 reopening data retrieved from: https://www.multistate.us/issues/covid-19-state-reopening-guide
Population data retrieved from: https://worldpopulationreview.com/states
