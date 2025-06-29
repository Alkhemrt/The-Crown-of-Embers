from backend.player_state import player
from backend.utils import load_weapon

def get_event():
    return {
        "title": "------------------------------------- Heading East -------------------------------------",
        "text": (
            "The trees rise tall and crooked.  The moon above follows you, distant and pale, but most of its light is eaten by the thick canopy. What little filters through pools in patches on the forest floor, faint and cold. \n"
            "\n"
            "You walk for what feels like hours. The forest seems to shift behind you. You hear branches creak somewhere off to your right. Then again, behind you. The sound stays just far enough behind to be uncertain. When you pause, it fades. When you walk, it resumes. \n"
            "\n"
        ),
        "options": ["Turn and face whatever’s behind you", "Keep walking"],
        "footer": "The sun is gone. The moon watches in silence."
    }


def handle_choice(option: str):
    if option == "Turn and face whatever’s behind you":
        return {
            "title": "------------------------------------- Heading East -------------------------------------",
            "text": (
                "You stop where you stand, and slowly turn to face the path you came from. \n"
                "You see a shape, low to the ground and wrong in the way it moves, crawls just at the edge of sight. The way it shifts its limbs makes it clear it isn’t human, though it may have been once. \n"
                "\n"
                "You reach for your weapon as it lock eyes with you. \n"    
            ),
            "options": ["FIGHT"],
            "footer": "The sun is gone. The moon watches in silence."
        }

    elif option == "Keep walking":
        return {
            "title": "------------------------------------- Heading East -------------------------------------",
            "text": (
                "You press on, one foot after the other, careful not to break twigs or kick stones. The sound behind you continues, soft but steady. You resist the urge to glance back as you keep walking forward."
                "You step into a small clearing, and above you the canopy opens like a wound. The moonlight pours down in full now, pale and heavy, lighting the space with cold silver. You take a breath and look behind you."
                "\n"
                "You see a shape, low to the ground and wrong in the way it moves, crawls just at the edge of sight. The way it shifts its limbs makes it clear it isn’t human, though it may have been once. \n"
                "\n"
                "You reach for your weapon as it lock eyes with you. \n"    
            ),
            "options": ["FIGHT"],
            "footer": "The sun is gone. The moon watches in silence."
        }

    elif option == "FIGHT":
        return {
            "battle": True,
            "enemy_file": "ghoul.json",
            "return_event": "going_east",
            "post_battle_choice": "GhoulFightOutcome"
        }

    elif option == "GhoulFightOutcome":
        return {
            "title": "------------------------------------- Heading East -------------------------------------",
            "text": (
                "The thing lets out a rasping hiss as it collapses at your feet. You stand over it, breathing heavy. Whatever it was, it's dead now."
                "\n"
                "\n"
                "Its body begins to wither almost instantly, the flesh pulling tight across its bones before flaking away like ash caught in a breeze. There’s no blood. No sign it was ever alive in the first place. Just a foul-smelling smear on the forest floor."
                "\n"
                "\n"
                "You take a breath, steady your grip, and keep moving. Vehlmoor lies past this forest, east through the dark."
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
            "next_event": "next_event"
        }

    else:
        return {
            "title": "Error",
            "text": "The forest doesn’t understand that choice.",
            "options": [],
            "footer": "The sun is gone. The moon watches in silence."
        }
