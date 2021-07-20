"""
W12 Data Analysis
Frances Naomi Alido
"""
import pandas as pd # Our data manipulation library
import seaborn as sns # Used for graphing/plotting
import matplotlib.pyplot as plt # If we need any low level methods
import os # Used to change the directory to the right place

players = pd.read_csv("nba_basketball_data/basketball_players.csv")
master = pd.read_csv("nba_basketball_data/basketball_master.csv")
nba = pd.merge(players, master, how="left", left_on="playerID", right_on="bioID")
#DISPLAYS ALL THE COLUMNS FULLY
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)
#Creates a new column that displays the full name of each player
nba["name"]= nba['firstName'].astype(str) + ' ' +nba['lastName']
#Creates a new column that displays the city, state, country of the player
nba["place"] = nba['hsCity'].astype(str) + ', ' +nba['hsState'] + ', ' + nba['hsCountry']

"""
PART I
1A. Calculate the mean and median number of points scored. (In other words, each row is the amount of points a 
player scored during a particular season. Calculate the median of these values. The result of this is 
that we have the median number of points players score each season.)
"""
#Mean
mean = nba["points"].mean()
print("Mean points: {:.2f}".format(mean))
#Median
median = nba["points"].median()
print("Median points: {:.2f}".format(median))
"""
2A. Determine the highest number of points recorded in a single season. 
Identify who scored those points and the year they did so.
"""
#Max points
max = nba["points"].max()
#Just the max points for verification purposes
print("\nMax points: {}".format(max))
#Max points with player info and year
print(nba[["year", "name", "points"]].sort_values("points", ascending=False).head(1))
"""
3A. Produce a boxplot that shows the distribution of total points, total assists, and total rebounds 
(each of these three is a separate box plot, but they can be on the same scale and in the same graphic).
"""
#Create box plot for points, assists, and rebounds
sns.boxplot(data=nba[["points", "assists", "rebounds"]])
#Show the current plot
plt.suptitle("Distribution of total points, total assists, and total rebounds")
plt.show()


#This will ensure that the window won't be closed when the script is finished.
plt.show(block=False)
"""
4A. Produce a plot that shows how the number of points scored has changed over time by showing the median 
of points scored per year, over time. The x-axis is the year and the y-axis is the median number of points
among all players for that year.
"""
#Get average points per game to aggregate data for each year
nba = nba[nba.GP > 0]
nba["pointsPerGame"] = nba["points"] / nba["GP"]

#Calculate median points per year
nba_median = nba[["pointsPerGame", "year"]].groupby("year").median()
nba_median = nba_median.reset_index()
nba_median = nba_median[nba_median["pointsPerGame"] > 0].round(2)
#print(nba_median)
sns.regplot(data=nba_median, x="year", y="pointsPerGame").set_title("Median points per year")
plt.show()
plt.show(block=False)

"""
PART II
2A. Some players score a lot of points because they attempt a lot of shots. Among players that 
have scored a lot of points, are there some that are much more efficient (points per attempt) 
than others?
"""
#creates a new dataframe that'll include only all the columns needed to compute player efficiency
nbaEfficiency = nba[["year", "name", "GP", "pointsPerGame","fgMade", "threeMade", "fgAttempted", "threeAttempted", "ftMade", "ftAttempted"]]

#INCLUDES ONLY PLAYERS THAT HAVE SCORED A LOT OF POINTS PER SEASON
nbaEfficiency = nbaEfficiency[nbaEfficiency.pointsPerGame > 30]

#COMPUTES TWO POINT FIELD GOAL, THREE POINT FIELD GOAL, AND FREE THROW PERCENTAGES
#FG = FIELD GOAL
#THREE = THREE POINT FIELD GOALS
nbaEfficiency["FGPercent"] = nbaEfficiency["fgMade"] / nbaEfficiency["fgAttempted"] * 100
nbaEfficiency["threeFGPercent"] = nbaEfficiency["threeMade"] / nbaEfficiency["threeAttempted"] * 100
nbaEfficiency["FTPercent"] = nbaEfficiency["ftMade"] / nbaEfficiency["ftAttempted"] * 100



#TOTALS BOTH FG% AND 3FG% EXCLUDING FREE THROWS
#Includes both 2 & 3 point field goal shots and total attempts to measure total points per attempt more accurately
nbaEfficiency["pointsPerAttempt"] = ((nbaEfficiency["fgMade"] + nbaEfficiency["threeMade"]) / (nbaEfficiency["fgAttempted"] + nbaEfficiency["threeAttempted"]))
nbaEfficiency = nbaEfficiency[nbaEfficiency.FGPercent > 0]
nbaEfficiency = nbaEfficiency[nbaEfficiency.threeFGPercent > 0]
nbaEfficiency = nbaEfficiency[nbaEfficiency.FTPercent > 0].round(2)
nbaEfficiency = nbaEfficiency[nbaEfficiency.pointsPerAttempt > 0].round(2)

