# ML-DM
An AI-driven tool designed for Dungeon Masters (DMs) in tabletop role-playing games. 

## Project description
Proposal: AI-Powered Dungeon Master Assistant with RAG
High-Level Concept: An AI-driven tool designed for Dungeon Masters (DMs) in tabletop role-playing games. The tool will leverage LangChain's Retrieval-Augmented Generation (RAG) to fetch relevant information from a campaign database and enhance storytelling in real-time. Using LLMs, the assistant will generate narrative suggestions, enemy encounters, and loot tailored to the game's current state based on prior campaign history and player choices.
Front End: A Flask web interface enables Dungeon Masters to manage game sessions, import custom maps, and view AI-generated suggestions in real-time. The interface will allow for intuitive interaction, such as token placement on a visual map and dialogue generation for non-player characters (NPCs).
Database:
*	Player Profiles: Stores character information 
    * Stats, Skills, Background
    * Inventory
    * Actions
*	Campaign Logs: Stores the narrative history, encounters, and NPC details.
*	Map Data: Contains custom maps and layouts for encounters.
The Retrieval-Augmented Generation (RAG) model will retrieve relevant parts of the campaign history to generate contextually appropriate suggestions for ongoing gameplay.
Tools:
*	LangChain: To query the campaign database using RAG and generate context-aware narratives based on the retrieved information.
    *	Example: “Jenny (Witch in the woods):  I have a request for you complete. I need a live troll to study their habits, and to fortify the defenses of the kingdom”
*	Langflow: To integrate the LLM with the database and ensure smooth retrieval of campaign data in real time.
    *	Example: A player defeats a key NPC, which is stored in the database. When the DM asks for a follow-up encounter, the LLM knows not to suggest that NPC, thanks to the real-time update. This can also come up as a negative later on if the players defeat enough NPCs to trigger consequences in the campaign. It should also be able to move some story beats to other living NPC’s. 


## Folder structure

```
ML-DM/
│
├── notebooks/
│   └── main.ipynb                    # Main Jupyter Notebook for prototyping the application
│
├── app/                              # Flask application folder
│   ├── __init__.py                   # Initialize Flask app
│   ├── routes.py                     # Define API routes for the frontend
│   ├── templates/                    # HTML templates for Flask (frontend)
│   │   └── index.html                # Main webpage for Dungeon Master interaction
│   ├── static/                       # Static files for the frontend
│   │   ├── css/                      # CSS files for styling
│   │   ├── js/                       # JavaScript files
│   │   └── images/                   # Images, icons, etc.
│   ├── maps/                         # Folder for custom maps uploaded by DMs
│   └── uploads/                      # Temporary folder for file uploads
│
├── data/                             # Data-related folders
│   ├── database.db                   # SQLite database (or equivalent) for campaign storage
│   ├── schema.sql                    # SQL schema for database structure
│   ├── campaign/                     # Campaign data storage
│   │   ├── players.json              # Player profiles data
│   │   ├── logs.json                 # Campaign narrative logs
│   │   └── maps.json                 # Maps metadata
│   └── corpus/                       # Corpus of text data for training the RAG model
│
├── langchain/                        # LangChain-related files
│   ├── query.py                      # Code to query the database using RAG
│   ├── config.py                     # Configuration file for LangChain
│   ├── prompts/                      # Custom prompt templates for LangChain
│   │   ├── npc_dialogue.txt          # Prompt for NPC dialogue generation
│   │   ├── encounter_suggestions.txt # Prompt for encounter generation
│   │   └── loot_generation.txt       # Prompt for loot generation
│   └── langflow/                     # Langflow integration files
│       ├── pipelines.json            # Langflow pipeline configurations
│       └── README.md                 # Instructions for Langflow setup
│
├── tests/                            # Test scripts
│   ├── test_app.py                   # Unit tests for Flask app
│   ├── test_query.py                 # Unit tests for LangChain queries
│   ├── test_models.py                # Unit tests for AI models
│   └── test_integration.py           # Integration tests for full application
│
├── docs/                             # Documentation 
│   ├── README.md                     # Overview of the project
│   ├── setup.md                      # Setup instructions
│   └── api.md                        # API documentation
│
├── requirements.txt                  # Python dependencies for the project
├── Dockerfile                        # Dockerfile to containerize the application
├── docker-compose.yml                # Docker Compose file for multi-container setup
├── .gitignore                        # Ignore unnecessary files for Git
└── config.yaml                       # Configuration file for the application
```
