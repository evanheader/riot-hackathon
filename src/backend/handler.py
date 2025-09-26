import json

def lambda_handler(event, context):
    # fake recap data for now
    recap = {
        "games_played": 123,
        "most_played_champion": "Ahri",
        "winrate": "54%",
        "highlight": "Your best game had 15 kills and zero deaths!"
    }
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(recap)
    }
