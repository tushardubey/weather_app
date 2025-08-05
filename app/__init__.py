from flask import Flask
from .routes import main
import os

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app = Flask(__name__, template_folder=template_dir)

    app.register_blueprint(main)
    return app
