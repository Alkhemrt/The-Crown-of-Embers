import json
import os
import random
from backend.player_state import player, save_player 


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
        "player_effects": [],
        "enemy_effects": [],
        "queued_move": default_move,
        "next_move_warning": None
    }

    save_player(player)


def has_effect(effects, name):
    return any(effect["name"] == name for effect in effects)


def apply_effect(effects, name, turns=2):
    effects.append({"name": name, "turns": turns})


def tick_effects(effects):
    remaining = []
    for effect in effects:
        effect["turns"] -= 1
        if effect["turns"] > 0:
            remaining.append(effect)
    return remaining


def effect_list_text(effects):
    names = list(set(effect["name"] for effect in effects))
    return ", ".join(names) if names else "none"


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

    state["player_effects"] = tick_effects(state.get("player_effects", []))
    state["enemy_effects"] = tick_effects(state.get("enemy_effects", []))

    player_defending = False
    player_stunned = has_effect(state["player_effects"], "Stun")

    if player_stunned:
        log.append("You're stunned and can't act this turn!")
    else:
        if action == "defend":
            player_defending = True
            log.append("You brace yourself and defend, reducing incoming damage!")
        elif action == "attack":
            dmg = player.get("damage", 1)

            if has_effect(state["player_effects"], "Weakness"):
                dmg = max(1, dmg - 2)
                log.append("You're weakened! Your damage is reduced.")

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
        save_player(player)
        return {
            "log": log,
            "outcome": "win",
            "level_up": level_up
        }

    enemy_stunned = has_effect(state["enemy_effects"], "stun")
    move = state.get("queued_move", {"name": "Idle", "damage": 0})

    if enemy_stunned:
        log.append(f"The {state['enemy']['name']} is stunned and skips their turn!")
    elif move["name"] == "Defend":
        state["enemy_defending"] = True
        log.append(f"The {state['enemy']['name']} is preparing to defend!")
    elif move["damage"] > 0:
        dmg = move["damage"]
        if player_defending:
            dmg = max(1, dmg // 2)
        state["player_hp"] -= dmg
        log.append(f"The {state['enemy']['name']} uses {move['name']} for {dmg} damage!")

        if 'effect' in move:
            effect_name = move["effect"]
            apply_effect(state["player_effects"], effect_name)
            log.append(f"You are affected by {effect_name}!")

    player["hp"] = state["player_hp"] = max(0, state["player_hp"])

    if state["player_hp"] <= 0:
        log.append("You were defeated...")
        player["battle"] = None
        save_player(player)
        return {
            "log": log,
            "outcome": "lose"
        }

    behavior = state["enemy"].get("behavior", "neutral")
    next_action = "attack"
    if enemy_stunned:
        next_action = "idle"
    elif behavior == "aggressive":
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
    elif next_action == "idle":
        next_move = {"name": "Idle", "damage": 0}
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
    spacer.append(f"Status effects: {effect_list_text(state['player_effects'])}")

    log.extend(spacer)

    save_player(player) 
    return {
        "log": log,
        "outcome": None
    }
