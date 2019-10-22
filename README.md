# playoffprobability
# A playoff probability generation engine for the MSPC Fantasy Football League


DESCRIPTION:

This program generates playoff probability measures for each team in my fantasy football league.

The program creates elo scores for each team, giving future expected scores and standard deviation
based on a recency-biased weighted average of previous scores.

Using normal distributions around each team's "elo score", the program repeatedly simulates the remainder of the season
a large, user-chosen, number of times (10,000-20,000 simulations recommended) and spits out the synthesized results
of these simulations, including each team's frequency of reaching the playofffs.



RUNNING THE PROGRAM:


The main program, MSPC.py, is entirely python code, with Pandas and Numpy importations, 
and is meant to be run in the terminal.

The file fftest.csv must be downloaded in concert, as MSPC.py will read in the csv data.




*NOTE: as the season has not yet begun, fftest.csv contains arbitrary, fake scores for testing purposes. 
When the season has progressed enough for meaningful data to be collected, fftest.csv will be replaced by 
MSPC.csv, an identically-formatted csv file containing the actual scores from the league.
