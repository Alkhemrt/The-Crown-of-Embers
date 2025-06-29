import json
import os
import random
from backend.player_state import player


def load_enemy(file_name):
    path = os.path.join(os.path.dirname(__file__), "enemies", file_name)
    with open(path, "r") as f:
        return json.load(f)


def start_battle_session(enemy_file):
    enemy = load_enemy(enemy_file)

    default_move = {"name": "Idle", "damage": 0}
    player["battle"] = {
        "enemy": enemy,
        "enemy_hp": enemy["hp"],
        "player_hp": player.get("hp", 100),
        "log": [],
        "enemy_defending": False,
        "queued_move": default_move,
        "next_move_warning": None
    }


def continue_battle(action="attack"):
    if not player.get("battle"):
        return {"error": "No battle in progress."}

    player.setdefault("xp", 0)
    player.setdefault("gold", 0)
    player.setdefault("level", 1)
    player.setdefault("max_hp", 100)
    player.setdefault("hp", player["max_hp"])

    state = player["battle"]
    log = []
    spacer = []

    player_defending = False
    if action == "defend":
        player_defending = True
        log.append("You brace yourself and defend, reducing incoming damage!")
    elif action == "attack":
        dmg = player.get("damage", 1)
        if state.get("enemy_defending"):
            dmg = max(1, dmg // 2)
            log.append(f"The {state['enemy']['name']} was defending and reduced your damage!")
            state["enemy_defending"] = False
        state["enemy_hp"] -= dmg
        log.append(f"You hit the {state['enemy']['name']} for {dmg} damage!")
    else:
        return {"error": f"Unknown action: {action}"}

    if state["enemy_hp"] <= 0:
        log.append(f"You defeated the {state['enemy']['name']}!")

        xp_gain = random.randint(*state["enemy"].get("xp", [5, 15]))
        gold_gain = random.randint(*state["enemy"].get("gold", [5, 18]))

        player["xp"] += xp_gain
        player["gold"] += gold_gain
        log.append(f"You gained {xp_gain} XP and {gold_gain} gold!")

        level_up = False
        xp_needed = 20 + player["level"] * 10
        while player["xp"] >= xp_needed:
            player["xp"] -= xp_needed
            player["level"] += 1
            player["max_hp"] += 10
            player["hp"] = player["max_hp"]
            level_up = True
            log.append(f"You leveled up to Level {player['level']}! Max HP increased to {player['max_hp']}.")
            xp_needed = 20 + player["level"] * 10

        player["battle"] = None
        return {
            "log": log,
            "outcome": "win",
            "level_up": level_up
        }

    move = state.get("queued_move", {"name": "Idle", "damage": 0})
    if move["name"] == "Defend":
        state["enemy_defending"] = True
        log.append(f"The {state['enemy']['name']} is defending!")
    elif move["damage"] > 0:
        dmg = move["damage"]
        if player_defending:
            dmg = max(1, dmg // 2)
        state["player_hp"] -= dmg
        log.append(f"The {state['enemy']['name']} uses {move['name']} for {dmg} damage!")

    player["hp"] = state["player_hp"] = max(0, state["player_hp"])

    if state["player_hp"] <= 0:
        log.append("You were defeated...")
        player["battle"] = None
        return {
            "log": log,
            "outcome": "lose"
        }

    behavior = state["enemy"].get("behavior", "neutral")
    next_action = "attack"
    if behavior == "aggressive":
        if random.random() < 0.1:
            next_action = "defend"
    elif behavior == "defensive":
        if random.random() < 0.4:
            next_action = "defend"
    else:
        if random.random() < 0.25:
            next_action = "defend"

    if next_action == "defend":
        next_move = {"name": "Defend", "damage": 0}
        state["next_move_warning"] = None
    else:
        next_move = random.choice(state["enemy"]["moves"])
        state["next_move_warning"] = next_move.get("warn")

    state["queued_move"] = next_move

    spacer.append("")
    spacer.append("")
    if state.get("next_move_warning"):
        spacer.append(state["next_move_warning"])
    spacer.append(f"Enemy HP: {state['enemy_hp']} / {state['enemy']['hp']}")

    log.extend(spacer)

    return {
        "log": log,
        "outcome": None
    }
