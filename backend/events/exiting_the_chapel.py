from backend.player_state import player
from backend.utils import load_weapon

def get_event():
    return {
        "title": "------------------------------------- Edge of the Forest -------------------------------------",
        "text": (
            "You step out beneath the open sky, your boots sinking slightly into the damp earth. The chapel looms behind you, a fading relic pressed against the edge of a black forest. Its trees stand silent and watchful. The air is cold, thick with the scent of moss, rust, and rain that never quite falls.\n"
            "\n"
            "\n"
            "\n"
            "Someone stands near the treeline."
        ),
        "options": ["Approach him"],
        "footer": "The sun is gone. The moon watches in silence."
    }


def handle_choice(option: str):
    if option == "Approach him":
        return {
            "title": "------------------------------------- Edge of the Forest -------------------------------------",
            "text": (
                "A thin man in a ragged cloak stands at the edge of the forest, hood drawn low over his face. A lantern swings from his belt, casting flickers of pale light on hollow cheeks and weathered skin. \n"
                "\n"
                "“Finally, one of you wakes,” he says. “I waited ten years, watching this place. Ever since the crown vanished and the sky turned to ash. They said none would ever wake. That the Wardens were stone forever. But look at you.”"
                "\n"
            ),
            "options": ["What are you talking about?"],
            "footer": "The sun is gone. The moon watches in silence."
        }

    elif option == "What are you talking about?":
        return {
            "title": "------------------------------------- Edge of the Forest -------------------------------------",
            "text": (
                "“Ah. So the sleep took your memories too,” he mutters. “Doesn’t matter. What matters is the crown. It’s gone, and with it, everything else. Light. Order. All of it.” \n"
                "\n"
                "He turns and gestures eastward, toward the shadowed forest.\n"
                "\n"
                "“Go east, through the woods. Past the river. Find the city of Vehlmoor. Ask for a man named Kael. He remembers more than I do. He’ll help you.” \n"
                "\n"
            ),
            "options": ["Who are you?"],
            "footer": "The sun is gone. The moon watches in silence."
        }

    elif option == "Who are you?":
        weapon = load_weapon("rusty_sword")
        player["inventory"].append(weapon)
        player["gold"] += 50

        return {
            "title": "------------------------------------- Edge of the Forest -------------------------------------",
            "text": (
                "“Knowing who I am won’t change what’s coming,” he says.\n"
                "\n"
                "From beneath his cloak, he draws a bundle, your hand closes around it instinctively. A few worn gold coins. A sword with a cracked hilt and a blade dulled by years of disuse.\n"
                "\n"
                "“This won’t get you far, but it’ll get you started. Don’t die. This world’s already had enough of that.” \n"
                "\n"
                "Without another word, he turns and walks into the woods, swallowed by mist and shadow before you can speak again."
            ),
            "options": ["Look at the path ahead"],
            "footer": "The sun is gone. The moon watches in silence."
        }
    
    elif option == "Look at the path ahead":
        return {
            "title": "------------------------------------- Edge of the Forest -------------------------------------",
             "text": ( 
                "Ahead lies the forest. The path east cuts straight through it. The air there feels wrong, It would be the quickest way, but not the safest.\n"
                "\n"
                "Or you could keep to the outskirts, tracing the edge of the woods and circling around. It’ll take longer, but the shadows might be thinner there… if only by a little.\n"
             ),    
            "options": ["Go east, directly through the forest", "Travel along the outskirts of the forest"],
            "footer": "The sun is gone. The moon watches in silence."    
        }



    elif option == "Go east, directly through the forest":
        return {
            "text": "",
            "options": [],
            "title": "",
            "footer": "",
            "next_event": "going_east"
        }
    
    elif option == "Travel along the outskirts of the forest":
        return {
            "text": "",
            "options": [],
            "title": "",
            "footer": "",
            "next_event": "forest_outskirts"
        }


    else:
        return {
            "title": "Error",
            "text": "The forest doesn’t understand that choice.",
            "options": [],
            "footer": "The sun is gone. The moon watches in silence."
        }