#PRINT SEASONAL RESULTS FOR FG%
print(nbaEfficiency[["year","name", "fgMade", "fgAttempted", "FGPercent"]].sort_values("FGPercent", ascending= False).head(10))

#PRINT SEASONAL RESULTS FOR 3FG%
print(nbaEfficiency[["year","name", "threeMade", "threeAttempted", "threeFGPercent"]].sort_values("threeFGPercent", ascending= False).head(10))

#PRINT SEASONAL RESULTS FT%
print(nbaEfficiency[["year","name", "FTPercent"]].sort_values("FTPercent", ascending= False).head(10))

#PRINT SEASONAL RESULTS PPT(POINTS PER ATTEMPT)
print(nbaEfficiency[["year","name", "pointsPerAttempt"]].sort_values("pointsPerAttempt", ascending= False).head(10))

"""
2B. It seems like some players may excel in one statistical category, but produce very little in other areas. 
Are there any players that are exceptional across many categories?
"""
#Gets the rest of the seasonal statistics of each player

#Seasonal rebounds per game
nba["reboundsPerGame"] = nba["rebounds"] / nba["GP"]
nba= nba[nba.reboundsPerGame >= 0].round(2)
#Seasonal assists per game
nba["assistsPerGame"] = nba["assists"] / nba["GP"]
nba= nba[nba.assistsPerGame >= 0].round(2)
#Seasonal blocks per game
nba["blocksPerGame"] = nba["blocks"] / nba["GP"]
nba[nba.blocksPerGame >= 0].round(2)

#Seasonal steals per game
nba["stealsPerGame"] = nba["steals"] / nba["GP"]
nba= nba[nba.stealsPerGame >= 0].round(2)

print(nba[["year", "name", "pointsPerGame", "assistsPerGame", "reboundsPerGame", "stealsPerGame", "blocksPerGame"]].sort_values(["assistsPerGame", "pointsPerGame", "reboundsPerGame", "stealsPerGame", "blocksPerGame"], ascending=[False, False, False, False, False]).head(10))

"""
2C. Much has been said about the rise of the three-point shot in recent years. It seems that 
players are shooting and making more three-point shots than ever. Recognizing that this 
dataset doesn't contain the very most recent data, do you see a trend of more three-point shots 
either across the league or among certain groups of players? Is there a point at 
which popularity increased dramatically?
"""
#Trends across the league
#3 points through the years

#Calculate 3 points per game
nbaEfficiency["threePointsPerGame"] = nbaEfficiency["threeMade"] / nbaEfficiency["GP"]

nbathreeFGtrends = nbaEfficiency[["threePointsPerGame", "year"]].groupby("year")["threePointsPerGame"].nlargest(10)
nbathreeFGtrends = nbathreeFGtrends.groupby("year").median()
nbathreeFGtrends = nbathreeFGtrends.reset_index()
nbathreeFGtrends = nbathreeFGtrends[nbathreeFGtrends["threePointsPerGame"] > 0]
sns.lineplot(data=nbathreeFGtrends, x="year", y="threePointsPerGame").set_title("3PPG (3 points per game) per year")
plt.show()
plt.show(block=False)

"""
PART III
3A. Many sports analysts argue about which player is the GOAT (the Greatest Of All Time). Based on this 
data, who would you say is the GOAT? Provide evidence to back up your decision.
"""
#Calculate each player's career statistics

#WORKING CAREER PPG - CAREER POINTS PER GAME
#Count the total number of points and games played that each player has
#Rename the columns as "total+(type of column)" for better clarity
nba_PPG = nba.groupby(["name"], as_index=False).agg({"points":"sum", "GP":"sum"}).rename(columns={'points':'totalPoints', 'GP':'totalGP'})
#Calculate the total points per game or career points per game
#with a player's total points and total games played
nba_PPG["totalPointsPerGame"] = nba_PPG["totalPoints"]/ nba_PPG["totalGP"]
nba_PPG= nba_PPG[nba_PPG.totalPointsPerGame > 0].round(2)
#Display only the top 10 players with the highest career points per game
nba_PPG = nba_PPG.sort_values("totalPointsPerGame", ascending=False).head(10)
print(nba_PPG)

#WORKING CAREER RPG - CAREER REBOUNDS PER GAME
nba_RPG = nba.groupby(["name"], as_index=False).agg({"rebounds":"sum", "GP":"sum"}).rename(columns={'rebounds':'totalRebounds', 'GP':'totalGP'})
nba_RPG["totalReboundsPerGame"] = nba_RPG["totalRebounds"]/ nba_RPG["totalGP"]
nba_RPG= nba_RPG[nba_RPG.totalReboundsPerGame > 0]
nba_RPG = nba_RPG.sort_values("totalReboundsPerGame", ascending=False).head(10)
print(nba_RPG)

