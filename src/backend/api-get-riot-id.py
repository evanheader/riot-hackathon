import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv("RIOT_API_KEY")

gameName = "joe schmoe"
tagLine = "swag"

url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}" 
headers = {"X-Riot-Token": apiKey}

response = requests.get(url, headers=headers) 
data = response.json()

print("PUUID:", data["puuid"]) 
print("GameName:", data["gameName"]) 
print("TagLine:", data["tagLine"])