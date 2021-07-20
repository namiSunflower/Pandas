import pandas as pd # Our data manipulation library
import numpy as np
import seaborn as sns # Used for graphing/plotting
import matplotlib.pyplot as plt # If we need any low level methods
import os # Used to change the directory to the right place

master = pd.read_csv("nba_basketball_data/basketball_master.csv")
awards = pd.read_csv("nba_basketball_data/basketball_awards_players.csv")
nba = pd.merge(awards, master, how="left", left_on="playerID", right_on="bioID")
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)

nba["name"]= nba['firstName'].astype(str)+' '+nba['lastName']

#Remove all these columns
nba = nba[nba.award != "All-ABA First Team"]
nba = nba[nba.award != "All-ABA Second Team"]
nba = nba[nba.award != "Comeback"]
nba = nba[nba.award != "Executive of the Year"]
nba = nba[nba.award != "Most Improved Player"]
nba = nba[nba.award != "J. Walter Kennedy Citizenship Award"]
nba = nba[nba.award != "Sportsmanship Award"]
nba = nba[nba.award != "All-Rookie First Team"]
nba = nba[nba.award != "All-Rookie Second Team"]
nba = nba[nba.award != "Sixth Man of the Year"]

#Create a pivot table that will count each player's number of awards by each category
numberOfAwards = (nba.pivot_table(index='name',columns='award', aggfunc='size', fill_value=0))
#renames Most Valuable Player column to MVP
numberOfAwards=numberOfAwards.rename(columns = {'Most Valuable Player':'MVP'})
#This formula for All-NBA Team and All Defensive Team is based on several NBA awards statistics
numberOfAwards["All-NBA Team"] = numberOfAwards["All-NBA First Team"] + numberOfAwards["All-NBA Second Team"] + numberOfAwards["All-NBA Third Team"]
numberOfAwards["All Defensive Team"] = numberOfAwards["All-Defensive First Team"] + numberOfAwards["All-Defensive Second Team"]
print(numberOfAwards[["All-NBA Team"]].sort_values("All-NBA Team", ascending=False).head(10))
print(numberOfAwards[["All Defensive Team"]].sort_values("All Defensive Team", ascending=False).head(10))
print(numberOfAwards[["MVP"]].sort_values("MVP", ascending=False).head(10))
print(numberOfAwards[["Finals MVP"]].sort_values("Finals MVP", ascending=False).head(10))
numberOfAwards = numberOfAwards[numberOfAwards["Rookie of the Year"] > 0]
print(numberOfAwards[["Rookie of the Year"]].sort_values("Rookie of the Year", ascending=False))
numberOfAwards = numberOfAwards[numberOfAwards["Defensive Player of the Year"] > 0]
print(numberOfAwards[["Defensive Player of the Year"]].sort_values("Defensive Player of the Year", ascending=False))

nba2 = nba
nba2 = nba2.query('name == "Michael Jordan"')
mj = (nba2.pivot_table(index='name',columns='award', aggfunc='size', fill_value=0))
mj = mj.rename(columns = {'Most Valuable Player':'MVP'})
#Had to adjust the formula since he has never received an ALL-NBA Third Team and an All-Defensive Second Team award.
mj["All-NBA Team"] = mj["All-NBA First Team"] + mj["All-NBA Second Team"]
mj["All Defensive Team"] = mj["All-Defensive First Team"]
print("Michael Jordan's No. of Awards")
print(mj[["All-NBA Team", "All Defensive Team", "MVP", "Finals MVP", "Rookie of the Year", "Defensive Player of the Year"]])

nba3 = nba
nba3 = nba3.query('name == "Wilton Chamberlain"')
wc = (nba3.pivot_table(index='name',columns='award', aggfunc='size', fill_value=0))
wc = wc.rename(columns = {'Most Valuable Player':'MVP'})
wc["All-NBA Team"] = wc["All-NBA First Team"] + wc["All-NBA Second Team"]
wc["All Defensive Team"] = wc["All-Defensive First Team"]
print("Wilton Chamberlain's No. of Awards")
print(wc[["All-NBA Team", "All Defensive Team", "MVP", "Finals MVP", "Rookie of the Year"]])



