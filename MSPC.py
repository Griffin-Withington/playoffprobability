
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics as sts

import warnings
warnings.filterwarnings('ignore')

############################

#     WEIGHTING PROCESSS




# Weighting Weekly results with recency bias

# relative weight set to model sigma equation:
# 1/(1+e^-t) where t = 4 - (most recent week - weighted week)/2


# takes integer current_week and returns a dictionary 
# mapping each week to weighting

def weighting(comp_weeks):
    
    weights = {}
    all_weights = []
    
    for week in range(1, comp_weeks + 1):
        weeks_back = comp_weeks - week
        t = 4 - weeks_back/2.0
        rel_weight = 1/(1 + math.exp(-t))
        all_weights.append(rel_weight)
        weights[week] = rel_weight
   
    total_weight = sum(all_weights)
    check = 0
    
    for week in range(1, comp_weeks + 1):
        weights[week] = weights[week]/total_weight
        check += weights[week]
    if check > .99 and check <1.01:
        return weights
    else: 
        print("weights not close enough to 1")
    
        


#print(weighting(12))



#
#
#
# FOR PLOTTING IF SO INCLINED
#
# 
    
# WEIHGTING PROCESS COMPLETE

######################################

       
              
                     
#######################################

# WEIGHTED MEAN AND STANDARD DEVIATION

 ######  AKA ELO SCORE
 


# The function elo_score takes in a LIST of scores received
# in the season and returns a tuple with elo rating and volitility
# (Rating (weighted mean), Volility (Weighted StdDev))


##### BIG NOTE: scores list must be ordered starting with week 1


def elo_score(scores_list):
    
    # Rating (weighted mean)
    
    w_mean = 0
    weeks = len(scores_list)
    weights = weighting(weeks)
    for week in range(0, weeks):
        w_mean += (scores_list[week] * weights[week + 1])
   
   
    # Volitility (weighted StdDev)
    
    summation = 0
    for week in range(0, weeks):
        summation += ((scores_list[week] - w_mean)**2) * weights[week + 1]
       
    
    variance = summation * (weeks/(weeks - 1))
    w_stddev = math.sqrt(variance)
   
   
    return (w_mean, w_stddev)                                               

#sample_scores = [100, 90, 100, 100, 100, 100, 100]                                   
#print(elo_score(sample_scores))                                                                                                      
                                     
                                                 

# ELO SCORES DONE

###########################################

                                                                                                                                                                                                                                                
###########################################



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
def gen_scores(elo, comp_weeks):
    
    # GENERATES SCORES FOR REST OF UNPLAYED WEEKS FROM A 
    #     NORMAL DISTRIBUTION CENTERED AROUND ELO SCORE AND ELO VOLITILITY
    
    scores = np.random.normal(elo[0], elo[1], 16-comp_weeks)
    return scores


df = pd.read_csv("fftest.csv")

#print(df) TEST


def get_comp_weeks(dataframe):
    
    # QUICK FUNCTION TO GRAB UNPLAYED WEEKS BY COUNTING NULL VALUES IN A COLUMN
    
    left = max(df.apply(lambda x: sum(x.isnull())))
    comp = 16 - left
    return comp
    
    
#get_comp_weeks(df) TEST


def sim_scores(dataframe):
    
    # USES ELO_SCORE AND GEN_SCORES FUNCTIONS ABOVE TO FILL OUT A SEASON WITH
    #   SIMULATED SCORES
    
    comp_weeks = get_comp_weeks(dataframe)
    
    for column in dataframe:
        if "pts" in column:
        #select the first "comp_weeks" many as a list to generate elo
            elo = elo_score(dataframe[column].iloc[0:comp_weeks].tolist()) 
            scores = gen_scores(elo, comp_weeks)
            for week in range(comp_weeks, 16):
                dataframe[column][week] = round(scores[week - comp_weeks],1)
    return dataframe
            
            
#########################################    
# CODING MATCHUPS 

#print(sim_scores(df)) TEST


teams =  ['G', 'X', 'M', 'D', 'T', 'C', 'J', 'A']   # DATA SPECIFIC TO MSPC LEAGUE
d1 = ['G', 'X', 'M', 'D']                           #   USED FOR TESTING PROGRAM

 
 
def eval_season(fulldf, division1, bl):
    
    # TAKES IN A SEASON, AS WELL AS TEAM NAMES, DIVISIONS
    # AND RETURNS A DATAFRAME WITH THE FORMAT:
   
    #                teamID(*)    Wins    Pts  Playoffs  Div
    #                   .           .      .       .      .  
    
    if bl == "full":
        wk = 14
    else:
        wk = get_comp_weeks(fulldf)
    regdf = fulldf.iloc[0:wk]
    tms = {}
    for column in regdf:
        if "pts" in column:
            team = column[0]
            team_wins = 0
            if team in division1:
                div = 1
            else:
                div = 2
            for week in range(0, wk):
                if regdf[column][week] > regdf[str(regdf[str(team) + " opp"][week]) + " pts"][week]:
                    team_wins += 1.0
                elif regdf[column][week] == regdf[str(regdf[str(team) + " opp"][week]) + " pts"][week]:
                    team_wins += 0.5                
            tms[team] = [team_wins,round(regdf[column].sum(), 1), None, div]
    playoff_teams = pd.DataFrame(tms, index = ["Wins", "Pts", "Playoffs", "Div"]).T
    season_results = playoff_teams.sort_values(["Wins", "Pts"], ascending = False)
    if season_results["Div"].iloc[0] == season_results["Div"].iloc[1] == season_results["Div"].iloc[2] == season_results["Div"].iloc[3]:
        season_results["Playoffs"].iloc[0:3] = 1
        season_results["Playoffs"].iloc[4] = 1
    else:
        season_results["Playoffs"].iloc[0:4] = 1
    season_results["Playoffs"].fillna(0, inplace = True)
    return season_results


