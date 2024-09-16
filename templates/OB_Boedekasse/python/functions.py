import requests
import json
import csv  
from datetime import datetime
import os
from bs4 import BeautifulSoup
import re

current_directory = os.path.dirname(os.path.abspath(__file__))

matches_file_path = os.path.join(current_directory, '..', 'database', 'matches.json')
player_finance_file_path = os.path.join(current_directory, '..', 'database', 'player_finance.json')
trans_file_path = os.path.join(current_directory, '..', 'database', 'trans.csv')
database_file_path = os.path.join(current_directory, '..', 'database')
mobilepay_box_file_path = os.path.join(current_directory, '..', 'database', 'mobile_box_stats.json')



#Find a time in the JSON file, input are the name type dbu_name or mobilepay_name
def search_database(filename,database,type):
    dbu_name_list = []
    with open(database_file_path+"/"+filename,"r", encoding="utf-8") as ap:
        data = json.load(ap)
        for i in range(len(data[database])):
            dbu_name_list.append(data[database][i][type])

    return dbu_name_list


#Webscrape the player list from DBU webiste
def find_team_lineup(match_id,dbu_season_ID):
    team_lineup_url = "https://www.dbu.dk/resultater/kamp/" + match_id + "_"+dbu_season_ID+"/kampinfo"

    #request html code from dbu.dk
    team_lineup_html_request = requests.get(team_lineup_url)
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(team_lineup_html_request.text, 'html.parser')
    
    # Find all team lineup information
    team_lineup_info = soup.find_all("div", {"class": "sr--match--team-cards dbu-grid"})
    
    # Extract text from HTML elements
    team_lineup_text = [info.get_text() for info in team_lineup_info]

    team_lineup_text_string = ""
    for elements in team_lineup_text:
        team_lineup_text_string += elements
    
    team_lineup_text_string = re.sub(r'\n\s*\n', '\n', team_lineup_text_string).strip()

    return team_lineup_text_string


#Insert all matches in database/player_finance.json
def add_matches_to_database(matches_list,season):
    with open(matches_file_path,"r+",encoding="utf-8") as ap:
        data = json.load(ap)
        for i in range(len(matches_list)):
            data["matches"][i]["season"] = season
            data["matches"][i]["matchID"] = matches_list[i]
            data["matches"][i]["playerlist"] = []
            data["matches"][i]["match_result"] = []
            data["matches"][i]["fine"] = ""

        # Move the file pointer to the beginning of the file before writing
        ap.seek(0)
        
        # Write the updated data back to the file
        json.dump(data, ap, indent=4)

        # Truncate the file to the current file position to remove any extra data. because the file add some weird ]} in the end. 
        ap.truncate()


def add_match_to_database(match_id, season, index):
    with open(matches_file_path, "r+", encoding="utf-8") as file:
        data = json.load(file)
        
        # Create a new match entry
        new_match = {
            "season": season,
            "matchID": match_id,
            "playerlist": [],
            "match_result": [],
            "fine": ""
        }

        # Insert the new match at the specified index
        data["matches"][index] = new_match
        
        # Move the file pointer to the beginning of the file before writing
        file.seek(0)
        
        # Write the updated data back to the file
        json.dump(data, file, indent=4)
        
        # Truncate the file to the current file position to remove any extra data because the file adds some weird ]} at the end.
        file.truncate()

# Example usage:
add_match_to_database("ABC123", "2024", 0)  # Insert at index 0



def who_played_the_game(playerlist,match_HTML):
    player_played = []
    for player in playerlist:
        if player in match_HTML:
            player_played.append(player)
    return player_played
    


def append_data_to_database(match,playerlist,len,match_result,fine):
    with open(matches_file_path,"r+",encoding="utf-8") as ap:
        data = json.load(ap)
        for i in range(len):
            matchID = data["matches"][i]["matchID"]
            if matchID == match:
                data["matches"][i]["playerlist"] = playerlist
                data["matches"][i]["match_result"] = match_result
                data["matches"][i]["fine"] = fine



        # Move the file pointer to the beginning of the file before writing
        ap.seek(0)
        
        # Write the updated data back to the file
        json.dump(data, ap, indent=4)

        # Truncate the file to the current file position to remove any extra data. because the file add some weird ]} in the end. 
        ap.truncate()

