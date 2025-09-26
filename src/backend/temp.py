import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ["RIOT_API_KEY"]
REGION = "na1"  # adjust to player region

def get_summoner(summoner_name):
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {"X-Riot-Token": API_KEY}
    r = requests.get(url, headers=headers)
    return r.json()

def get_recent_matches(puuid, count=5):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    headers = {"X-Riot-Token": API_KEY}
    r = requests.get(url, headers=headers)
    return r.json()

def get_match_details(match_id):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    r = requests.get(url, headers=headers)
    return r.json()

def get_puuid_by_riot_id(game_name, tag_line):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": API_KEY}
    r = requests.get(url, headers=headers)
    return r.json().get("puuid")

def lambda_handler(event, context):
    params = event.get("queryStringParameters", {})
    if "gameName" in params and "tagLine" in params:
        puuid = get_puuid_by_riot_id(params["gameName"], params["tagLine"])
        if not puuid:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Could not find puuid for Riot ID."})
            }
        summoner = get_summoner_by_puuid(puuid)
    else:
        summoner_name = params.get("name", "Faker")
        summoner = get_summoner(summoner_name)
        puuid = summoner.get("puuid")
    if not puuid:
        print("Summoner API response:", summoner)
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Could not find summoner or puuid.", "response": summoner})
        }
    match_ids = get_recent_matches(puuid)
    recent_games = [get_match_details(mid) for mid in match_ids]

    recap = {
        "summoner": summoner.get("name", params.get("gameName", "Unknown")),
        "games_played": len(recent_games),
        "recent_matches": recent_games
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(recap)
    }

# Helper to get summoner by puuid

def get_summoner_by_puuid(puuid):
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}
    r = requests.get(url, headers=headers)
    return r.json()

if __name__ == "__main__":
    result = get_puuid_by_riot_id("header","evan")
    
    print(result)
