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




