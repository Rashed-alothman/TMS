# app.py
# The controller — this file's only job is to wire everything together.
# It creates the app, loads config, registers blueprints, and starts the server.

import logging
import os

from flask import Flask
from models.database import db
from routes.task_routes import task_api
from views.page_views import pages


def create_app():
    """
    Application factory function.
    Calling this function creates and configures a fresh Flask app.
    This pattern makes testing much easier — you can create isolated app instances per test.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # --- Configuration ---
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///tms.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Initialize extensions with this app ---
    db.init_app(app)

    # --- Register Blueprints (route groups) ---
    app.register_blueprint(pages)  # HTML pages: /, /homepage, /login, /about
    app.register_blueprint(task_api)  # REST API:   /homepage/api/tasks/...

    # --- Create database tables if they don't exist ---
    with app.app_context():
        db.create_all()

    return app


# Configure logging once, at startup
logging.basicConfig(level=logging.INFO)

app = create_app()

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
