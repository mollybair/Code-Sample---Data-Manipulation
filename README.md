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
look for evidence of correlation. These plots led me to decide to use the data
to fit a linear regression model, with the goal of predicting a state's COVID-19
total cases per capita and new daily cases per capita.

To select features, I used the backward selection method. While there are only
two features to select from (rank and score), I decided to implement backward
selection so that my code can be more easily scaled up, and so that I could 
test the effects of including state fixed effects in my models.

Total COVID-19 cases per capita is best predicted without including state fixed
effects. The mean squared error is slightly smaller without state fixed effects,
and the model is simpler. The mean squared error is 7.7913, and the model explains
12.01% of the variation in the test data. So, this model is helpful but could be
improved with the inclusion of more features.

With and without the inclusion of state fixed effects, the OLS model that uses
new cases per capita as its dependent variable results in a negative test R-squared
value. This means that the model created using the training data is bad. 
This is in accordance with the very small mean squared error in these two models, 
which may indicate underfitting. So, we do not have enough features to predict 
new COVID-19 cases per capita. 

COVID-19 case data retrieved from: https://covidtracking.com/data/
COVID-19 reopening data retrieved from: https://www.multistate.us/issues/covid-19-state-reopening-guide
Population data retrieved from: https://worldpopulationreview.com/states
