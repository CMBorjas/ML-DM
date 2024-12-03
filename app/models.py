from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

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
