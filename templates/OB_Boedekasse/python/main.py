#!/opt/render/.local/bin/python3

from functions import *

# dbu_match_ID_list = ["193827","193831","193834","193840","193845","193847","201625","201750","201753","202852","202855","202857"]
# season = "409842"
dbu_match_ID_list = ["894708","894711","894714","894809","895540","895598","895603","895544","895606","895609","895628","895632","896193","896199"]
dbu_season = "427115"
season_start = "01/04/2024"
won_match = 10
draw_match = 20
lost_match = 30

conceded_goal = 5
scored_goal = 2 

red_card_fine = 100
yellow_card_fine = 50

#list of all dbu players
dbu_names = search_database("player_finance.json","payingPlayers","dbu_name")

#list of all players mobilepay name
mobilepay_names = search_database("player_finance.json","payingPlayers","mobilepay_name")

#Add all the matches to the matches database without adding information
add_matches_to_database(dbu_match_ID_list,dbu_season)
add_match_to_database("407063","427339",len(dbu_match_ID_list))

#Reset all players economy data.
reset_fines(len(dbu_names))

update_player_deposit(mobilepay_names,season_start)



def runCode(match,season):
    match_result = find_match_result(match,season)
    if match_result == False:
        return
    elif match_result == "postponed":
        print("postponed")
        return
    print("videre",match)
    fine = calculate_fine(match_result,won_match,draw_match,lost_match,conceded_goal,scored_goal)
    team_lineup_in_match = find_team_lineup(match,season)
    playerlist = who_played_the_game(dbu_names,team_lineup_in_match)
    append_data_to_database(match,playerlist,(len(dbu_match_ID_list)+1),match_result,fine)
    update_dept(playerlist,fine,len(dbu_names))

# making the matches.json file.     
for dbumatch in dbu_match_ID_list:
    runCode(dbumatch,dbu_season)
    
runCode("407063","427339")

find_balance(yellow_card_fine,red_card_fine) 
mobilepay_box(season_start)