#find a match result ex ØB VEJGAARD: 2-1
def find_match_result(match_id,dbu_season_ID):
    match_result_url = "https://www.dbu.dk/resultater/kamp/" + match_id + "_"+dbu_season_ID+"/kampinfo"

    #request html code from dbu.dk
    match_result_html_request = requests.get(match_result_url)
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(match_result_html_request.text, 'html.parser')
    
    #Find which day the match is played
    matchDate = soup.find_all("div", {"class": "date"})
    matchDate = str(matchDate)
    matchDate = re.search(r'\d{2}-\d{2}-\d{4}', matchDate)
    matchDate = matchDate.group()
    matchDate = datetime.strptime(matchDate, "%d-%m-%Y")

    #Find the current date
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Compare dates
    if matchDate > today:        
        return False



    # Find all team lineup information
    match_result_info = soup.find_all("div", {"class": "sr--match--live-score--result"})
    
    # Extract text from HTML elements
    match_result_text = [info.get_text() for info in match_result_info]

    match_result_text = re.sub(r'\n\s*\n', '\n', match_result_text[0]).strip()

    # Split the string into lines
    lines = match_result_text.split('\n')
    print(lines)
    if "Øster Sundby" in lines[0]:
        # Extract scores for Øster Sundby B and the opponent
        #check if its not a number it return False
        if lines[2].isdigit():           
            oster_sundby_score = int(lines[2])
            opponent_score = int(lines[-3])
        else:
            return "postponed"
    else:
        if lines[-3].isdigit():
            oster_sundby_score = int(lines[-3])
            opponent_score = int(lines[2])
        else:
            return "postponed"
    # Storing scores in the desired format
    return  {'oester_sundby': oster_sundby_score, 'opponent': opponent_score}



def calculate_fine(result,won_match,draw_match,lost_match,conceded_goal,scored_goal):
    oeb = result["oester_sundby"]
    opp = result["opponent"]
   
    fine = 0

    #depends who won 
    fine += oeb_won(result,won_match,lost_match,draw_match)

    #scored goal fine
    fine += oeb * scored_goal
    fine += opp * conceded_goal

    return fine

def oeb_won(result,win,lose,draw):
    oeb = result["oester_sundby"]
    opp = result["opponent"]

    if(oeb > opp):
        return win
    elif(oeb < opp):
        return lose
    else:
        return draw
    


# RESET ALL PLAYER FINANCE JSON FILE + adding with active paying players list 
#Reset everything exepct for extra fines for exampel yellow cars og taberdømt kamp osv. 
def reset_fines(players_list):
    with open(player_finance_file_path,"r+",encoding="utf-8") as ap:
        data = json.load(ap)
        for i in range(players_list):
            data["payingPlayers"][i]["Dept"] = 0
            data["payingPlayers"][i]["Deposit"] = 0
            data["payingPlayers"][i]["balance"] = 0  

            # reset all extra fines
            # data["payingPlayers"][i]["extra_fines"]["others"] = []
            # data["payingPlayers"][i]["extra_fines"]["others_price"] = []

            

        # Move the file pointer to the beginning of the file before writing
        ap.seek(0)
        
        # Write the updated data back to the file
        json.dump(data, ap, indent=4)

        # Truncate the file to the current file position to remove any extra data. because the file add some weird ]} in the end. 
        ap.truncate()



#update player's dept in JSON file
def update_dept(playerlist,fine,len_of_players):
    with open(player_finance_file_path,"r+",encoding="utf-8") as ap:
        data = json.load(ap)

        for i in range(len_of_players):
            if (data["payingPlayers"][i]["dbu_name"] in playerlist):
                data["payingPlayers"][i]["Dept"] += fine
                ap.seek(0)  # Move the cursor to the beginning of the file
                json.dump(data, ap, indent=4)
                ap.truncate()  # Truncate the remaining data in the file


