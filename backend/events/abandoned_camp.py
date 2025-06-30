from backend.player_state import player
from backend.utils import load_weapon

def get_event():
    return {
        "title": "------------------------------------- The Abandoned Camp -------------------------------------",
        "text": (
            "The forest begins to thin, just enough for you to move more freely, and after another stretch of silence and damp earth underfoot, you spot a faint glow ahead.\n"
            "\n"
            "It’s a campfire, or what’s left of one, just a few glowing embers nestled in a ring of dark stone. The air still carries the scent of smoke. A half-eaten meal sits on a wooden plate nearby, cold but not yet spoiled, and a threadbare blanket is folded with care beside a log, as if its owner meant to return."
            "\n"
            "Suddenly, a scream cuts through the stillness. You turn toward it and spot a cave, half-hidden behind a wall of ivy and stone. \n"
            "The fire crackles softly in the background.\n"
        ),
        "options": ["Search the camp for supplies or clues", "Head toward the cave", "Keep moving east"],
        "footer": "The sun is gone. The moon watches in silence."
    }


def handle_choice(option: str):
    if option == "Search the camp for supplies or clues":
        weapon = load_weapon("bluewrap_knife")
        player["inventory"].append(weapon)
        player["gold"] += 6
        return {
            "title": "------------------------------------- The Abandoned Camp -------------------------------------",
            "text": (
                "You crouch beside the campfire, brushing aside the ash and old leaves. The warmth still clings to the stones. Whoever built this fire was here within the last few hours. \n"
                "\n"
                "You sift through what’s been left behind. A worn satchel yields a few gold coins, which you pocket. Beneath the blanket you find a small knife, used but clean, with a handle wrapped in faded blue cloth. Not much for a fight, but it might serve if needed.\n"
                "\n"
                "What catches your eye last is a folded scrap of parchment near the bowl. The ink is smeared, but a few lines remain legible:\n"
                "\n"
                "“...he followed me from the ruins. Eyes like cinders. I don’t think I’ll make it to Vehlmoor. If anyone finds this, please tell my daughter, Elira, what became of me.”\n"
                "\n"
                "The writing trails off violently. The parchment is torn.\n"
                "\n"
                "You glance toward the cave again. It yawns open beneath the ivy like a mouth full of breathless dark. If something followed the writer here, it might still be close.\n"
            ),
            "options": ["Head toward the cave", "Keep moving east"],
            "footer": "The sun is gone. The moon watches in silence."
        }

    elif option == "Head toward the cave":
        return {
            "title": "------------------------------------- The Abandoned Camp -------------------------------------",
            "text": (
                "You push aside the curtain of ivy and step into the cave. It smells of damp rot and iron. The air grows noticeably colder, and the scent intensifies as you move deeper, your boots crunching softly on bone-dry gravel.\n"
                "\n"
                "Something breaks the silence. Wet, tearing sounds. Chewing. Low, rasping breaths, rising from the darkness ahead."
                "\n"
                "The cave widens. Moonlight from a crack above spills down onto the stone floor. You see a body.\n"
                "\n"
                "What’s left of the man from the camp lies sprawled across the rocks, his throat torn open, one hand still clutching his sword. Standing over him is a creature like nothing you've ever seen. Part wolf, part bear, grotesquely large.\n"
                "\n"
                "It looks up. Eyes like dying coals. It's jaw slick with blood. Its body is stretched thin and raw-looking, ribs sharp under its hide, claws clacking on the stone as it shifts its weight.\n"
                "\n"
                "It doesn’t move. It just watches you for a long, breathless moment as you stand frozen in place. Then it launches itself at you.\n"
            ),
            "options": ["FIGHT"],
            "footer": "The sun is gone. The moon watches in silence."
        }

    elif option == "FIGHT":
        return {
            "battle": True,
            "enemy_file": "gravefang.json",
            "return_event": "abandoned_camp",
            "post_battle_choice": "GravefangFightOutcome"
        }

    elif option == "GravefangFightOutcome":
        return {
            "title": "------------------------------------- The Abandoned Camp -------------------------------------",
            "text": (
                "The Gravefang lets out a strangled, bone-deep snarl as it collapses in a broken heap beside the body. Its limbs twitch once, twice, then goes still. \n"
                "\n"
                "You stagger back, chest heaving, body burning from the fight. The cave is silent now. You’re alive. You beat it."
                "\n"
                "You notice the sword in the fallen man's hand. You kneel beside him. The blade is old but well-cared for, the hilt wrapped in black leather, the edge still sharp. But to take it would mean prying it from his fingers.\n"
            ),
            "options": ["Take the sword from his hand", "Pay your respects and leave"],
            "footer": "The sun is gone. The moon watches in silence."
        }
    
    elif option == "Take the sword from his hand":
        weapon = load_weapon("traveler_blade")
        player["inventory"].append(weapon)
        return {
            "title":"------------------------------------- The Abandoned Camp -------------------------------------",
            "text": (
                "You reach down and grip the sword. His fingers are stiff, locked in place, but as you pull, they loosen—slowly, without resistance.\n"
                "\n"
                "The weapon is heavier than yours. It's solid, well-balanced and clearly built to last. The edge is clean and sharp, far better than your rusted blade. You test its weight. It feels good in your hand. \n"
                "\n"
                "Whatever his name was, he won't be needing it now. But you will.\n"
                "\n"
                "You rise, sword in hand, and step away from the body. The cave is silent as you turn and continue toward Vehlmoor. \n"
            ),
            "options": ["Continue"],
            "footer": "The sun is gone. The moon watches in silence."
        }
    
    elif option == "Pay your respects and leave":
        return {
            "title":"------------------------------------- The Abandoned Camp -------------------------------------",
            "text": (
                "You kneel beside the fallen man, bowing your head. His hand still clutches the sword tight, even in death. You don’t touch it.\n"
                "\n"
                "“You fought to the end. May you rest,” you say.\n"
                "\n"
                "You rise and step away from the body. The cave is silent as you turn and continue toward Vehlmoor. \n"
            ),
            "options": ["Continue"],
            "footer": "The sun is gone. The moon watches in silence."
        }

    elif option == "Keep moving east":
        return {
            "title": "-------------------------------------- The Abandoned Camp -------------------------------------",
            "text": (
                "You cast one last glance at the abandoned camp and decide to move on.\n"
                "\n"
            ),
            "options": ["Continue"],
            "footer": "The sun is gone. The moon watches in silence."
        }



    elif option == "Continue":
        return {
            "text": "",
            "options": [],
            "title": "",
            "footer": "",
            "next_event": "weaw"
        }

    else:
        return {
            "title": "Error",
            "text": "The forest doesn’t understand that choice.",
            "options": [],
            "footer": "The sun is gone. The moon watches in silence."
        }
