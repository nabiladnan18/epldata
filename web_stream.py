import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly_express as px


# path = "https://raw.githubusercontent.com/TheButcherOfBlaviken/epldata/master/combined_3800_rows.csv"
path = "combined_3800_rows.csv"
data = st.cache(pd.read_csv)(path)
# print(data.shape)
# print(data.columns)
# print(data.head(10))
table = data.iloc[:, :11]
# print(table.head(10))
unsorted_teams = list(table["HomeTeam"].unique())
teams = sorted(unsorted_teams)


# def run():
#     return


def data(selection):

    # DF Write Columns #

    # loc[:, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    #####################
    # GENERAL STATISTICS
    #####################

    # total number of games played
    played_home = table.query(f"HomeTeam == '{selection}'", inplace=False)      # HOME df
    played_away = table.query(f"AwayTeam == '{selection}'", inplace=False)      # AWAY df
    played_total = played_home + played_away        # TOTAL df
    played_total_count = len(played_total)       # TOTAL COUNT

    # total games won and lost
    total_home_wins = table.query(f"HomeTeam == '{selection}' and FTR == 'H'", inplace=False)       # home wins df
    total_away_wins = table.query(f"AwayTeam == '{selection}' and FTR == 'A'", inplace=False)       # away wins df
    total_wins = total_home_wins + total_away_wins      # total wins df
    total_wins_count = len(total_wins)          # total wins count
    total_losses = played_total_count - total_wins      # played total df
    total_losses_count = played_total_count - total_wins_count        # total losses count

    # number of seasons appeared
    no_of_seasons = played_total_count / 38      # number of seasons count

    # total clean sheets
    clean_sheets_home = table.query(f"HomeTeam == '{selection}' and FTAG == 0")       # home clean sheets df
    clean_sheets_away = table.query(f"AwayTeam == '{selection}' and HTAG == 0")       # away clean sheets df
    clean_sheets = clean_sheets_away + clean_sheets_home        # total clean sheets df
    clean_sheets_count = len(clean_sheets)        # total no. of clean sheets count

    #####################
    # DOMINATION STATISTICS
    #####################

    # Winning at HT and FT at HOME
    home_waht_waft = table.query(f"HomeTeam == '{selection}' and HTR == 'H' and FTR == 'H'", inplace=False).loc[:, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    # Winning with more than 3 goals and a 2-goal GD
    domination_win = table.query(f"HomeTeam == '{selection}' and FTHG > 3 and FTAG < 2", inplace=False).loc[:, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    # Winning with more than 2 goals and a clean-sheet
    domination_with_cs = table.query(f"HomeTeam == '{selection}' and FTHG > 2 and FTAG == 0", inplace=False).loc[:, ["Date", "AwayTeam", "FTHG", "HTHG"]]

    #####################
    # COMEBACK STATISTICS
    #####################

    # losing at HT then winning at FT at HOME df
    home_laht_waft = table.query(f"HomeTeam == '{selection}' and HTR == 'A' and FTR == 'H'", inplace=False).loc[:, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    # losing at HT then winning at FT at AWAY df
    away_laht_waft = table.query(f"AwayTeam == '{selection}' and HTR == 'H' and FTR == 'A'", inplace=False).loc[:, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    # losing at HT then winning at FT df
    total_laht_waft = home_laht_waft + away_laht_waft

    # losing at HT then winning at FT count
    total_laht_waft_count = len(total_laht_waft)



    #####################
    # OOPSIE STATISTICS
    #####################

    # matches lost after being ahead at half-time at home
    home_waht_laft = table.query(f"HomeTeam == '{selection}' and HTR == 'H' and FTR == 'A'", inplace=False).loc[:, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    # pc of winning after being ahead at HT at home
    pc_of_ftw_htw = round((len(home_waht_waft) / len(played_home)) * 100, ndigits=2)

    # pc of losing after being ahead at HT at home
    pc_of_ftl_htw = round((len(home_waht_laft) / len(played_home)) * 100, ndigits=2)

    # pc of total wins
    pc_of_win = round((total_wins_count / played_total_count) * 100, ndigits=2)

# analytics

    f''' ## General statistics for {selection}
    
    Won {pc_of_win}% of all matches played.\n

    \n
    Played a total of {played_total_count} matches or {no_of_seasons} season(s) since 2009-10.\n
    Kept a total of {clean_sheets_count} clean sheets.\n

    '''

    '## Domination'

    f'### Won {pc_of_ftw_htw}% of home games after being ahead at half-time: {len(home_waht_waft)} time(s)'
    st.write(home_waht_waft)

    f'### Won by over 3 goals with at least 2 GD: {len(domination_win)}times(s)'
    st.write(domination_win)

    '## Comeback'






    '## Oopsies'
    f"### Lost {pc_of_ftl_htw}% of home games after being ahead at half-time: {len(home_waht_laft)} time(s)"
    st.write(home_waht_laft)


    '''
    
    '''


'''
# Find out your team's performance in the PL starting from 2009/10 season till 2018/2019.
'''

clubs = st.selectbox('Pick your club:', teams)
data(clubs)

'''
### Thanks for visiting! <3
Please wait for more updates! 
'''


# if __name__ == "__main__":
#     run()
