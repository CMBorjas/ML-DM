from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    """Factory function to create the Flask app."""
    app = Flask(__name__)

    # App configurations
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    # Register blueprints or routes
    from .routes import main
    app.register_blueprint(main)

    return app
