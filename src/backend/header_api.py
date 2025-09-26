import os
import json
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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

def get_recent_matches(puuid):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": API_KEY}
    r = requests.get(url, headers=headers)
    return r.json()

def get_match_details(match_id):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    r = requests.get(url, headers=headers)
    return r.json()

@app.route('/recap', methods=['GET'])
def recap():
    game_name = request.args.get('gameName')
    tag_line = request.args.get('tagLine')
    if not game_name or not tag_line:
        return jsonify({'error': 'Missing gameName or tagLine'}), 400
    puuid = get_puuid_by_riot_id(game_name, tag_line)
    if not puuid:
        return jsonify({'error': f'Could not find PUUID for Riot ID {game_name}#{tag_line}'}), 404
    summoner = get_summoner_by_puuid(puuid)
    match_ids = get_recent_matches(puuid)
    matches = [get_match_details(mid) for mid in match_ids]

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
    return jsonify(recap)

if __name__ == "__main__":
    app.run(debug=True)
