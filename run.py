from flask import Flask
import threading
import gradio as gr
from app import create_app
import os
import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

# Initialize the Flask app
app = create_app()

# Define a simple Gradio function
def generate_response(query):
    return f"Gradio received query: {query}"

# Create the Gradio interface
gradio_interface = gr.Interface(
    fn=generate_response,
    inputs="text",
    outputs="text",
    title="Dungeon Master Assistant",
    description="Gradio Interface for Dungeon Master."
)

# Function to run Gradio
def run_gradio():
    try:
        logging.info("Starting Gradio...")
        # Launch Gradio and suppress blocking
        gradio_interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            quiet=True  # Suppress verbose output
        )
    except Exception as e:
        logging.error(f"Gradio encountered an error: {e}")

# Function to run Flask
def run_flask():
    try:
        logging.info("Starting Flask...")
        app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)  # Disable reloader for threading
    except Exception as e:
        logging.error(f"Flask encountered an error: {e}")

if __name__ == "__main__":
    # Run Gradio in a separate thread
    gradio_thread = threading.Thread(target=run_gradio, daemon=True)  # Daemon ensures it exits with the main program
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
