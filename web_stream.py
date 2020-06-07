import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly_express as px
import numpy as np

path = "https://raw.githubusercontent.com/TheButcherOfBlaviken/epldata/master/combined_3800_rows.csv"  # path to the publicly accessible data
# path = "combined_3800_rows.csv"
data = pd.read_csv(path)
# print(data.shape)
# print(data.columns)
# print(data.head(10))
table = data.iloc[:, :11]  # all the rows and upto the 11th column
# print(table.head(10))
unsorted_teams = list(table["HomeTeam"].unique())  # finds out the individual names of the team but are unsorted
teams = sorted(unsorted_teams)  # the team names are now sorted


# def run():
#     return

# @st.cache(suppress_st_warning=True)
def data(selection):
    #####################
    # GENERAL STATISTICS
    #####################

    # total number of games played
    played_home = table.query(f"HomeTeam == '{selection}'", inplace=False)  # HOME df
    played_away = table.query(f"AwayTeam == '{selection}'", inplace=False)  # AWAY df
    played_total = played_home + played_away
    played_total_count = len(played_total)  # TOTAL COUNT
    played_home_count = len(played_home)  # total home games count
    played_away_count = len(played_away)  # total away games count

    # total games won and lost
    total_home_wins = table.query(f"HomeTeam == '{selection}' and FTR == 'H'", inplace=False)  # home wins df
    total_away_wins = table.query(f"AwayTeam == '{selection}' and FTR == 'A'", inplace=False)  # away wins df
    total_home_losses = table.query(f"HomeTeam == '{selection}' and FTR == 'A'", inplace=False)  # home losses df
    total_away_losses = table.query(f"AwayTeam == '{selection}' and FTR == 'H'", inplace=False)  # away losses df
    total_winning_ht_home = table.query(f"HomeTeam == '{selection}' and HTR == 'H'",
                                        inplace=False)  # winning at home at HT df
    total_winning_ht_away = table.query(f"AwayTeam == '{selection}' and HTR == 'A'",
                                        inplace=False)  # winning at away at HT df
    total_losing_ht_home = table.query(f"HomeTeam == '{selection}' and HTR == 'A'",
                                       inplace=False)  # losing at home at HT df
    total_losing_ht_away = table.query(f"AwayTeam == '{selection}' and HTR == 'H'",
                                       inplace=False)  # losing at away at HT df

    total_winning_ht_home_count = len(total_winning_ht_home)
    total_winning_ht_away_count = len(total_winning_ht_away)
    total_losing_ht_home_count = len(total_losing_ht_home)
    total_losing_ht_away_count = len(total_losing_ht_away)

    total_wins = total_home_wins + total_away_wins  # total wins df
    total_wins_count = len(total_wins)  # total wins count
    total_losses = played_total - total_wins  # played total df
    total_losses_count = played_total_count - total_wins_count  # total losses count
    total_home_wins_count = len(total_home_wins)  # total home wins count
    total_away_wins_count = len(total_away_wins)  # total away wins count

    # test block #
    # if total_losses_count == len(total_away_losses) + len(total_home_losses):
    #     print("Issallgood, man!)
    # else:
    #     print("DF is fucked")
    #     raise AssertionError
    # end test block #

    # number of seasons appeared
    no_of_seasons = int(played_total_count / 38)  # number of seasons count

    # total clean sheets
    clean_sheets_home = table.query(f"HomeTeam == '{selection}' and FTAG == 0")  # home clean sheets df
    clean_sheets_away = table.query(f"AwayTeam == '{selection}' and HTAG == 0")  # away clean sheets df
    clean_sheets = clean_sheets_away + clean_sheets_home  # total clean sheets df
    clean_sheets_count = len(clean_sheets)  # total no. of clean sheets count

    #####################
    # DOMINATION STATISTICS
    #####################

    # Winning at HT and FT at HOME
    home_waht_waft = table.query(f"HomeTeam == '{selection}' and HTR == 'H' and FTR == 'H'", inplace=False).loc[:,
                     ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
    home_waht_waft_count = len(home_waht_waft)

    # # Winning with more than 3 goals and a 2-goal GD # #

    # Creating a new column called 'gd' in each created DF and using eggs.sub(spam) to subtract spam from eggs
    total_home_wins['gd'] = total_home_wins["FTHG"].sub(total_home_wins["FTAG"])
    total_away_wins['gd'] = total_away_wins["FTAG"].sub(total_away_wins["FTHG"])

    # finding gd > 2
    domination_wins_home = total_home_wins.loc[total_home_wins['gd'] > 2]
    domination_wins_away = total_away_wins.loc[total_away_wins['gd'] > 2]

    domination_win_at_home_count = len(domination_wins_home)
    domination_win_at_away_count = len(domination_wins_away)

    # adding one DF to another DF at the end eggs.append(spam) to add spam at the end of eggs
    domination_wins = domination_wins_home.append(domination_wins_away).loc[:,
                      ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
    domination_win_count = len(domination_wins)

    # Winning with more than 2 goals and a clean-sheet
    domination_with_cs = table.query(f"HomeTeam == '{selection}' and FTHG > 2 and FTAG == 0", inplace=False).loc[:,
                         ["Date", "HomeTeam", "AwayTeam", "FTHG", "HTHG"]]

    # pc of winning after being ahead at HT at home
    pc_of_ftw_htw = round((home_waht_waft_count / total_winning_ht_home_count) * 100, ndigits=2)

    # pc of total wins
    pc_of_win = round((total_wins_count / played_total_count) * 100, ndigits=2)

    # Biggest win - home

    # how to use many many conditions involving max and min
    # biggest_win_home = total_home_wins.loc[(((total_home_wins["FTHG"] == total_home_wins["FTHG"].max()) > (
    # total_home_wins["gd"] == total_home_wins["gd"].max())) & (total_home_wins["FTHG"] != total_home_wins["FTAG"]))["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    biggest_win_home = total_home_wins.loc[(total_home_wins["gd"] == total_home_wins["gd"].max()) & (
                total_home_wins["FTHG"] == total_home_wins["FTHG"].max()),
                                           ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    # yeah i know the first thing is not required.
    # wrote it just so that I remember that you can write multiple conditions like that.
    # interestingly, the logic operators do not work like programming e.g. it's not && but &, not || but | and
    # gte or lte is written => and <= respectively!
    # biggest_win_home = biggest_gd_home.loc[biggest_gd_home["FTHG"] == biggest_gd_home["FTHG"].max(),
    #                                         ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    # biggest_win_home_df = total_home_wins.loc[total_home_wins, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
    biggest_win_home_gs = biggest_win_home.loc[:, "FTHG"].values[0]
    biggest_win_home_gc = biggest_win_home.loc[:, "FTAG"].values[0]
    biggest_win_home_opponent = list(biggest_win_home.loc[:, "AwayTeam"].values)

    # Biggest win - away

    # biggest_win_away_index = total_away_wins[["gd"]].idxmax()
    # biggest_win_away_index = total_away_wins.loc[
    #     total_away_wins["FTAG"] == total_away_wins["FTAG"].max()
    #     ].index.tolist()
    #
    # for i in biggest_win_away_index:
    #     biggest_win_away_df = total_away_wins.loc[i, ["Date", "HomeTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
    #     biggest_win_away_gc = total_away_wins.loc[i, "FTHG"].values[0]
    #     biggest_win_away_gs = total_away_wins.loc[i, "FTAG"].values[0]
    #     biggest_win_away_opponent = total_away_wins.loc[i, "HomeTeam"].values[0]

    biggest_win_away = total_away_wins.loc[((total_away_wins["FTAG"] == total_away_wins["FTAG"].max()) & (
            total_away_wins["FTAG"] != total_away_wins["FTHG"]) & (
                                                    total_away_wins["gd"] == total_away_wins["gd"].max())),
                                           ["Date", "HomeTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    # biggest_win_home_df = total_home_wins.loc[total_home_wins, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
    biggest_win_away_gs = biggest_win_away.loc[:, "FTAG"].values[0]
    biggest_win_away_gc = biggest_win_away.loc[:, "FTHG"].values[0]
    biggest_win_away_opponent = list(biggest_win_away.loc[:, "HomeTeam"].values)

    #####################
    # COMEBACK STATISTICS
    #####################

    # losing at HT then winning at FT at HOME df
    home_laht_waft = table.query(f"HomeTeam == '{selection}' and HTR == 'A' and FTR == 'H'", inplace=False).loc[
                     :,
                     ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
    home_laht_waft_count = len(home_laht_waft)
    pc_of_home_laht_waft = round((home_laht_waft_count / total_losing_ht_home_count) * 100, ndigits=2)

    # losing at HT then winning at FT at AWAY df
    away_laht_waft = table.query(f"AwayTeam == '{selection}' and HTR == 'H' and FTR == 'A'", inplace=False).loc[:,
                     ["Date", "HomeTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
    away_laht_waft_count = len(away_laht_waft)
    pc_of_away_laht_waft = round((away_laht_waft_count / total_losing_ht_away_count) * 100, ndigits=2)

    # losing at HT then winning at FT df
    total_laht_waft = home_laht_waft + away_laht_waft

    # losing at HT then winning at FT count
    total_laht_waft_count = len(total_laht_waft)

    # losing at HT total
    losing_at_ht = len(total_losing_ht_home + total_losing_ht_away)

    #####################
    # OOPSIE STATISTICS
    #####################

    # matches lost after being ahead at half-time at home
    home_waht_laft = table.query(f"HomeTeam == '{selection}' and HTR == 'H' and FTR == 'A'", inplace=False).loc[
                     :, ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
    home_waht_laft_count = len(home_waht_laft)

    # pc of losing after being ahead at HT at home
    pc_of_ftl_htw = round((home_waht_laft_count / total_winning_ht_home_count) * 100, ndigits=2)

    # Biggest loss - home
    total_home_losses['gd'] = total_home_losses["FTAG"].sub(total_home_losses["FTHG"])

    biggest_loss_home_gd = total_home_losses.loc[total_home_losses["gd"] == total_home_losses["gd"].max()]
    biggest_loss_home = biggest_loss_home_gd.loc[biggest_loss_home_gd["FTAG"] == biggest_loss_home_gd["FTAG"].max(),
                                                 ["Date", "AwayTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
    biggest_loss_home_gs = biggest_loss_home.loc[:, "FTAG"].values[0]
    biggest_loss_home_gc = biggest_loss_home.loc[:, "FTHG"].values[0]
    biggest_loss_home_opponent = list(biggest_loss_home.loc[:, "AwayTeam"])

    # Biggest loss - away
    total_away_losses['gd'] = total_away_losses["FTHG"].sub(total_away_losses["FTAG"])

    # USE MULTIPLE AND CONDITIONS LIKE THIS #                                                                                               # HEY CHECK THIS OUT #
    # biggest_loss_away = total_away_losses.loc[((total_away_losses["FTHG"] == total_away_losses["FTHG"].max()) &
    #                                            (total_away_losses["FTHG"] != total_away_losses["FTAG"].max())),
    #                                           ["Date", "HomeTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]

    biggest_loss_away_gd = total_away_losses.loc[total_away_losses['gd'] == total_away_losses['gd'].max()]
    biggest_loss_away = biggest_loss_away_gd.loc[biggest_loss_away_gd["FTHG"] == biggest_loss_away_gd["FTHG"].max(),
                                                 ["Date", "HomeTeam", "FTHG", "FTAG", "HTHG", "HTAG"]]
    biggest_loss_away_gc = biggest_loss_away.loc[:, "FTHG"].values[0]
    biggest_loss_away_gs = biggest_loss_away.loc[:, "FTAG"].values[0]
    biggest_loss_away_opponent = list(biggest_loss_away.loc[:, "HomeTeam"])

    # analytics

    f''' ## General statistics for {selection}
    
    Won {pc_of_win}% of all matches played.\n
    Played a total of {played_total_count} matches or {no_of_seasons} season(s) since 2009-10.\n
    Kept a total of {clean_sheets_count} clean sheets.\n

    '''

    '## > We fought them hard, we fought them well'

    f'### Won {pc_of_ftw_htw}% of home games after being ahead at half-time: {home_waht_waft_count} time(s)'
    st.write(home_waht_waft)

    f'### Won by over 3 goals with at least 2 GD. Home: {domination_win_at_home_count} time(s). Away: {domination_win_at_away_count} time(s)'
    st.write(domination_wins)

    f'### Biggest victory at home: {biggest_win_home_gs}-{biggest_win_home_gc} against {", ".join(biggest_win_home_opponent)}'
    st.write(biggest_win_home)

    f'### Biggest victory away: {biggest_win_away_gc}-{biggest_win_away_gs} against {", ".join(biggest_win_away_opponent)}'
    st.write(biggest_win_away)

    '## > Hairdryer treatment from the Gaffer?'

    f'### Won {pc_of_home_laht_waft}% of home matches after losing at half time: {home_laht_waft_count} time(s)'
    st.write(home_laht_waft)

    f'### Won {pc_of_away_laht_waft}% of away matches after losing at half time: {away_laht_waft_count} times(s)'
    st.write(away_laht_waft)

    '## > Shame! _ding_ Shame! _ding_ '
    f"### Lost {pc_of_ftl_htw}% of home games after being ahead at half-time: {len(home_waht_laft)} time(s)"
    st.write(home_waht_laft)

    f'### Biggest loss at home: {biggest_loss_home_gs}-{biggest_loss_home_gc} against {", ".join(biggest_loss_home_opponent)}'
    st.write(biggest_loss_home)

    f'### Biggest loss away: {biggest_loss_away_gc}-{biggest_loss_away_gs} against {", ".join(biggest_loss_away_opponent)}'
    st.write(biggest_loss_away)

    # '## Win statistics for all teams'
    '''
    '''


'''
# Find out your team's performance in the PL starting from 2009/10 season till 2018/2019.
'''

clubs = st.selectbox('Pick your club:', teams)
# clubs = "Arsenal"         # Testing #
data(clubs)

'''
### Thanks for visiting! <3
Please wait for more updates! \n 
Nabil Adnan
'''

# if __name__ == "__main__":
#     run()
