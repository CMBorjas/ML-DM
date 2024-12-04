import os
import json
import random
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

# Path to the NPC storage file
NPC_FILE_PATH = os.path.join("data", "campaign", "npcs.json")

# Ensure the data directory exists
if not os.path.exists(NPC_FILE_PATH):
    with open(NPC_FILE_PATH, "w") as file:
        json.dump([], file) # Start with an empty list

Base = declarative_base()

class Player(Base):
    """
    Represents a player in the campaign.
    """
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stats = Column(JSON)  # Assuming stats are stored as JSON
    inventory = Column(JSON)  # Inventory items stored as JSON
    actions = Column(JSON)  # Player actions stored as JSON

    def __repr__(self):
        return f"<Player(id={self.id}, name={self.name}, stats={self.stats})>"


def generate_npc(name="Azaavara"):
    """
    Generate a random NPC with predefined templates and random values.
    """
    npc = {
        "name": name,
        "race": random.choice(["dragonborn", "dwarf", "elf", "gnome", "half-elf", "half-orc", "halfling", "human", "tiefling"]),
        "class": random.choice(["Artificer","Barbarian","Bard","Cleric","Druid", "Fighter","Monk","Paladin","Ranger","Rogue","Sorcerer","Warlock","Wizard"]),
        "level": random.randint(1, 20),
        "stats": {
            "STR": random.randint(8, 18),
            "DEX": random.randint(8, 18),
            "CON": random.randint(8, 18),
            "INT": random.randint(8, 18),
            "WIS": random.randint(8, 18),
            "CHA": random.randint(8, 18),
        },
        "abilities": ["Darkvision", "Healing Hands", "Radiant Soul"],
        "languages": ["Common", "Celestial"],
        "spells": ["Message", "Light", "Dominate Monster", "Crown of Madness"],
        "special_abilities": [
            "Fame and Glamour: Renowned performer with incredible charm.",
            "Radiant Soul: Gain radiant wings for a short duration.",
        ],
    }

    # Save NPC to file
    with open(NPC_FILE_PATH, "r") as file:
        npcs = json.load(file)
    
    # Append the new NPC to the list
    npcs.append(npc)

    # Save the updated list back to the file
    with open(NPC_FILE_PATH, "w") as file:
        json.dump(npcs, file, indent=4)

    return npc

# Function to get all NPCs ----------------------------------------------------------------------------------------------------------------------------------
def get_all_npcs():
    """
    Fetch all NPCs from the storage file.
    """
    # Ensure the file exists and is initialized
    if not os.path.exists(NPC_FILE_PATH):
        with open(NPC_FILE_PATH, "w") as file:
            json.dump([], file)  # Initialize with an empty list

    with open(NPC_FILE_PATH, "r") as file:
        return json.load(file)
