from flask import Blueprint, render_template

# Define a blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page route."""
    return render_template('index.html', title="Dungeon Master Assistant")