#Reads all transactions from the mobilepay box from the new season and update the player deposit
def update_player_deposit(playerlist,dbu_season_start_date):
    with open(trans_file_path,"r",encoding="utf-8") as ap:
        mobilepay_box_data = csv.reader(ap)

        #define the start season date to a datetime instead of string so it can be compared.
        dbu_season_start_date = datetime.strptime(dbu_season_start_date, "%d/%m/%Y")
        for row in mobilepay_box_data:
            # Extract the date string from the CSV row
            transfer_date_str = row[0].split(',')[0].strip()

            # Convert the date string to a datetime object
            transaction_date = datetime.strptime(transfer_date_str, "%d/%m/%Y %H:%M")

            if transaction_date > dbu_season_start_date:    
                #Row[1] is name 
                name = row[1]
                #Row[3] is deposit number
                deposit_number = int(row[5])
                if deposit_number < 0:
                    print(deposit_number,name)
                    continue
                print(name)

                for i in range(len(playerlist)):
                    player = playerlist[i]
                    if player == name:
                        with open(player_finance_file_path,"r+") as ap:
                            data = json.load(ap)
                            data["payingPlayers"][i]["Deposit"] += deposit_number
                            ap.seek(0)  # Move the cursor to the beginning of the file
                            json.dump(data, ap, indent=4)
                            ap.truncate()  # Truncate the remaining data in the file
                            break

def find_balance(yellow_card_fine,red_card_fine):
    with open(player_finance_file_path,"r+",encoding="utf-8") as ap:
        data = json.load(ap)

        for i in range(len(data["payingPlayers"])):
            dept = data["payingPlayers"][i]["Dept"]
            deposit = data["payingPlayers"][i]["Deposit"]
            red = int(data["payingPlayers"][i]["extra_fines"]["red_card"])
            yellow = int(data["payingPlayers"][i]["extra_fines"]["yellow_card"])

            extra_fines = data["payingPlayers"][i]["extra_fines"]["others_price"]
            if extra_fines:  # Check if the list is not empty
                total_extra_fines = sum(map(int, extra_fines))
            else:
                total_extra_fines  = 0  # Set total_extra_fines to 0 if the list is empty

            balance = deposit - dept - (red * red_card_fine) - (yellow * yellow_card_fine) - total_extra_fines
            data["payingPlayers"][i]["balance"] = balance

            ap.seek(0)  # Move the cursor to the beginning of the file
            json.dump(data, ap, indent=4)
            ap.truncate()  # Truncate the remaining data in the file


def mobilepay_box(season_start):
    #The total balance before season
    balance = 19
    send_money_to = []
    send_money_amount = []
    date = []
    with open(trans_file_path,"r",encoding="utf-8") as ap:
        mobilepay_box_data = csv.reader(ap)

        #define the start season date to a datetime instead of string so it can be compared.
        season_start = datetime.strptime(season_start, "%d/%m/%Y")
        for row in mobilepay_box_data:
            # Extract the date string from the CSV row
            transfer_date_str = row[0].split(',')[0].strip()

            # Convert the date string to a datetime object
            transaction_date = datetime.strptime(transfer_date_str, "%d/%m/%Y %H:%M")

            

            if transaction_date > season_start:    
                #Row[1] is name 
                name = row[1]
                #Row[3] is deposit number
                deposit_number = int(row[5])
                
                #Row[0] is date
                transfer_date = row[0]
                balance += deposit_number
                
                if(deposit_number < 0):
                    send_money_to.append(name)
                    send_money_amount.append(deposit_number)
                    date.append(transfer_date)

    with open(mobilepay_box_file_path,"r+",encoding="utf-8") as ap:
        data = json.load(ap)
        data["box"][0]["balance"] = balance
        data["box"][0]["send_money_to"] = send_money_to
        data["box"][0]["send_money_amount"] = send_money_amount
        data["box"][0]["date"] = date
         # Move the file pointer to the beginning of the file before writing
        ap.seek(0)
        
        # Write the updated data back to the file
        json.dump(data, ap, indent=4)

        # Truncate the file to the current file position to remove any extra data. because the file add some weird ]} in the end. 
        ap.truncate()