# playoffprobability
# A playoff probability generation engine for the MSPC Fantasy Football League


DESCRIPTION:


The folling sites are the inspiration for this project:


###########

https://www.fangraphs.com/standings/playoff-odds

https://projects.fivethirtyeight.com/2019-mlb-predictions/

http://mlb.mlb.com/mlb/standings/probability.jsp

###########


These site pages estimate the current probability of each Major League Baseball team 
finishing in the league's top third, and reaching the league playoffs.

I created the same concept for my fantasy football league.

The program creates elo scores for each team, giving future expected scores and standard deviation
based on a recency-biased weighted average of previous scores.

Using normal distributions around each team's "elo score", the program repeatedly simulates the remainder of the season
a large, user-chosen, number of times (10,000-20,000 simulations recommended) and spits out the synthesized results
of these simulations, including each team's frequency of reaching the playofffs.



RUNNING THE PROGRAM:


For now, the program is entirely python code, with Pandas and Numpy importations, 
and is meant to be run in the terminal.

The file fftest.csv must be downloaded in concert, as MSPC.py will read in the csv data.




*NOTE: as the season has not yet begun, fftest.csv contains arbitrary, fake scores for testing purposes. 
When the season has progressed enough for meaningful data to be collected, fftest.csv will be replaced by 
MSPC.csv, an identically-formatted csv file containing the actual scores from the league.
