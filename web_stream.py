import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly_express as px


# @st.cache
def read_data():
    path = "https://raw.githubusercontent.com/TheButcherOfBlaviken/epldata/master/combined_csv4.csv"
    # path = "combined_csv4.csv"
    data = pd.read_csv(path)
    # print(data.shape)
    # print(data.columns)
    # print(data.head(10))
    
    read_data.table = data.iloc[:, :11]
    # print(read_data.table.head(10))
    
    unsorted_teams = list(read_data.table["HomeTeam"].unique())
    read_data.teams = sorted(unsorted_teams)
    return read_data.teams, read_data.table


read_data()

'''
# Find out your team's performance in the PL starting from 2009/10 season till 2018/2019.
'''
clubs = st.selectbox('Pick your club:', read_data.teams)

home_waht_waft = read_data.table.query(f"HomeTeam == '{clubs}' and HTR == 'H' and FTR == 'H'", inplace=False)

# matches lost after being ahead at half-time at home
home_waht_laft = read_data.table.query(f"HomeTeam == '{clubs}' and HTR == 'H' and FTR == 'A'", inplace=False)

# total number of games played
played_home = read_data.table.query(f"HomeTeam == '{clubs}'", inplace=False)  # home
played_away = read_data.table.query(f"AwayTeam == '{clubs}'", inplace=False)  # away
# played_total_by_2 = int((len(played_away) + len(played_home))/2)
played_total = int((len(played_away) + len(played_home)))

# number of seasons appeared
no_of_seasons = int(played_total / 38)

# total number of wins after losing at half-time
home_laht_waft = read_data.table.query(f"HomeTeam == '{clubs}' and HTR == 'A' and FTR == 'H'", inplace=False)
away_laht_waft = read_data.table.query(f"AwayTeam == '{clubs}' and HTR == 'H' and FTR == 'A'", inplace=False)
total_laht_waft = len(home_laht_waft) + len(away_laht_waft)

# total games won and lost
total_home_wins = read_data.table.query(f"HomeTeam == '{clubs}' and FTR == 'H'", inplace=False)
total_away_wins = read_data.table.query(f"AwayTeam == '{clubs}' and FTR == 'A'", inplace=False)
total_wins = int((len(total_home_wins) + len(total_away_wins)))
total_losses = played_total - total_wins

# pc of winning after being ahead at HT at home
pc_of_ftw_htw = round((len(home_waht_waft) / len(played_home)) * 100, ndigits=2)

# pc of losing after being ahead at HT at home
pc_of_ftl_htw = round((len(home_waht_laft) / len(played_home)) * 100, ndigits=2)

# pc of total wins
pc_of_win = round((total_wins / played_total) * 100, ndigits=2)
# pc_wins.append(pc_of_win)
# analytics

f'''
## Key statistics for {clubs}

Won {pc_of_win}% of all matches played.\n
Won {pc_of_ftw_htw}% of home games after being ahead at half-time.\n
Lost {pc_of_ftl_htw}% of home games after being ahead at half-time.\n
Played a total of {played_total} matches or {no_of_seasons} season(s) since 2009-10.\n
'''

st.subheader(f"Winning at half time and full time at home: {len(home_waht_waft)} time(s)")
query_df = read_data.table.query(f"HomeTeam == '{clubs}' and HTR == 'H' and FTR == 'H'", inplace=False)
w_ht_ft = query_df.loc[:, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
st.write(w_ht_ft)

st.subheader(f"Winning at half time but losing at full time at home: {len(home_waht_laft)} time(s)")
query_df = read_data.table.query(f"HomeTeam == '{clubs}' and HTR == 'H' and FTR == 'A'", inplace=False)
w_ht_ft = query_df.loc[:, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
st.write(w_ht_ft)

'''
'''

'''
### Thanks for visiting! <3
Please wait for more updates! 
'''


if __name__ == "__main__":
    read_data()

