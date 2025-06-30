import os
import json

PLAYER_FILE = os.path.join(os.path.dirname(__file__), "player_data.json")

def load_player():
    if os.path.exists(PLAYER_FILE):
        with open(PLAYER_FILE, "r") as f:
            return json.load(f)
    return {
        "hp": 100,
        "max_hp": 100,
        "xp": 0,
        "level": 1,
        "gold": 0,
        "damage": 1,
        "inventory": [],
        "equipped": None,
        "battle": None
    }

def save_player(data):
    with open(PLAYER_FILE, "w") as f:
        json.dump(data, f, indent=2)

player = load_player()
