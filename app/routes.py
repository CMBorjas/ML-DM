import os
import json
import gradio as gr
import psutil
import threading
from werkzeug.utils import secure_filename
from app.models import get_all_npcs
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

UPLOAD_FOLDER = os.path.join("app", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Define the Blueprint
main = Blueprint("main", __name__, template_folder="templates", static_folder="static")

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Path to the NPC storage file
NPC_FILE_PATH = os.path.join("data", "campaign", "npcs.json")

# Helper function to check if the uploaded file is allowed ------------------------------------------------------------------------------
def allowed_file(filename):
    """
    Helper function to check if the uploaded file is allowed.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to release a port ------------------------------------------------------------------------------------------------------
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

# Add the index route to the Blueprint --------------------------------------------------------------------------------------------------
@main.route("/")
def index():
    """
    Serve the main Dungeon Master Map page with NPCs loaded.
    """
    # Ensure the file exists and is initialized
    if not os.path.exists(NPC_FILE_PATH):
        with open(NPC_FILE_PATH, "w") as file:
            json.dump([], file)  # Initialize with an empty list

    with open(NPC_FILE_PATH, "r") as file:
        npcs = json.load(file)
    print("NPCs passed to template:", npcs)  # Debugging line
    return render_template("index.html", npcs=npcs)

# Add the upload map route to the Blueprint --------------------------------------------------------------------------------------------
@main.route("/upload_map", methods=["POST"])
def upload_map():
    """
    Handle map uploads.
    """
    if "map" not in request.files:
        flash("No map file part")
        return redirect(url_for("main.index"))

    file = request.files["map"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("main.index"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        flash(f"Map uploaded successfully: {filename}")
        return redirect(url_for("main.index"))
    else:
        flash("Invalid file type. Only images are allowed.")
        return redirect(url_for("main.index"))

# Add the upload token route to the Blueprint -------------------------------------------------------------------------------------------
@main.route("/upload_token", methods=["POST"])
def upload_token():
    """
    Handle token uploads.
    """
    if "token" not in request.files:
        flash("No token file part")
        return redirect(url_for("main.index"))

    file = request.files["token"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("main.index"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        flash(f"Token uploaded successfully: {filename}")
        return redirect(url_for("main.index"))
    else:
        flash("Invalid file type. Only images are allowed.")
        return redirect(url_for("main.index"))

# Add the proxy route to the Gradio interface -------------------------------------------------------------------------------------------
@main.route("/proxy_to_gradio/", defaults={"path": ""})
@main.route("/proxy_to_gradio/<path:path>")
def proxy_to_gradio(path):
    """
    Proxy to the Gradio interface.
    """
    return redirect(f"http://127.0.0.1:7860/{path}")


# Route to load NPCs and pass them to the frontend --------------------------------------------------------------------------------------
@main.route("/npcs", methods=["GET"])
def load_npcs():
    with open(NPC_FILE_PATH, "r") as file:
        npcs = json.load(file)
    return render_template("index.html", npcs=npcs)

# Route for Gradio chat with a specific NPC
@main.route("/talk_to_npc_gradio/<npc_name>", methods=["GET"])
def talk_to_npc_gradio(npc_name):
    """
    Redirects to a Gradio interface for chatting with the selected NPC.
    """
    if not os.path.exists(NPC_FILE_PATH):
        return jsonify({"error": "NPC storage file not found!"}), 500

    with open(NPC_FILE_PATH, "r") as file:
        npcs = json.load(file)

    npc = next((npc for npc in npcs if npc["name"] == npc_name), None)
    if not npc:
        return jsonify({"error": "NPC not found!"}), 404

    def chat_with_npc(user_input):
        response = f"{npc['name']} the {npc['class']} says: 'Ah, {user_input}! Tell me more.'"
        return response

    gradio_interface = gr.Interface(
        fn=chat_with_npc,
        inputs="text",
        outputs="text",
        title=f"Chat with {npc['name']}",
        description=f"You are chatting with {npc['name']}, a level {npc['level']} {npc['race']} {npc['class']}.",
    )

    # Release port if in use and dynamically select a port
    server_port = 7861
    release_port(server_port)

    def launch_gradio():
        gradio_interface.launch(
            server_name="127.0.0.1",
            server_port=server_port,
            share=False,
            prevent_thread_lock=True,  # Non-blocking
        )

    # Start Gradio in a separate thread
    threading.Thread(target=launch_gradio).start()

    # Redirect to the Gradio interface
    return redirect(f"http://127.0.0.1:{server_port}")
    return redirect("http://127.0.0.1:7861")

# Route to handle deleting an NPC
@main.route("/delete_npc/<npc_name>", methods=["DELETE"])
def delete_npc(npc_name):
    with open(NPC_FILE_PATH, "r") as file:
        npcs = json.load(file)

    # Filter out the NPC to delete
    updated_npcs = [npc for npc in npcs if npc["name"] != npc_name]

    if len(updated_npcs) == len(npcs):
        return jsonify({"success": False, "message": "NPC not found."}), 404

    # Save the updated list back to the file
    with open(NPC_FILE_PATH, "w") as file:
        json.dump(updated_npcs, file)

    return jsonify({"success": True})
