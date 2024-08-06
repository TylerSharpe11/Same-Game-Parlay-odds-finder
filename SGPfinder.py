import requests
import pandas as pd

def get_markets(game_id):
    url = f"https://sib.nc.sportsbook.fanduel.com/api/sports/fixedodds/market/{game_id}"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "x-application": "FhMFpcPWXMeyZxOx"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def create_parlay_request(market1_id, selection1_id, market2_id, selection2_id):
    url = "https://sib.nc.sportsbook.fanduel.com/api/sports/fixedodds/transactional/v1/implyBets?"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "x-application": "FhMFpcPWXMeyZxOx"
    }
    body = {
        "betLegs": [
            {
                "legType": "SIMPLE_SELECTION",
                "betRunners": [{"runner": {"marketId": market1_id, "selectionId": selection1_id}}]
            },
            {
                "legType": "SIMPLE_SELECTION",
                "betRunners": [{"runner": {"marketId": market2_id, "selectionId": selection2_id}}]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()

def extract_odds(parlay_response):
    try:
        odds = parlay_response['betCombinations'][0]['winAvgOdds']['americanDisplayOdds']['americanOdds']
    except (KeyError, IndexError):
        odds = None
    return odds

def save_to_spreadsheet(results):
    df = pd.DataFrame(results)
    df.to_excel("parlay_odds.xlsx", index=False)

# Main
game_id = "your_game_id_here"
markets = get_markets(game_id)

results = []

for market1 in markets:
    for selection1 in market1['selections']:
        for market2 in markets:
            if market1 == market2:
                continue
            for selection2 in market2['selections']:
                parlay_response = create_parlay_request(market1['id'], selection1['id'], market2['id'], selection2['id'])
                odds = extract_odds(parlay_response)
                results.append({
                    "Market1_ID": market1['id'],
                    "Selection1_ID": selection1['id'],
                    "Market2_ID": market2['id'],
                    "Selection2_ID": selection2['id'],
                    "Odds": odds
                })

save_to_spreadsheet(results)