#print(eval_season(df, d1, "no"))   TEST
    
############################################33

    
def simulate(seasons, watch, fle, teams, div):
    
    
    

    df = pd.read_csv(fle)
    
    comp_weeks = get_comp_weeks(df)
    cur_wins = eval_season(df, div, "no")
    team_results = {}
    
    for team in teams:
        team_results[team] = [[],None, [],[], None, None, None]   
        team_results[team][1] = round(elo_score(df[team + " pts"].iloc[0:comp_weeks].tolist())[0],1)
        team_results[team][4] = str(int(cur_wins["Wins"][team])) + " - " + str(int(comp_weeks - cur_wins["Wins"][team]))
        team_results[team][5] = cur_wins["Div"][team]
        team_results[team][6] = round(elo_score(df[team + " pts"].iloc[0:comp_weeks].tolist())[1],2)
    for season in range(1, seasons+1):
        while watch not in ["yes", "no"]:
            watch = input("Please type yes or no, all lower case, no quotation marks   ")
        if watch == "yes":
            print("Season " + str(season) + " simulating")    
        copy = df.copy()
        fulldf = sim_scores(copy)
        sim = eval_season(fulldf, div, "full")
        for team in team_results:
            team_results[team][0].append(sim["Wins"][team])
            team_results[team][2].append(sim["Pts"][team])
            team_results[team][3].append(sim["Playoffs"][team])
    team_result = {}
    for team in team_results:
        team_result[team] = [[],[],[],[],[],[],[],[]]    
        team_result[team][0] = round(sts.mean(team_results[team][0]), 1)
        team_result[team][1] = team_results[team][1]
        team_result[team][2] = team_results[team][6]
        team_result[team][3] = round(sts.mean(team_results[team][2]), 0)
        team_result[team][4] = round(sts.stdev(team_results[team][2]), 0)
        team_result[team][5] = str(round(100*sum(team_results[team][3])/seasons, 1)) + "%"
        team_result[team][6] = team_results[team][4]
        team_result[team][7] = team_results[team][5]

        table = pd.DataFrame(team_result, index = ["Exp. Wins", "Elo Score", "Elo Vol", "Exp Ttl Pts", "Var of Ttl Pts", "Playoff Prob", "Record", "Division"]).T
        srttable = table.sort_values(["Exp. Wins", "Playoff Prob"], ascending = False)
    return srttable


# SO ENDS THE PROGRAM BODY
#################################################

# THE FOLLOWING FUNCTIONS ORGANIZE THE DATA TO BE PRESENTED 
# IN THE CONTEXT OF THE MICHAEL SCOTT PAPER COMPANY FANTASY FOOTBALL LEAGUE


    
    
def MSPC(table):
    # Reads in pandas dataframe given from simulate and inserts team names, current records, divisions
    table["Team"] = None
    table["Team"]['T'] = "Knights of the Night"
    table["Team"]['G'] = "Little Kid Lovers"
    table["Team"]['J'] = "Quad Desk"
    table["Team"]['X'] = "How the Turned Tables"
    table["Team"]['M'] = "Voodoo Mama Juju"
    table["Team"]['C'] = "Threat Level Midnight"
    table["Team"]['A'] = "Born on a Beach"
    table["Team"]['D'] = "Hypothetical Camping Trip"

    for team in range(0, 8):
        if table["Division"].iloc[team] == 1:
            table["Division"].iloc[team] = "Office"
        else:
            table["Division"].iloc[team] = "Warehouse"

        
    cols = table.columns.tolist()
    cols = cols[-1:] + cols[-2:-1] + cols[1:2] + cols[-3:-2] + cols[:1] + cols[-4:-3] 
    table = table[cols]
    return table
    


    
def MSPC_elo(table):
    table["Team"] = None
    table["Team"]['T'] = "Knights of the Night"
    table["Team"]['G'] = "Little Kid Lovers"
    table["Team"]['J'] = "Quad Desk"
    table["Team"]['X'] = "How the Turned Tables"
    table["Team"]['M'] = "Voodoo Mama Juju"
    table["Team"]['C'] = "Threat Level Midnight"
    table["Team"]['A'] = "Born on a Beach"
    table["Team"]['D'] = "Hypothetical Camping Trip"
    
    cols = table.columns.tolist()
    cols = cols[-1:] + cols[-2:-1] + cols[1:2] + cols[2:3]
    table = table[cols]
    return table   
    
    
    
    
 
sims = int(input("How many simulations would you like to run? (recommended 20,000 maximum)   "))
wch = input("Would you like to view the current simulation count while running? (type yes or no)(runs ~20% faster if no)   ")
tb = simulate(sims, wch, "fftest.csv", teams, d1)    
        
                
print(MSPC(tb))   
        
          
    
print(MSPC_elo(tb))    
    
    
    
    
    