#WORKING CAREER APG - CAREER ASSISTS PER GAME
nba_APG = nba.groupby(["name"], as_index=False).agg({"assists":"sum", "GP":"sum"}).rename(columns={'assists':'totalAssists', 'GP':'totalGP'})
nba_APG["totalAssistsPerGame"] = nba_APG["totalAssists"]/ nba_APG["totalGP"]
nba_APG= nba_APG[nba_APG.totalAssistsPerGame > 0]
nba_APG = nba_APG.sort_values("totalAssistsPerGame", ascending=False).head(10)
print(nba_APG)

#WORKING CAREER SPG - CAREER STEALS PER GAME
nba_SPG = nba.groupby(["name"], as_index=False).agg({"steals":"sum", "GP":"sum"}).rename(columns={'steals':'totalSteals', 'GP':'totalGP'})
nba_SPG["totalStealsPerGame"] = nba_SPG["totalSteals"]/ nba_SPG["totalGP"]
nba_SPG= nba_SPG[nba_SPG.totalStealsPerGame > 0].round(2)
nba_SPG = nba_SPG.sort_values("totalStealsPerGame", ascending=False).head(10)
print(nba_SPG)

#WORKING CAREER BPG - CAREER BLOCKS PER GAME
nba_BPG = nba.groupby(["name"], as_index=False).agg({"blocks":"sum", "GP":"sum"}).rename(columns={'blocks':'totalBlocks', 'GP':'totalGP'})
nba_BPG["totalBlocksPerGame"] = nba_BPG["totalBlocks"]/ nba_BPG["totalGP"]
nba_BPG= nba_BPG[nba_BPG.totalBlocksPerGame > 0].round(2)
nba_BPG = nba_BPG.sort_values("totalBlocksPerGame", ascending=False).head(10)
print(nba_BPG)


#MICHAEL JORDAN CAREER STATS
#Copies original dataframe to a new one that filters only Michael Jordan's results
nba2 = nba
nba2 = nba2.query('name == "Michael Jordan"')

mj = nba2.groupby(["name", "pos"], as_index=False).agg({"GP":"sum", "points":"sum", "assists":"sum", "rebounds":"sum", "steals":"sum", "blocks":"sum"})
mj["pointsPerGame"] = mj["points"]/ mj["GP"]
mj["assistsPerGame"] = mj["assists"]/ mj["GP"]
mj["reboundsPerGame"] = mj["rebounds"]/ mj["GP"]
mj["stealsPerGame"] = mj["steals"]/ mj["GP"]
mj["blocksPerGame"] = mj["blocks"]/ mj["GP"]
#Round values
mj["pointsPerGame"] = mj["pointsPerGame"].round(2)
mj["assistsPerGame"] = mj["assistsPerGame"].round(2)
mj["reboundsPerGame"] = mj["reboundsPerGame"].round(2)
mj["stealsPerGame"] = mj["stealsPerGame"].round(2)
mj["blocksPerGame"] = mj["blocksPerGame"].round(2)

#Displays Michael Jordan's statistics
print("#####################################Michael Jordan's Career Stats#####################################")
print(mj[["name", "pos", "pointsPerGame", "assistsPerGame", "reboundsPerGame", "stealsPerGame", "blocksPerGame"]])

nba3 = nba
nba3 = nba3.query('name == "Wilton Chamberlain"')
wc = nba3.groupby(["name", "pos"], as_index=False).agg({"GP":"sum", "points":"sum", "assists":"sum", "rebounds":"sum", "steals":"sum", "blocks":"sum"})
wc["pointsPerGame"] = wc["points"]/ wc["GP"]
wc["assistsPerGame"] = wc["assists"]/ wc["GP"]
wc["reboundsPerGame"] = wc["rebounds"]/ wc["GP"]
wc["stealsPerGame"] = wc["steals"]/ wc["GP"]
wc["blocksPerGame"] = wc["blocks"]/ wc["GP"]
#Round values
wc["pointsPerGame"] = wc["pointsPerGame"].round(2)
wc["assistsPerGame"] = wc["assistsPerGame"].round(2)
wc["reboundsPerGame"] = wc["reboundsPerGame"].round(2)
wc["stealsPerGame"] = wc["stealsPerGame"].round(2)
wc["blocksPerGame"] = wc["blocksPerGame"].round(2)

print("###################################Wilton Chamberlain's Career Stats###################################")
print(wc[["name", "pos", "pointsPerGame", "assistsPerGame", "reboundsPerGame", "stealsPerGame", "blocksPerGame"]])





