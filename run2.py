from flask import Flask, render_template, request, jsonify
import threading
import gradio as gr
from app import create_app
import os
import logging
import time
import psutil
import atexit
import signal

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

# Initialize the Flask app
app = create_app()

# Define the Gradio function
def generate_response(query):
    """
    Gradio function to generate a response for Dungeon Masters.
    """
    response = f"AI Suggestion: {query}"  # Example logic
    return response

# Create the Gradio interface
gradio_interface = gr.Interface(
    fn=generate_response,
    inputs="text",
    outputs="text",
    title="Dungeon Master Assistant",
    description="Gradio Interface for Dungeon Master AI suggestions."
)

# Flask route for the Gradio proxy
@app.route("/gradio/<path:path>")
def proxy_to_gradio(path):
    """
    Proxy requests to the Gradio interface running on port 7860.
    """
    return redirect(f"http://127.0.0.1:7860/{path}")

# Function to release a port if already in use
def release_port(port):
    for conn in psutil.net_connections(kind="tcp"):
        if conn.laddr.port == port:
            logging.info(f"Terminating process using port {port}")
            try:
                process = psutil.Process(conn.pid)
                process.terminate()
                process.wait(timeout=3)
                logging.info(f"Process on port {port} terminated successfully.")
            except psutil.NoSuchProcess:
                logging.info(f"Process on port {port} is already terminated.")
            except Exception as e:
                logging.error(f"Could not terminate process on port {port}: {e}")

# Function to run Gradio
def run_gradio():
    try:
        gradio_interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            quiet=True
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
