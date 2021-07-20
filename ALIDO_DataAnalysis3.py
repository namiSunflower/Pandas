import pandas as pd # Our data manipulation library
import seaborn as sns # Used for graphing/plotting
import matplotlib.pyplot as plt # If we need any low level methods
import os # Used to change the directory to the right place

coach_awards = pd.read_csv("nba_basketball_data/basketball_awards_coaches.csv")
master = pd.read_csv("nba_basketball_data/basketball_master.csv")
#Before merging, reorder the columns to avoid errors
coach_awards = coach_awards[["coachID", "year", "award", "lgID"]]

nba_coach = pd.merge(coach_awards, master, how="left", left_on="coachID", right_on="bioID")
nba_coach["name"]= nba_coach['firstName'].astype(str) + nba_coach['lastName']

#Creates new dataframe to only include awards within the NBA league
nba_award = nba_coach
nba_award = nba_award[nba_award.award != "ABA Coach of the Year"]

mostNBA_Awards = nba_award.groupby("name", as_index=False).agg({"award":"count"}).rename(columns={'award':'totalAwards'})

mostNBA_Awards = mostNBA_Awards.sort_values("totalAwards", ascending=False)

#Plots a barplot to show the coaches with the most awards
sns.set_theme(style="whitegrid")
mostNBA_Awards = mostNBA_Awards[mostNBA_Awards.totalAwards > 1]
sns.barplot(data=mostNBA_Awards, x="totalAwards", y="name", orient="h").set_title("Most NBA Coach of the Year Awards")
plt.show()
plt.show(block=False)


aba_award = nba_coach
aba_award = aba_award[aba_award.award != "NBA Coach of the Year"]

mostABA_Awards = aba_award.groupby("name", as_index=False).agg({"award":"count"}).rename(columns={'award':'totalAwards'})

mostABA_Awards = mostABA_Awards.sort_values("totalAwards", ascending=False)

sns.set_theme(style="whitegrid")


sns.barplot(data=mostABA_Awards, x="totalAwards", y="name", orient="h").set_title("Most ABA Coach of the Year Awards")
plt.show()
plt.show(block=False)