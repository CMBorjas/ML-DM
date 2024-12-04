import os
import logging
import time
import psutil
import atexit
import signal
import threading
import gradio as gr
import json

from flask import Flask, render_template, request, jsonify, redirect
from app import create_app
from app.models import generate_npc

# Configure logging ---------------------------------------------------------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

# Initialize the Flask app -------------------------------------------------------------------------------------------------------------
app = create_app()

# Path to the NPC storage file
NPC_FILE_PATH = os.path.join("data", "campaign", "npcs.json")

# Ensure the data directory exists and read the NPCs from file ----------------------------------------------------------------------------
def get_npcs():
    """"Retrive the list of all NPCs"""
    if os.path.exists(NPC_FILE_PATH):
        with open(NPC_FILE_PATH, "r") as file:
            return json.load(file)
    return []

# Define the Gradio function ------------------------------------------------------------------------------------------------------------
def generate_response(query):
    """
    Gradio function to handle NPC generation and conversation.
    """

    npc = get_npcs()

    logging.debug(f"Received query: {query}")  # Log incoming query
    if query.lower().startswith("create npc"):
        # Generate a new NPC
        npc = generate_npc(name="Azaavara Minstrel")  # Example name
        npc_details = (
            f"NPC Created:\n"
            f"Name: {npc['name']}\n"
            f"Class: {npc['class']}\n"
            f"Race: {npc['race']}\n"
            f"Level: {npc['level']}\n"
            f"Abilities: {', '.join(npc['abilities'])}\n"
            f"Languages: {', '.join(npc['languages'])}\n"
            f"Spells: {', '.join(npc['spells'])}\n"
            f"Special Abilities: {', '.join(npc['special_abilities'])}"
        )
        return npc_details
    
    elif query.lower().startswith("talk to npc"):
        # Handle conversation with the NPC
        npc_name = query.split("talk to npc")[-1].strip()
        with open(NPC_FILE_PATH, "r") as file:
            npcs = json.load(file)
        
        npc = next((npc for npc in npcs if npc['name'].lower() == npc_name.lower()), None)
        if npc:
            return f"The NPC {npc['name']} says: 'Hello, traveler! What brings you to my realm?'"
        else:
            return f"NPC {npc_name} not found."
    
    elif query.lower().startswith("delete npc"):
        # Handle NPC deletion
        npc_name = query.split("delete npc")[-1].strip()
        with open(NPC_FILE_PATH, "r") as file:
            npcs = json.load(file)
        
        updated_npcs = [npc for npc in npcs if npc['name'].lower() != npc_name.lower()]
        if len(updated_npcs) == len(npcs):
            return f"NPC {npc_name} not found."
        
        with open(NPC_FILE_PATH, "w") as file:
            json.dump(updated_npcs, file)
        
        return f"NPC {npc_name} has been deleted."
    
    else:
        # Default response for undefined queries
        return "I am not sure how to respond to that. Try 'create NPC' or 'talk to NPC'."

# Create the Gradio interface------------------------------------------------------------------------------------------------------------
gradio_interface = gr.Interface(
    fn=generate_response,
    inputs="text",
    outputs="text",
    title="Dungeon Master Assistant",
    description="Interact with the Dungeon Master Assistant to create NPCs or chat with them."
)

# Flask route for the Gradio proxy
@app.route("/gradio/<path:path>")
def proxy_to_gradio(path):
    """
    Proxy requests to the Gradio interface running on port 7860.
    """
    return redirect(f"http://127.0.0.1:7860/{path}")

# Function to release a port if already in use -------------------------------------------------------------------------------------------
def release_port(port):
    """
    Ensure the specified port is available by terminating any process using it.
    """
    for conn in psutil.net_connections(kind="tcp"):
        if conn.laddr.port == port:
            try:
                process = psutil.Process(conn.pid)
                process.terminate()
                process.wait(timeout=3)
                print(f"Terminated process using port {port}.")
            except psutil.NoSuchProcess:
                print(f"Port {port} already free.")
            except Exception as e:
                print(f"Failed to release port {port}: {e}")

# Function to run Gradio
def run_gradio():
    try:
        # Placeholder function for the interface (to avoid crashing when idle)
        def default_function(user_input):
            return "Gradio is ready to connect NPCs for chat."

        # Keep Gradio's main server running
        gr.Interface(
            fn=default_function,
            inputs="text",
            outputs="text",
            title="Gradio Main Server"
        ).launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            quiet=True,
        )
    except Exception as e:
        logging.error(f"Gradio encountered an error: {e}")

# Function to run Flask
def run_flask():
    try:
        logging.info("Starting Flask...")
        release_port(5000)  # Ensure port is available
        app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logging.error(f"Flask encountered an error: {e}")

# Cleanup function for termination
def cleanup(signal=None, frame=None):
    logging.info("Cleaning up...")
    release_port(7860)
    release_port(5000)
    os.system("kill -9 $(lsof -t -i:5000)")  # Terminate Flask app if needed
    os.system("kill -9 $(lsof -t -i:7860)")  # Terminate Gradio app if needed
    logging.info("Cleanup complete.")

# Register cleanup for application exit
atexit.register(cleanup)
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

if __name__ == "__main__":
    # Run Gradio in a separate thread
    gradio_thread = threading.Thread(target=run_gradio, daemon=True)
    gradio_thread.start()

    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Keep the main thread alive to prevent premature termination
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Exiting...")
