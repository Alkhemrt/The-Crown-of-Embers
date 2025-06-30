from backend.utils import load_weapon
from backend.player_state import player

visited_choices = set()

def get_event():
    player.clear()
    player.update({
        "gold": 0,
        "inventory": [],
        "equipped": None,
        "damage": 0
    })

    return {
        "text": (
            "The stone beneath you is cold, cracked by time and weathered by silence. Your fingers twitch, stiff with the weight of years, as breath returns to your lungs like something long forgotten. The chapel around you is broken, its roof torn open, its walls half-swallowed by ivy and rot. Above, the sky looms black and endless, its walls half-swallowed by ivy and rot. Above, the sky looms black and endless, a starless void where only the pale moon lingers like an eye that never closes.\n"
            "\n"
        ),
        "options": ["Sit up"],
        "title": "------------------------------------- Awaking from Stone -------------------------------------",
        "footer": "Not all that crumbles is dead."
    }

def handle_choice(option: str):
    if option == "Who are you?":
        weapon = load_weapon("rusty_sword")
        player["inventory"].append(weapon)
        player["gold"] += 5



def handle_choice(option: str):
    global visited_choices
    option = option.strip()

    if option.lower() == "sit up":
        visited_choices = set()
        return {
            "text": (
                "You sit up slowly, your body heavy with the weight of what feels like an eternity spent in stone. Dust clings to your skin. Your armor is dull and pitted, marked by time more than battle. All around you, the shattered statues of your brothers and sisters lie in pieces. Some still wear their helmets. Some are missing heads or limbs. You still remember their names even now. \n"
                "\n"
                "\n"
                "You’re not sure what year it is. You’re not even sure if you are still alive in the way you once were. \n"
            ),
            "options": _get_remaining_options(),
            "title": "------------------------------------- Awaking from Stone -------------------------------------",
            "footer": "Not all that crumbles is dead.",
            "next_event": None
        }

    elif option in {"Stand up", "Inspect the statues", "Call out"}:
        visited_choices.add(option)

        if option == "Stand up":
            text = (
                "You push yourself to your feet, unsteady at first, as your legs remember how to move. Your joints groan in protest, metal scraping against stone. The air feels thinner than you remember. You take a breath and feel the dust settle in your lungs like ash. There is no one here. No sound answers you. Just the broken chapel, and the moon staring down. \n"
            )
        elif option == "Inspect the statues":
            text = (
                "You move toward the nearest shattered figure, kneeling beside the stone fragments. A gauntlet lies near its hand. His face is split down the middle, the statue's eyes forever wide in silent warning. Another lies with its helm caved in, as though something struck it from above. \n"
            )
        elif option == "Call out":
            text = (
                "Your voice breaks the silence, rough and unused. It echoes once off the chapel walls, then fades into the night beyond. No answer comes. Only wind. \n"
            )

        options = _get_remaining_options()

        if options == ["Exit the chapel"]:
            text += (
                "There is probably nothing more to do here. You notice the broken archway at the far end of the chapel, where moonlight spills like silver blood across the stone floor. The great doors, once sealed, are now slightly ajar. \n"
                "\n"
            )

        return {
            "text": text,
            "options": options,
            "title": "------------------------------------- Awaking from Stone -------------------------------------",
            "footer": "Not all that crumbles is dead.",
            "next_event": None
        }

    elif option == "Exit the chapel":
        return {
            "text": "",
            "options": [],
            "title": "",
            "footer": "",
            "next_event": "exiting_the_chapel"
        }

def _get_remaining_options():
    base_options = ["Stand up", "Inspect the statues", "Call out"]
    remaining = [opt for opt in base_options if opt not in visited_choices]

    if not remaining:
        return ["Exit the chapel"]
    return remaining
