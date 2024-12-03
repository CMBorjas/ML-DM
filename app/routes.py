from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join("app", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Define the Blueprint
main = Blueprint("main", __name__, template_folder="templates", static_folder="static")

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """
    Helper function to check if the uploaded file is allowed.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/")
def index():
    """
    Serve the main Dungeon Master Map page.
    """
    return render_template("index.html")

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

@main.route("/proxy_to_gradio/", defaults={"path": ""})
@main.route("/proxy_to_gradio/<path:path>")
def proxy_to_gradio(path):
    """
    Proxy to the Gradio interface.
    """
    return redirect(f"http://127.0.0.1:7860/{path}")

