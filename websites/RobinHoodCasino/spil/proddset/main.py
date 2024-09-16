import flet as ft
import json


def getOddsetData():
    # https://api.the-odds-api.com/v4/sports/soccer_uefa_european_championship/odds/?apiKey=d24d8748a9826bebfa5b0a63c6362d76&regions=eu&markets=h2h,spreads
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data


def findMatchesTest():
    matchesList = [{"id": 0, "homeTeam": "Manchester United", "awayTeam": "Aab", "homeOdds": 2, "drawOdds": 1.5, "awayOdds": 3},{"id": 1, "homeTeam": "Liverpool", "awayTeam": "Chelsea", "homeOdds": 2.5, "drawOdds": 2.0, "awayOdds": 3.5}]
    match = {"id": 0, "homeTeam": "Manchester United", "awayTeam": "Aab", "homeOdds": 2, "drawOdds": 1.5, "awayOdds": 3}
    match1 = {"id": 1, "homeTeam": "Liverpool", "awayTeam": "Chelsea", "homeOdds": 2.5, "drawOdds": 2.0, "awayOdds": 3.5}
    match2 = {"id": 2, "homeTeam": "Arsenal", "awayTeam": "Tottenham", "homeOdds": 2.8, "drawOdds": 2.2, "awayOdds": 3.2}

    matchesList.extend([match, match1, match2])
    return matchesList

def findMatches():
    data = getOddsetData()
    matchesList = []

    # Iterate through each match entry in the JSON data
    for match in data:
        # Extract relevant information
        id = match["id"]
        home_team = match["home_team"]
        away_team = match["away_team"]
        odds = match["bookmakers"][0]["markets"][0]["outcomes"]

        home_odds = odds[0]["price"]     
        draw_odds = odds[1]["price"]         
        away_odds = odds[2]["price"]         

        match_dict = {
            "id": len(matchesList), 
            "homeTeam": home_team,
            "awayTeam": away_team,
            "homeOdds": home_odds,
            "drawOdds": draw_odds,
            "awayOdds": away_odds
        }
            
        matchesList.append(match_dict)
    return matchesList


def main(page: ft.page):
    page.scroll = "always"

    coupon_lst = ["test"]
    coupon_display = ft.Text("hej")
    page.add(coupon_display)

    def display_coupon(event):
        coupon_display = ft.Text(coupon_lst)
        page.update()

    def appendOdds(event, match, bet, odds):
        coupon_lst.append({match, bet, odds})
        display_coupon(None)

    def generateOddsFields(event):
        matches = findMatches()
        for match in matches[:5]:
            homeTeamLabel = ft.Text(value=f"{match.get("homeTeam")}   - ")
            awayTeamLabel = ft.Text(value=match.get("awayTeam"))
            homeOddsBtn = ft.ElevatedButton(text=match.get('homeOdds'), on_click=lambda e, m=match: appendOdds(e, m['id'], "1", m['homeOdds']))
            drawOddsBtn = ft.ElevatedButton(text=match.get('drawOdds'), on_click=lambda e, m=match: appendOdds(e, m['id'], "x", m['drawOdds']))
            awayOddsBtn = ft.ElevatedButton(text=match.get('awayOdds'), on_click=lambda e, m=match: appendOdds(e, m['id'], "2", m['awayOdds']))
            
            # Make them into a row
            matchRow = ft.Row(
                controls=[homeTeamLabel,awayTeamLabel,homeOddsBtn,drawOddsBtn,awayOddsBtn],
                spacing=10
            )
            # Insert the row into a container.
            matchContainer = ft.Container(
                content=matchRow,
                border=ft.border.all(1, "black"), 
                padding=10,  
                border_radius=5, 
                width=page.width * 0.4
            )
            page.add(matchContainer)


    # clickBtn = ft.ElevatedButton(text="click", on_click=generateOddsFields)
    # page.add(clickBtn)
    generateOddsFields(None)
    
ft.app(target=main)



