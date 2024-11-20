from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import gradio as gr
from gradio_interface import create_gradio_interface

# Create the Blueprint
bp = Blueprint('main', __name__)

# Folder paths for uploads
UPLOAD_FOLDER_MAPS = "app/maps/"
UPLOAD_FOLDER_TOKENS = "app/static/images/tokens/"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER_MAPS, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_TOKENS, exist_ok=True)

# Route for the index page
@bp.route('/')
def index():
    return render_template('index.html')

# Route to handle map uploads
@bp.route('/upload-map', methods=['POST'])
def upload_map():
    if 'map' not in request.files:
        return {"success": False, "message": "No file part"}, 400

    file = request.files['map']
    if file.filename == '':
        return {"success": False, "message": "No file selected"}, 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER_MAPS, filename)
        file.save(filepath)
        return {"success": True, "filename": filename, "message": f"Map {filename} uploaded successfully!"}, 200

# Route to handle token uploads
@bp.route('/upload-token', methods=['POST'])
def upload_token():
    if 'token' not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files['token']
    if file.filename == '':
        flash("No selected file")
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER_TOKENS, filename))
        flash(f"Token {filename} uploaded successfully!")
        return redirect(url_for('main.index'))
