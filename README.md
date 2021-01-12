# Python Code Sample - Data Manipulation

This code sample creates and joins two pandas dataframes--one from a csv file
and another from scraping a website. The first dataframe, df_cases, has data on 
COVID-19 cases for a number of states. For each state, the following counts are 
recorded on each collection date: total cases, white cases, Black cases, 
Hispanic cases, white cumulative incidence, Black cumulative incidence, and 
Hispanic cumulative incidence. The second dataframe, df_rank, contains each 
state's rank based on their COVID-19 reopening plan. While perhaps counterintuitive, 
a lower rank means the state is more open. 

The resulting panel dataframe is used to create a visualization that compares the
cumulative incidences for each racial group in the most open state (Florida) and in
the most closed state (California). In both states, the white cumulative incidence
is lowest and the Hispanic cumulative incidence is highest. However, all three
racial groups experience much higher cumulative incidences in Florida than they
do in California. This indicates ithat a stricter reopening policy likely inhibits
the spread of COVID-19. 

A limitation of this analysis is that the state reopening ranks were last updated
on October 30, 2020 whereas the most recent wave of case data is from September
22, 2020. 
