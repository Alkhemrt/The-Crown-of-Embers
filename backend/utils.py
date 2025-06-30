import json
import os

def load_weapon(weapon_id):
    path = os.path.join(os.path.dirname(__file__), "weapons", f"{weapon_id}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Weapon '{weapon_id}' not found.")
    with open(path, "r") as f:
        return json.load(f)
