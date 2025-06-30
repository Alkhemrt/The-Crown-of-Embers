from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.player_state import player
from backend.battle_engine import start_battle_session, continue_battle
import importlib
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EVENTS_DIR = "events"

@app.get("/event")
def get_event(name: str):
    try:
        module = importlib.import_module(f"backend.{EVENTS_DIR}.{name}")
        return module.get_event()
    except Exception as e:
        print(f"Error loading event '{name}':", e)
        return {"text": "Failed to load event.", "options": [], "title": "ERROR", "footer": "Something broke."}

@app.get("/choose")
def choose(name: str, option: str):
    try:
        module = importlib.import_module(f"backend.{EVENTS_DIR}.{name}")
        return module.handle_choice(option)
    except Exception as e:
        print(f"Error handling choice '{option}' in event '{name}':", e)
        import traceback; traceback.print_exc()
        return {"text": "Failed to handle choice.", "options": [], "title": "ERROR", "footer": "Something broke."}

@app.get("/player")
def get_player():
    return {
        "gold": player.get("gold", 0),
        "inventory": player.get("inventory", []),
        "equipped": player.get("equipped", None),
        "damage": player.get("damage", 0),
        "hp": player.get("hp", 100),
        "xp": player.get("xp", 0),
        "level": player.get("level", 1)
    }

@app.post("/equip")
def equip_weapon(request: Request):
    data = request.query_params
    weapon_name = data.get("name")

    if player.get("equipped") == weapon_name:
        player["equipped"] = None
        player["damage"] = 0
        return {"success": True, "equipped": None, "damage": 0}

    for item in player["inventory"]:
        if item["name"] == weapon_name:
            player["equipped"] = weapon_name
            player["damage"] = item.get("damage", 0)
            return {"success": True, "equipped": weapon_name, "damage": player["damage"]}

    return {"success": False, "error": "Item not found"}

@app.get("/battle/start")
def battle_start(enemy_file: str):
    start_battle_session(enemy_file)
    return {"success": True}

@app.get("/battle/step")
def battle_step(action: str = "attack"):
    return continue_battle(action)