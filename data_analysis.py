import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

data = pd.read_csv("combined_csv.csv").drop_duplicates()
print(data.shape)
print(data.columns)
# print(data.head(10))

table = data.iloc[:, :11]
print(table.head(10))

unsorted_teams = list(table["HomeTeam"].unique())
teams = sorted(unsorted_teams)

pc_wins = []
for i in teams:
    # matches won winning after being ahead at half-time at home
    home_waht_waft = table.query(f"HomeTeam == '{i}' and HTR == 'H' and FTR == 'H'", inplace=False)

    # matches lost after being ahead at half-time at home
    home_waht_laft = table.query(f"HomeTeam == '{i}' and HTR == 'H' and FTR == 'A'", inplace=False)

    # total number of games played
    played_home = table.query(f"HomeTeam == '{i}'", inplace=False)  # home
    played_away = table.query(f"AwayTeam == '{i}'", inplace=False)  # away
    # played_total_by_2 = int((len(played_away) + len(played_home))/2)
    played_total = int((len(played_away) + len(played_home)))

    # number of seasons appeared
    no_of_seasons = int(played_total/38)

    # total number of wins after losing at half-time
    home_laht_waft = table.query(f"HomeTeam == '{i}' and HTR == 'A' and FTR == 'H'", inplace=False)
    away_laht_waft = table.query(f"AwayTeam == '{i}' and HTR == 'H' and FTR == 'A'", inplace=False)
    total_laht_waft = len(home_laht_waft) + len(away_laht_waft)

    # total games won and lost
    total_home_wins = table.query(f"HomeTeam == '{i}' and FTR == 'H'", inplace=False)
    total_away_wins = table.query(f"AwayTeam == '{i}' and FTR == 'A'", inplace=False)
    total_wins = int((len(total_home_wins) + len(total_away_wins)))
    total_losses = played_total - total_wins

    # pc of winning after being ahead at HT at home
    pc_of_ftw_htw = round((len(home_waht_waft) / len(played_home)) * 100, ndigits=2)

    # pc of losing after being ahead at HT at home
    pc_of_ftl_htw = round((len(home_waht_laft) / len(played_home)) * 100, ndigits=2)

    # pc of total wins
    pc_of_win = round((total_wins / played_total) * 100, ndigits=2)
    pc_wins.append(pc_of_win)
    # analytics
    print(
        "##############################"'\n'
        f"{i}"'\n'
        "##############################"'\n'
               
        f"> Won {pc_of_win}% of all matches played."'\n'
        f"> Won {pc_of_ftw_htw}% of home games after being ahead at half-time."'\n'
        f"> Lost {pc_of_ftl_htw}% of home games after being ahead at half-time."'\n'
        f"> Played a total of {played_total} matches or {no_of_seasons} season(s) since 2009-10."'\n'
        f"> "
        )

# y = []
# for i in range(0, 36):
#     y.append(i)

plt.title("Win percentage by teams from 2009-10 to 2018-19 seasons")
plt.xlabel("Teams in PL")
plt.ylabel("Percentage of wins")
plt.tick_params(axis='x', labelsize=10)
plt.xticks(rotation=90)
plt.bar(teams, pc_wins)
plt.show()





