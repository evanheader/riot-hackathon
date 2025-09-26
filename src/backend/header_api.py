import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ["RIOT_API_KEY"]
REGION = "na1"  # adjust to player region

def get_puuid_by_riot_id(game_name, tag_line):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": API_KEY}
    r = requests.get(url, headers=headers)
    return r.json().get("puuid")


def get_summoner_by_puuid(puuid):
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
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

if __name__ == "__main__":
    game_name = "joe schmoe"
    tag_line = "swag"
    puuid = get_puuid_by_riot_id(game_name, tag_line)
    if not puuid:
        print(f"Could not find PUUID for Riot ID {game_name}#{tag_line}")
        exit(1)
    summoner = get_summoner_by_puuid(puuid)
    match_ids = get_recent_matches(puuid, count=5)
    matches = [get_match_details(mid) for mid in match_ids]

    # Analyze matches for useful info
    champ_counts = {}
    wins = 0
    highlight = ""
    for match in matches:
        info = match.get("info", {})
        participants = info.get("participants", [])
        player = next((p for p in participants if p.get("puuid") == puuid), None)
        if not player:
            continue
        champ = player.get("championName", "Unknown")
        champ_counts[champ] = champ_counts.get(champ, 0) + 1
        if player.get("win"):
            wins += 1
        # Simple highlight: highest kills
        if not highlight or player.get("kills", 0) > highlight.get("kills", 0):
            highlight = player
    most_played_champ = max(champ_counts, key=champ_counts.get) if champ_counts else "Unknown"
    winrate = f"{wins}/{len(matches)} ({(wins/len(matches)*100 if matches else 0):.1f}%)"
    highlight_str = f"{highlight.get('championName', '')}: {highlight.get('kills', 0)} Kills, {highlight.get('deaths', 0)} Deaths, {highlight.get('assists', 0)} Assists"

    recap = {
        "summoner": summoner.get("name", game_name),
        "games_played": len(matches),
        "most_played_champion": most_played_champ,
        "winrate": winrate,
        "highlight": highlight_str
    }
    print(json.dumps(recap, indent=2))
