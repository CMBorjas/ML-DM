from sqlalchemy import create_engine
from app.models import Base

def initialize_database():
    engine = create_engine('sqlite:///data/database.db')
    Base.metadata.create_all(engine)
    print("Database initialized!")

if __name__ == "__main__":
    initialize_database()
