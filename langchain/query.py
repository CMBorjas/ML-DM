from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Player  # Assuming models.py defines your database models

# Database connection setup
engine = create_engine('sqlite:///../data/database.db')
Session = sessionmaker(bind=engine)
session = Session()

def get_player_profile(player_id):
    """
    Retrieve a player's profile from the database.
    """
    player = session.query(Player).filter_by(id=player_id).first()
    if player:
        return {
            "id": player.id,
            "name": player.name,
            "stats": player.stats,
            "inventory": player.inventory,
            "actions": player.actions
        }
    return None
